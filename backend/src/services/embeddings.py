"""
Embeddings Service
Wrapper for SentenceTransformer model for generating text embeddings.
"""

import logging
from typing import List
from sentence_transformers import SentenceTransformer
from functools import lru_cache

from src.core.config import get_settings

logger = logging.getLogger(__name__)


@lru_cache(maxsize=1)
def get_embedding_model() -> SentenceTransformer:
    """
    Get or create the embedding model instance.
    Uses LRU cache to ensure only one model instance is created.

    Returns:
        SentenceTransformer: The initialized embedding model
    """
    settings = get_settings()
    model_name = settings.embedding_model_name
    logger.info(f"Initializing SentenceTransformer with model: {model_name}")

    try:
        model = SentenceTransformer(model_name)
        logger.info(f"Successfully initialized embedding model: {model_name}")
        return model
    except Exception as e:
        logger.error(f"Failed to initialize embedding model '{model_name}': {str(e)}")
        raise


class EmbeddingService:
    """Service for generating embeddings from text using SentenceTransformer."""

    def __init__(self):
        """Initialize the embedding service."""
        self.model = get_embedding_model()
        self.model_name = get_settings().embedding_model_name
        logger.info(f"EmbeddingService initialized with model: {self.model_name}")

    def encode(self, text: str) -> List[float]:
        """
        Generate embedding vector for the input text.

        Args:
            text: Input text to encode

        Returns:
            List[float]: Embedding vector (384 dimensions for all-MiniLM-L6-v2)

        Raises:
            ValueError: If text is empty or None
            Exception: If embedding generation fails
        """
        if not text or not text.strip():
            raise ValueError("Input text cannot be empty")

        try:
            logger.debug(f"Encoding text: {text[:50]}...")
            embedding = self.model.encode(text).tolist()
            logger.debug(f"Generated embedding of length {len(embedding)}")
            return embedding
        except Exception as e:
            logger.error(f"Error encoding text: {str(e)}", exc_info=True)
            raise

    def encode_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embedding vectors for multiple texts in batch.
        More efficient than calling encode() multiple times.

        Args:
            texts: List of input texts to encode

        Returns:
            List[List[float]]: List of embedding vectors

        Raises:
            ValueError: If texts list is empty
            Exception: If embedding generation fails
        """
        if not texts:
            raise ValueError("Input texts list cannot be empty")

        try:
            logger.debug(f"Encoding batch of {len(texts)} texts")
            embeddings = self.model.encode(texts).tolist()
            logger.debug(f"Generated {len(embeddings)} embeddings")
            return embeddings
        except Exception as e:
            logger.error(f"Error encoding batch: {str(e)}", exc_info=True)
            raise

    def get_model_info(self) -> dict:
        """
        Get information about the current embedding model.

        Returns:
            dict: Model information including name and dimension
        """
        return {
            "model_name": self.model_name,
            "embedding_dimension": self.model.get_sentence_embedding_dimension(),
        }


# Global instance for reuse
_embedding_service_instance = None


def get_embedding_service() -> EmbeddingService:
    """
    Get or create the global EmbeddingService instance.

    Returns:
        EmbeddingService: The global embedding service instance
    """
    global _embedding_service_instance
    if _embedding_service_instance is None:
        _embedding_service_instance = EmbeddingService()
    return _embedding_service_instance
