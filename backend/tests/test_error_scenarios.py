import pytest
import asyncio
from unittest.mock import Mock, patch, MagicMock
from src.services.rag_service import RAGService
from src.api.chat import chat_endpoint, is_off_topic_query
from src.models.chat import ChatRequest
from fastapi import HTTPException, Request
from slowapi.errors import RateLimitExceeded
from fastapi.requests import Request as FastAPIRequest
from starlette.datastructures import Address
import time
import uuid


class TestErrorScenarios:
    """Comprehensive test suite for error scenarios in the RAG system."""

    @pytest.fixture
    def mock_request(self):
        """Create a mock request object for rate limiting tests."""
        request = Mock(spec=FastAPIRequest)
        request.client = Mock()
        request.client.host = "127.0.0.1"
        return request

    @pytest.fixture
    def valid_chat_request(self):
        """Create a valid ChatRequest for testing."""
        return ChatRequest(query="What is ROS 2?")

    @pytest.fixture
    def rag_service_mock(self):
        """Create a mock RAG service."""
        with patch('src.api.chat.RAGService') as mock_class:
            mock_instance = Mock()
            mock_instance.chat.return_value = "ROS 2 is a flexible framework for writing robot applications."
            mock_class.return_value = mock_instance
            yield mock_instance

    def test_empty_query_validation(self):
        """Test validation for empty query."""
        with pytest.raises(ValueError):
            ChatRequest(query="")

    def test_whitespace_only_query_validation(self):
        """Test validation for whitespace-only query."""
        with pytest.raises(ValueError):
            ChatRequest(query="   ")

    def test_long_query_validation(self):
        """Test validation for queries that exceed length limit."""
        long_query = "A" * 1001  # More than 1000 characters
        with pytest.raises(ValueError):
            ChatRequest(query=long_query)

    def test_query_sanitization_removes_excess_whitespace(self):
        """Test that query sanitization removes excessive whitespace."""
        test_query = "  What    is   ROS 2?  "
        request = ChatRequest(query=test_query)
        # The validator should remove excess whitespace
        assert " " not in request.query.strip() or request.query.count("  ") == 0

    def test_query_sanitization_xss_prevention(self):
        """Test that query sanitization prevents XSS attempts."""
        xss_query = "<script>alert('xss')</script>"
        with pytest.raises(ValueError, match="potentially unsafe content"):
            ChatRequest(query=xss_query)

    def test_query_sanitization_javascript_protocol_prevention(self):
        """Test that query sanitization prevents JavaScript protocol attempts."""
        js_query = "javascript:alert('xss')"
        with pytest.raises(ValueError, match="potentially unsafe content"):
            ChatRequest(query=js_query)

    def test_off_topic_query_detection(self):
        """Test detection of off-topic queries."""
        off_topic_queries = [
            "Tell me a joke",
            "What's the weather like?",
            "Do you have an opinion on politics?",
            "How are you feeling today?"
        ]

        for query in off_topic_queries:
            assert is_off_topic_query(query) is True

    def test_on_topic_query_detection(self):
        """Test that on-topic queries are not flagged as off-topic."""
        on_topic_queries = [
            "What is robot kinematics?",
            "Explain ROS 2 architecture",
            "How does humanoid locomotion work?",
            "What is physical AI?"
        ]

        for query in on_topic_queries:
            assert is_off_topic_query(query) is False

    @pytest.mark.asyncio
    async def test_chat_endpoint_empty_query_error(self, mock_request):
        """Test chat endpoint with empty query."""
        empty_request = ChatRequest(query="")
        with pytest.raises(HTTPException) as exc_info:
            await chat_endpoint(empty_request, mock_request)
        assert exc_info.value.status_code == 422

    @pytest.mark.asyncio
    async def test_chat_endpoint_whitespace_only_query_error(self, mock_request):
        """Test chat endpoint with whitespace-only query."""
        whitespace_request = ChatRequest(query="   ")
        with pytest.raises(HTTPException) as exc_info:
            await chat_endpoint(whitespace_request, mock_request)
        assert exc_info.value.status_code == 422

    @pytest.mark.asyncio
    async def test_chat_endpoint_xss_query_error(self, mock_request):
        """Test chat endpoint with XSS attempt."""
        xss_request = ChatRequest(query="<script>alert('xss')</script>")
        with pytest.raises(HTTPException) as exc_info:
            await chat_endpoint(xss_request, mock_request)
        assert exc_info.value.status_code == 422

    @pytest.mark.asyncio
    async def test_chat_endpoint_off_topic_response(self, mock_request):
        """Test chat endpoint response for off-topic queries."""
        off_topic_request = ChatRequest(query="Tell me a joke")
        response = await chat_endpoint(off_topic_request, mock_request)
        assert "only answer questions about" in response["response"].lower()
        assert "request_id" in response

    @pytest.mark.asyncio
    async def test_chat_endpoint_rate_limit_error(self, mock_request):
        """Test chat endpoint behavior when rate limit is exceeded."""
        # Create a request that will trigger rate limit
        valid_request = ChatRequest(query="What is ROS 2?")

        # Mock the rate limiting to raise an exception
        with patch('src.api.chat.limiter') as limiter_mock:
            limiter_mock.limit = Mock(side_effect=RateLimitExceeded("Rate limit exceeded"))

            # Simulate rate limit exceeded
            with pytest.raises(HTTPException) as exc_info:
                await chat_endpoint(valid_request, mock_request)
            assert exc_info.value.status_code == 429

    @pytest.mark.asyncio
    async def test_chat_endpoint_rag_service_error(self, rag_service_mock, mock_request):
        """Test chat endpoint when RAG service returns error response."""
        error_request = ChatRequest(query="Test query")
        rag_service_mock.chat.return_value = "The chatbot is currently unavailable due to an error."

        # Patch the global rag_service instance to use our mock
        with patch('src.api.chat.rag_service', rag_service_mock):
            response = await chat_endpoint(error_request, mock_request)
            assert "currently unavailable" in response["response"]
            assert "request_id" in response

    @pytest.mark.asyncio
    async def test_chat_endpoint_rag_service_exception(self, rag_service_mock, mock_request):
        """Test chat endpoint when RAG service throws an exception."""
        error_request = ChatRequest(query="Test query")
        rag_service_mock.chat.side_effect = Exception("Test error")

        # Patch the global rag_service instance to use our mock
        with patch('src.api.chat.rag_service', rag_service_mock):
            with pytest.raises(HTTPException) as exc_info:
                await chat_endpoint(error_request, mock_request)
            assert exc_info.value.status_code == 500

    @pytest.mark.asyncio
    async def test_chat_endpoint_internal_error(self, rag_service_mock, mock_request):
        """Test chat endpoint for internal server errors."""
        # Simulate an internal error in the chat endpoint
        with patch('src.api.chat.rag_service.chat', side_effect=Exception("Internal error")):
            test_request = ChatRequest(query="Test query")
            with pytest.raises(HTTPException) as exc_info:
                await chat_endpoint(test_request, mock_request)
            assert exc_info.value.status_code == 500

    def test_rag_service_performance_metrics(self):
        """Test RAG service performance metrics collection."""
        with patch('src.services.rag_service.SentenceTransformer'), \
             patch('src.services.rag_service.QdrantClient'), \
             patch('src.services.rag_service.OpenAI'):
            service = RAGService()

            # Verify metrics structure exists
            metrics = service.get_performance_metrics()
            assert 'total_queries' in metrics
            assert 'cache_hit_rate_percent' in metrics
            assert 'avg_embedding_time_seconds' in metrics
            assert 'avg_total_time_seconds' in metrics

    def test_rag_service_error_handling_in_chat_method(self):
        """Test RAG service error handling in chat method."""
        with patch('src.services.rag_service.SentenceTransformer') as mock_st, \
             patch('src.services.rag_service.QdrantClient') as mock_qdrant, \
             patch('src.services.rag_service.OpenAI') as mock_openai:

            # Mock the embedding model to raise an exception
            mock_st.return_value = Mock()
            mock_st.return_value.encode.side_effect = Exception("Embedding error")

            service = RAGService()
            result = service.chat("Test query")

            # Should return error message instead of crashing
            assert "encountered an error" in result.lower()

    def test_rag_service_embedding_error_retry_logic(self):
        """Test RAG service retry logic for embedding errors."""
        with patch('src.services.rag_service.SentenceTransformer') as mock_st, \
             patch('src.services.rag_service.QdrantClient') as mock_qdrant, \
             patch('src.services.rag_service.OpenAI') as mock_openai:

            # Mock the embedding model to fail once then succeed
            mock_st.return_value = Mock()
            mock_st.return_value.encode = Mock(side_effect=[Exception("First try failed"), [0.1] * 384])

            service = RAGService()
            result = service.chat("Test query")

            # Method should have been called twice (first failed, second succeeded)
            assert mock_st.return_value.encode.call_count == 2
            # Should not be an error response since retry succeeded
            assert "encountered an error" not in result.lower()

    def test_rag_service_retrieval_error_handling(self):
        """Test RAG service error handling for retrieval errors."""
        with patch('src.services.rag_service.SentenceTransformer') as mock_st, \
             patch('src.services.rag_service.QdrantClient') as mock_qdrant, \
             patch('src.services.rag_service.OpenAI') as mock_openai:

            # Mock the Qdrant client to raise an exception
            mock_qdrant_instance = Mock()
            mock_qdrant_instance.search.side_effect = Exception("Qdrant error")
            mock_qdrant.return_value = mock_qdrant_instance

            # Set up the embedding model
            mock_st.return_value = Mock()
            mock_st.return_value.encode.return_value = [0.1] * 384

            service = RAGService()
            result = service.chat("Test query")

            # Should return empty context result, not crash
            assert service.retrieve_context([0.1] * 384) == []

    def test_rag_service_generation_error_handling(self):
        """Test RAG service error handling for generation errors."""
        with patch('src.services.rag_service.SentenceTransformer') as mock_st, \
             patch('src.services.rag_service.QdrantClient') as mock_qdrant, \
             patch('src.services.rag_service.OpenAI') as mock_openai:

            # Set up the embedding model
            mock_st.return_value = Mock()
            mock_st.return_value.encode.return_value = [0.1] * 384

            # Set up Qdrant to return context
            mock_qdrant_instance = Mock()
            mock_search_result = Mock()
            mock_search_result.id = "test_id"
            mock_search_result.payload = {"text": "Test context", "source": "test.md", "section": "Test"}
            mock_search_result.score = 0.9
            mock_qdrant_instance.search.return_value = [mock_search_result]
            mock_qdrant.return_value = mock_qdrant_instance

            # Mock OpenAI to raise an exception
            mock_openai_instance = Mock()
            mock_openai_instance.chat.completions.create.side_effect = Exception("OpenAI error")
            mock_openai.return_value = mock_openai_instance

            service = RAGService()
            result = service.chat("Test query")

            # Should handle the error gracefully
            assert "encountered an error" in result.lower()

    @pytest.mark.asyncio
    async def test_chat_endpoint_request_id_generation(self, rag_service_mock, mock_request):
        """Test that each request gets a unique request ID."""
        with patch('src.api.chat.rag_service', rag_service_mock):
            # Make multiple requests and check request IDs
            request1 = ChatRequest(query="First query")
            response1 = await chat_endpoint(request1, mock_request)

            request2 = ChatRequest(query="Second query")
            response2 = await chat_endpoint(request2, mock_request)

            # Both responses should have request IDs
            assert "request_id" in response1
            assert "request_id" in response2

            # Request IDs should be different
            assert response1["request_id"] != response2["request_id"]

            # Request IDs should be valid UUIDs
            uuid.UUID(response1["request_id"])
            uuid.UUID(response2["request_id"])

    def test_error_response_structure(self):
        """Test that error responses have the correct structure."""
        from src.api.chat import ErrorResponse, ValidationErrorResponse

        # Test ErrorResponse structure
        error_resp = ErrorResponse(
            error="Test Error",
            error_code="TEST_ERROR",
            message="Test message",
            timestamp="2023-01-01T00:00:00Z"
        )
        assert hasattr(error_resp, 'error')
        assert hasattr(error_resp, 'error_code')
        assert hasattr(error_resp, 'message')
        assert hasattr(error_resp, 'timestamp')

        # Test ValidationErrorResponse structure
        validation_resp = ValidationErrorResponse(
            error="Validation Error",
            error_code="VALIDATION_ERROR",
            message="Test validation message",
            details=[{"field": "test", "error": "test error"}],
            timestamp="2023-01-01T00:00:00Z"
        )
        assert hasattr(validation_resp, 'details')
        assert isinstance(validation_resp.details, list)


class TestSecurityErrorScenarios:
    """Test security-related error scenarios."""

    @pytest.mark.asyncio
    async def test_chat_endpoint_malicious_content_detection(self, mock_request):
        """Test detection and rejection of malicious content."""
        malicious_queries = [
            "<script>alert('xss')</script>",
            "javascript:alert('xss')",
            "onload=alert('xss')",
            "<img src=x onerror=alert('xss')>",
        ]

        for malicious_query in malicious_queries:
            with pytest.raises(HTTPException) as exc_info:
                malicious_request = ChatRequest(query=malicious_query)
                await chat_endpoint(malicious_request, mock_request)
            assert exc_info.value.status_code == 422

    @pytest.mark.asyncio
    async def test_chat_endpoint_long_content_rejection(self, mock_request):
        """Test rejection of excessively long content."""
        long_content = "A" * 1001  # More than the 1000 character limit
        with pytest.raises(HTTPException) as exc_info:
            long_request = ChatRequest(query=long_content)
            await chat_endpoint(long_request, mock_request)
        assert exc_info.value.status_code == 422


if __name__ == "__main__":
    pytest.main([__file__])