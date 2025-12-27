"""
Embeddings Service
Uses FastEmbed (CPU-only ONNX) for generating text embeddings.
Compatible with all-MiniLM-L6-v2 model used for indexing.
"""

import logging
from typing import List
from fastembed import TextEmbedding
from functools import lru_cache

from src.core.config import get_settings

logger = logging.getLogger(__name__)


@lru_cache(maxsize=1)
def get_embedding_model() -> TextEmbedding:
    """Get or create the embedding model instance."""
    settings = get_settings()
    model_name = settings.embedding_model_name
    if not model_name.startswith("sentence-transformers/"):
        model_name = f"sentence-transformers/{model_name}"
    logger.info(f"Initializing FastEmbed with model: {model_name}")

    try:
        model = TextEmbedding(model_name=model_name)
        logger.info(f"Successfully initialized embedding model: {model_name}")
        return model
    except Exception as e:
        logger.error(f"Failed to initialize embedding model: {str(e)}")
        raise


class EmbeddingService:
    """Service for generating embeddings from text using FastEmbed."""

    def __init__(self):
        """Initialize the embedding service."""
        self.model = get_embedding_model()
        self.model_name = get_settings().embedding_model_name
        logger.info(f"EmbeddingService initialized with model: {self.model_name}")

    def encode(self, text: str) -> List[float]:
        """Generate embedding vector for the input text."""
        if not text or not text.strip():
            raise ValueError("Input text cannot be empty")

        try:
            logger.debug(f"Encoding text: {text[:50]}...")
            embeddings = list(self.model.embed([text]))
            embedding = embeddings[0].tolist()
            logger.debug(f"Generated embedding of length {len(embedding)}")
            return embedding
        except Exception as e:
            logger.error(f"Error encoding text: {str(e)}", exc_info=True)
            raise

    def encode_batch(self, texts: List[str]) -> List[List[float]]:
        """Generate embedding vectors for multiple texts in batch."""
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
        """Get information about the current embedding model."""
        return {
            "model_name": self.model_name,
            "embedding_dimension": 384,
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
