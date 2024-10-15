# comment_classifier.py

import logging

from transformers import pipeline

from gpu_resource_manager import GPUResourceManager


class CommentClassifier:
    def __init__(self):
        logging.info("Loading zero-shot classification model on CUDA...")
        self.classifier = pipeline(
            "zero-shot-classification",
            model="facebook/bart-large-mnli",
            device='cuda',
            batch_size=384
        )

    def classify_comments_batch(self, comments):
        if not all(isinstance(comment, str) and comment for comment in comments):
            logging.error("All comments must be non-empty strings.")
            return []

        labels = ["Claim", "Counterclaim", "Rebuttal", "Evidence"]

        if not comments:
            logging.warning("No comments to classify in this batch.")
            return []

        logging.info(f"Classifying batch of {len(comments)} comments...")

        try:
            results = self.classifier(comments, candidate_labels=labels)
            classifications = [result['labels'][0] for result in results]
            logging.info("Comment classification completed.")
            return classifications

        except ValueError as ve:
            logging.error(f"ValueError occurred: {ve}")
            return []
        except Exception as e:
            logging.error(f"Unexpected error occurred during classification: {e}")
            return []
        finally:
            try:
                del results
                GPUResourceManager.clear_gpu_memory()
                logging.info("Memory cleanup completed.")
            except Exception as cleanup_error:
                logging.warning(f"Cleanup error: {cleanup_error}")
