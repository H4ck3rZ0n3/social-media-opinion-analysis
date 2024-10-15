# opinion_analyzer.py

import logging
import cudf
import os
from datasets import Dataset
from datetime import datetime

from comment_classifier import CommentClassifier
from conclusion_generator import ConclusionGenerator
from gpu_resource_manager import GPUResourceManager
from text_preprocessor import TextPreprocessor
from topic_similarity_calculator import TopicSimilarityCalculator


class OpinionAnalyzer:
    def __init__(self):
        self.preprocessor = TextPreprocessor()
        self.similarity_calculator = TopicSimilarityCalculator()
        self.comment_classifier = CommentClassifier()
        self.conclusion_generator = ConclusionGenerator()

    def load_data(self, topic_path, opinion_path):
        topics_df = cudf.read_csv(topic_path)
        self.topics_rw = topics_df['text'].to_pandas().tolist()

        opinion_df = cudf.read_csv(opinion_path)
        self.opinions_rw = opinion_df['text'].to_pandas().tolist()

        logging.info("Files loaded successfully.")

    def save_conclusions_data(self, conclusions):
        try:
            if not conclusions:
                logging.warning("No conclusions data available to save.")
                return

            topics = []
            summaries = []
            effectivenesses = []

            now = datetime.now()
            timestamp = now.strftime("%Y%m%d_%H%M%S")

            for topic, effectiveness, summary_list in conclusions:
                topics.append(topic)
                summaries.append(' '.join(summary_list))
                effectivenesses.append(effectiveness)

            df = cudf.DataFrame({
                'topic': topics,
                'summary': summaries,
                'effectiveness': effectivenesses
            })

            save_dir = 'outputs'
            if save_dir and not os.path.exists(save_dir):
                os.makedirs(save_dir, exist_ok=True)

            save_path = os.path.join(save_dir, f'conclusions_{timestamp}.csv')

            logging.info(f"Conclusions saving to {save_path}...")

            df.to_csv(save_path, index=False)

            logging.info(f"Conclusions successfully saved to {save_path}.")

        except Exception as e:
            logging.error(f"An error occurred while saving data: {e}")

    def save_opinions_data(self, comments):
        try:
            if not comments:
                logging.warning("No opinions data available to save.")
                return

            opinions = []
            topics = []
            types = []

            now = datetime.now()
            timestamp = now.strftime("%Y%m%d_%H%M%S")

            for comment in comments:
                opinions.append(comment['text'])
                topics.append(comment['topic'])
                types.append(comment['type'])

            df = cudf.DataFrame({
                'opinion': opinions,
                'topic': topics,
                'type': types
            })

            save_dir = 'outputs'
            if save_dir and not os.path.exists(save_dir):
                os.makedirs(save_dir, exist_ok=True)

            save_path = os.path.join(save_dir, f'opinions_{timestamp}.csv')

            logging.info(f"Opinions saving to {save_path}...")

            df.to_csv(save_path, index=False)

            logging.info(f"Opinions successfully saved to {save_path}.")

        except Exception as e:
            logging.error(f"An error occurred while saving data: {e}")

    def preprocess_data(self):
        logging.info("Preprocessing topics and opinions...")

        dataset_topic = (
            Dataset.from_dict({'topic': self.topics_rw})
            .map(lambda x: {'topic': self.preprocessor.preprocess_text(x['topic'])})
            .filter(lambda x: x['topic'] is not None)
        )

        dataset_opinion = (
            Dataset.from_dict({'opinion': self.opinions_rw})
            .map(lambda x: {'opinion': self.preprocessor.preprocess_text(x['opinion'])})
            .filter(lambda x: x['opinion'] is not None)
            # .take(500)  # Optional: limit for testing
        )

        self.topics = dataset_topic['topic']
        self.opinions = dataset_opinion['opinion']

    def batch_process_comments(self, batch_size=8192):
        self.classified_comments = []

        total_batches = (len(self.opinions) + batch_size - 1) // batch_size
        for i in range(0, len(self.opinions), batch_size):
            batch_number = i // batch_size + 1
            logging.info(f"Processing batch {batch_number}/{total_batches}...")

            batch_comments = self.opinions[i:i + batch_size]

            if not batch_comments:
                logging.warning("Skipping empty batch.")
                continue

            related_topics = self.similarity_calculator.get_topics_by_similarity_batch(
                batch_comments, self.topics
            )

            classifications = self.comment_classifier.classify_comments_batch(batch_comments)

            for comment, topic, classification in zip(batch_comments, related_topics, classifications):
                self.classified_comments.append({
                    "text": comment,
                    "topic": topic,
                    "type": classification
                })

            logging.info("Batch processing completed.")

        logging.info("All batches processed.")
        GPUResourceManager.clear_gpu_memory()

    def analyze_csv(self, topic_path, opinion_path):
        logging.info("Starting the main process...")

        self.load_data(topic_path, opinion_path)
        self.preprocess_data()
        self.batch_process_comments()

        logging.info("Generating conclusions...")

        conclusions = self.conclusion_generator.generate_conclusions(self.classified_comments)

        self.save_opinions_data(self.classified_comments)
        self.save_conclusions_data(conclusions)

        # If desired, print conclusions
        # for topic, effectiveness, topic_summaries in conclusions:
        #     print(f"Topic: {topic}\nEffectiveness: {effectiveness}\nSummary: {' '.join(topic_summaries)}\n")

        logging.info("Process completed.")

    def analyze_grpc(self, topics, opinions):
        logging.info("Starting the main process...")

        self.topics_rw = topics
        self.opinions_rw = opinions

        self.preprocess_data()
        self.batch_process_comments()

        logging.info("Generating conclusions...")

        conclusions = self.conclusion_generator.generate_conclusions(self.classified_comments)

        opinions_result = [
            (comment['text'], comment['topic'], comment['type'])
            for comment in self.classified_comments
        ]

        topics_result = [
            (topic, summary, effectiveness)
            for topic, effectiveness, summary_list in conclusions
            for summary in summary_list
        ]

        logging.info("Process completed.")

        return opinions_result, topics_result
