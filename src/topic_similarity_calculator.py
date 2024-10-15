# topic_similarity_calculator.py

import logging

import cupy as cp

from sentence_transformers import SentenceTransformer

from gpu_resource_manager import GPUResourceManager


class TopicSimilarityCalculator:
    def __init__(self):
        logging.info("Loading sentence embedding model on CUDA...")
        self.embedding_model = SentenceTransformer(
            'sentence-transformers/all-MiniLM-L6-v2', device='cuda'
        ).to('cuda')

    def get_topics_by_similarity_batch(self, comments, topics):
        logging.info(f"Calculating topic similarity for batch of {len(comments)} comments...")

        comment_embeddings = self.embedding_model.encode(comments, convert_to_tensor=True)
        topic_embeddings = self.embedding_model.encode(topics, convert_to_tensor=True)

        try:
            comment_embeddings_cp = cp.asarray(comment_embeddings)
            topic_embeddings_cp = cp.asarray(topic_embeddings)

            comment_embeddings_cp /= cp.linalg.norm(comment_embeddings_cp, axis=1, keepdims=True)
            topic_embeddings_cp /= cp.linalg.norm(topic_embeddings_cp, axis=1, keepdims=True)

            similarities = cp.matmul(comment_embeddings_cp, topic_embeddings_cp.T)
            closest_topic_indices = cp.argmax(similarities, axis=1)

            result = [topics[idx] for idx in closest_topic_indices.get()]
        finally:
            del comment_embeddings_cp, topic_embeddings_cp, similarities, closest_topic_indices
            GPUResourceManager.clear_gpu_memory()

        logging.info("Topic similarity calculation completed.")
        return result
