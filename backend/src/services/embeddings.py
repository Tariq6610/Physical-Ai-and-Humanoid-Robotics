"""
Embeddings Service
Wrapper for FastEmbed model for generating text embeddings.
Uses lightweight FastEmbed instead of sentence-transformers to reduce image size.
"""

import logging
from typing import List
from fastembed import TextEmbedding
from functools import lru_cache

from src.core.config import get_settings

logger = logging.getLogger(__name__)


@lru_cache(maxsize=1)
def get_embedding_model() -> TextEmbedding:
    """
    Get or create the embedding model instance.
    Uses LRU cache to ensure only one model instance is created.

    Returns:
        TextEmbedding: The initialized FastEmbed model
    """
    settings = get_settings()
    model_name = settings.embedding_model_name
    # FastEmbed uses full model path
    if not model_name.startswith("sentence-transformers/"):
        model_name = f"sentence-transformers/{model_name}"
    logger.info(f"Initializing FastEmbed with model: {model_name}")

    try:
        model = TextEmbedding(model_name=model_name)
        logger.info(f"Successfully initialized embedding model: {model_name}")
        return model
    except Exception as e:
        logger.error(f"Failed to initialize embedding model '{model_name}': {str(e)}")
        raise


class EmbeddingService:
    """Service for generating embeddings from text using FastEmbed."""

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
            # FastEmbed returns a generator, convert to list and get first item
            embeddings = list(self.model.embed([text]))
            embedding = embeddings[0].tolist()
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
            embeddings = [emb.tolist() for emb in self.model.embed(texts)]
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
            "embedding_dimension": 384,  # all-MiniLM-L6-v2 dimension
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
