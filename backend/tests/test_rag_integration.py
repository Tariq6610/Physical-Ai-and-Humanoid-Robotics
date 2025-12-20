import pytest
import asyncio
from unittest.mock import Mock, patch, MagicMock
from src.services.rag_service import RAGService
from src.api.chat import chat_endpoint
from src.models.chat import ChatRequest
from fastapi import HTTPException
from slowapi.errors import RateLimitExceeded
from fastapi.requests import Request


class TestRAGServiceIntegration:
    """Integration tests for the RAG service pipeline."""

    @pytest.fixture
    def rag_service(self):
        """Create a RAGService instance for testing."""
        with patch('src.services.rag_service.SentenceTransformer'), \
             patch('src.services.rag_service.QdrantClient'), \
             patch('src.services.rag_service.OpenAI'):
            service = RAGService()
            service.embedding_model = Mock()
            service.embedding_model.encode.return_value = [0.1] * 384
            service.qdrant_client = Mock()
            service.openai_client = Mock()
            return service

    @pytest.fixture
    def mock_request(self):
        """Create a mock request object for rate limiting tests."""
        request = Mock(spec=Request)
        request.client = Mock()
        request.client.host = "127.0.0.1"
        return request

    def test_rag_pipeline_end_to_end(self, rag_service):
        """Test the complete RAG pipeline from query to response."""
        # Mock the embedding generation
        test_query = "What is ROS 2?"
        rag_service.embedding_model.encode.return_value = [0.1] * 384

        # Mock the Qdrant search results
        mock_search_result = Mock()
        mock_search_result.id = "test_id"
        mock_search_result.payload = {
            "text": "ROS 2 is a flexible framework for writing robot applications.",
            "source": "ch1-intro-ros.md",
            "section": "Introduction"
        }
        mock_search_result.score = 0.9
        rag_service.qdrant_client.search.return_value = [mock_search_result]

        # Mock the OpenAI response
        mock_choice = Mock()
        mock_choice.message.content = "ROS 2 is a flexible framework for writing robot applications."
        rag_service.openai_client.chat.completions.create.return_value.choices = [mock_choice]

        # Execute the pipeline
        result = rag_service.chat(test_query)

        # Verify the result
        assert result is not None
        assert "ROS 2" in result

        # Verify that all steps were called
        rag_service.embedding_model.encode.assert_called_once_with(test_query)
        rag_service.qdrant_client.search.assert_called_once()
        rag_service.openai_client.chat.completions.create.assert_called_once()

    def test_rag_pipeline_with_no_context(self, rag_service):
        """Test the RAG pipeline when no relevant context is found."""
        # Mock the embedding generation
        test_query = "What is quantum computing?"
        rag_service.embedding_model.encode.return_value = [0.1] * 384

        # Mock empty search results
        rag_service.qdrant_client.search.return_value = []

        # Execute the pipeline
        result = rag_service.chat(test_query)

        # Verify the result indicates no context found
        assert "couldn't find any relevant information" in result.lower()

    def test_rag_pipeline_with_error_handling(self, rag_service):
        """Test the RAG pipeline error handling."""
        # Mock the embedding generation to raise an exception
        test_query = "Test query"
        rag_service.embedding_model.encode.side_effect = Exception("Embedding error")

        # Execute the pipeline
        result = rag_service.chat(test_query)

        # Verify the result indicates an error
        assert "encountered an error" in result.lower()

    def test_rag_pipeline_with_retry_logic(self, rag_service):
        """Test that the RAG pipeline implements retry logic."""
        # Mock the embedding generation to fail once then succeed
        test_query = "Retry test"
        rag_service.embedding_model.encode.side_effect = [Exception("First try failed"), [0.1] * 384]

        # Mock the Qdrant search results
        mock_search_result = Mock()
        mock_search_result.id = "test_id"
        mock_search_result.payload = {
            "text": "Test context",
            "source": "test.md",
            "section": "Test"
        }
        mock_search_result.score = 0.9
        rag_service.qdrant_client.search.return_value = [mock_search_result]

        # Mock the OpenAI response
        mock_choice = Mock()
        mock_choice.message.content = "Test response"
        rag_service.openai_client.chat.completions.create.return_value.choices = [mock_choice]

        # Execute the pipeline
        result = rag_service.chat(test_query)

        # Verify that the method was called twice (first failed, second succeeded)
        assert rag_service.embedding_model.encode.call_count == 2
        assert result is not None


