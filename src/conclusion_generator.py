# conclusion_generator.py

import logging
from collections import defaultdict

from transformers import BartTokenizer, BartForConditionalGeneration

from gpu_resource_manager import GPUResourceManager
from topic_effectiveness_classifier import TopicEffectivenessClassifier


class ConclusionGenerator:
    def __init__(self):
        self.tokenizer = BartTokenizer.from_pretrained("facebook/bart-large-cnn")
        self.summarization_model = BartForConditionalGeneration.from_pretrained(
            "facebook/bart-large-cnn"
        ).to('cuda')
        self.effectiveness_classifier = TopicEffectivenessClassifier()

    def generate_conclusions(self, opinions, batch_size=64):
        grouped_comments = defaultdict(list)
        for opinion in opinions:
            grouped_comments[opinion['topic']].append(opinion)

        results = []
        summaries = []

        all_comments = [
            (topic, comment) for topic, comments in grouped_comments.items() for comment in comments
        ]
        total_comments = len(all_comments)

        for i in range(0, len(all_comments), batch_size):
            batch = all_comments[i:i + batch_size]
            batch_comments = [t[1]['text'] for t in batch]

            progress = (i + len(batch)) / total_comments * 100
            logging.info(f"Processing Conclusions batch {progress:.2f}%... ")

            inputs = self.tokenizer(
                batch_comments,
                return_tensors="pt",
                max_length=1024,
                padding=True,
                truncation=True
            ).to('cuda')

            summary_ids = self.summarization_model.generate(
                inputs["input_ids"],
                max_length=100,
                min_length=30,
                length_penalty=2.0,
                num_beams=4,
                repetition_penalty=2.5,
                no_repeat_ngram_size=3,
                early_stopping=True
            )

            batch_summaries = [
                self.tokenizer.decode(g, skip_special_tokens=True)
                for g in summary_ids
            ]
            summaries.extend(batch_summaries)

        for topic, comments in grouped_comments.items():
            effectiveness = self.effectiveness_classifier.classify_topic_effectiveness(comments)
            topic_summaries = [
                summaries[i] for i, (t, _) in enumerate(all_comments) if t == topic
            ]

            results.append((topic, effectiveness, topic_summaries))

        GPUResourceManager.clear_gpu_memory()
        return results