class TestChatAPIIntegration:
    """Integration tests for the chat API endpoint."""

    @pytest.fixture
    def chat_request(self):
        """Create a ChatRequest for testing."""
        return ChatRequest(query="What is ROS 2?")

    @pytest.fixture
    def rag_service_mock(self):
        """Create a mock RAG service."""
        with patch('src.api.chat.RAGService') as mock_class:
            mock_instance = Mock()
            mock_instance.chat.return_value = "ROS 2 is a flexible framework for writing robot applications."
            mock_class.return_value = mock_instance
            yield mock_instance

    def test_chat_endpoint_success(self, chat_request, rag_service_mock, mock_request):
        """Test successful chat endpoint request."""
        # Execute the endpoint
        result = asyncio.run(chat_endpoint(chat_request, mock_request))

        # Verify the result
        assert "response" in result
        assert "ROS 2" in result["response"]

        # Verify that the RAG service was called
        rag_service_mock.chat.assert_called_once_with(chat_request.query)

    def test_chat_endpoint_off_topic_query(self, mock_request):
        """Test chat endpoint with off-topic query."""
        off_topic_request = ChatRequest(query="Tell me a joke")

        # Execute the endpoint
        result = asyncio.run(chat_endpoint(off_topic_request, mock_request))

        # Verify the result indicates off-topic query
        assert "only answer questions about" in result["response"].lower()

    def test_chat_endpoint_rag_error(self, rag_service_mock, mock_request):
        """Test chat endpoint when RAG service returns error response."""
        chat_request = ChatRequest(query="Test query")
        rag_service_mock.chat.return_value = "The chatbot is currently unavailable."

        # Execute the endpoint
        result = asyncio.run(chat_endpoint(chat_request, mock_request))

        # Verify the result indicates unavailability
        assert "currently unavailable" in result["response"]

    def test_chat_endpoint_exception_handling(self, rag_service_mock, mock_request):
        """Test chat endpoint exception handling."""
        chat_request = ChatRequest(query="Test query")
        rag_service_mock.chat.side_effect = Exception("Test error")

        # Execute the endpoint
        result = asyncio.run(chat_endpoint(chat_request, mock_request))

        # Verify the result indicates unavailability
        assert "currently unavailable" in result["response"]

    def test_rate_limiting(self, chat_request, rag_service_mock, mock_request):
        """Test rate limiting functionality."""
        # Simulate rate limit exceeded
        with pytest.raises(RateLimitExceeded):
            raise RateLimitExceeded("Rate limit exceeded")


class TestCachingIntegration:
    """Integration tests for caching functionality."""

    @pytest.fixture
    def rag_service_with_cache(self):
        """Create a RAGService instance with caching enabled."""
        with patch('src.services.rag_service.SentenceTransformer'), \
             patch('src.services.rag_service.QdrantClient'), \
             patch('src.services.rag_service.OpenAI'):
            service = RAGService()
            service.embedding_model = Mock()
            service.embedding_model.encode.return_value = [0.1] * 384
            service.qdrant_client = Mock()
            service.openai_client = Mock()
            return service

    def test_cache_hit_and_miss(self, rag_service_with_cache):
        """Test caching functionality."""
        test_query = "Cached query test"

        # Mock the responses
        rag_service_with_cache.embedding_model.encode.return_value = [0.1] * 384
        mock_search_result = Mock()
        mock_search_result.id = "test_id"
        mock_search_result.payload = {
            "text": "Test cached response",
            "source": "test.md",
            "section": "Test"
        }
        mock_search_result.score = 0.9
        rag_service_with_cache.qdrant_client.search.return_value = [mock_search_result]

        mock_choice = Mock()
        mock_choice.message.content = "Test cached response"
        rag_service_with_cache.openai_client.chat.completions.create.return_value.choices = [mock_choice]

        # First call - should not be cached
        result1 = rag_service_with_cache.chat(test_query)

        # Second call with same query - should be cached
        result2 = rag_service_with_cache.chat(test_query)

        # Verify both results are the same
        assert result1 == result2

        # Verify that the RAG service methods were only called once due to caching
        assert rag_service_with_cache.embedding_model.encode.call_count == 1


if __name__ == "__main__":
    pytest.main([__file__])