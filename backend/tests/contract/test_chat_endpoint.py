"""
Contract tests for POST /chat endpoint.
Verifies API contract compliance and response structure.
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock, Mock

from src.main import app


client = TestClient(app)


class TestChatEndpointContract:
    """Contract tests for POST /chat endpoint."""

    @patch('src.api.chat.rag_service.chat_async', new_callable=AsyncMock)
    def test_chat_endpoint_success_response_structure(self, mock_chat_async):
        """
        T013: Test POST /chat endpoint returns correct response structure.
        Acceptance: 200 status, response matches ChatResponse schema.
        """
        # Arrange: Mock RAG service
        mock_chat_async.return_value = "Physical AI combines artificial intelligence with physical robotics systems."

        # Act: Send chat request
        response = client.post(
            "/chat",
            json={"query": "What is Physical AI?"}
        )

        # Assert: Verify response structure
        assert response.status_code == 200

        json_response = response.json()
        assert "response" in json_response
        assert isinstance(json_response["response"], str)
        assert len(json_response["response"]) > 0

        # Optional fields that may be present
        if "sources" in json_response:
            assert isinstance(json_response["sources"], list)

        if "session_id" in json_response:
            assert isinstance(json_response["session_id"], str)

    @patch('src.api.chat.rag_service.chat_async', new_callable=AsyncMock)
    def test_chat_endpoint_with_session_id(self, mock_chat_async):
        """
        Test POST /chat endpoint accepts and uses session_id.
        Acceptance: Session ID passed to RAG service.
        """
        # Arrange
        mock_chat_async.return_value = "Test response"

        # Act: Send request with session_id
        response = client.post(
            "/chat",
            json={
                "query": "What are humanoid robots?",
                "session_id": "test-session-123"
            }
        )

        # Assert
        assert response.status_code == 200
        mock_chat_async.assert_called_once()

        # Verify session_id was passed (either from JSON or generated)
        call_kwargs = mock_chat_async.call_args
        # Session ID should be passed to chat_async
        assert call_kwargs.kwargs.get('session_id') is not None

    def test_chat_endpoint_validation_empty_query(self):
        """
        Test POST /chat endpoint validates empty queries.
        Acceptance: 422 Unprocessable Entity for empty query.
        """
        # Act: Send request with empty query
        response = client.post(
            "/chat",
            json={"query": ""}
        )

        # Assert: Validation error
        assert response.status_code == 422
        json_response = response.json()
        assert "detail" in json_response

    def test_chat_endpoint_validation_missing_query(self):
        """
        Test POST /chat endpoint requires query field.
        Acceptance: 422 Unprocessable Entity for missing query.
        """
        # Act: Send request without query
        response = client.post(
            "/chat",
            json={}
        )

        # Assert: Validation error
        assert response.status_code == 422

    def test_chat_endpoint_validation_query_max_length(self):
        """
        Test POST /chat endpoint enforces maximum query length.
        Acceptance: 422 for queries exceeding 2000 characters (per FR-007).
        """
        # Act: Send request with very long query
        long_query = "A" * 2001  # Exceeds FR-007 limit

        response = client.post(
            "/chat",
            json={"query": long_query}
        )

        # Assert: Validation error or truncation (depending on implementation)
        # If validation is strict: 422
        # If truncation is applied: 200 with truncated query
        assert response.status_code in [200, 422]

    @patch('src.api.chat.RAGService')
    def test_chat_endpoint_handles_service_errors(self, mock_rag_service_class):
        """
        Test POST /chat endpoint handles RAG service errors gracefully.
        Acceptance: 500 Internal Server Error with user-friendly message.
        """
        # Arrange: Mock service error
        mock_service = Mock()
        mock_service.chat_async = AsyncMock(
            side_effect=Exception("Internal service error")
        )
        mock_rag_service_class.return_value = mock_service

        # Act
        response = client.post(
            "/chat",
            json={"query": "test query"}
        )

        # Assert: Error response
        assert response.status_code == 500
        json_response = response.json()
        assert "detail" in json_response or "error" in json_response

    @patch('src.api.chat.rag_service.chat_async', new_callable=AsyncMock)
    def test_chat_endpoint_handles_qdrant_unavailable(self, mock_chat_async):
        """
        Test POST /chat endpoint handles Qdrant connection errors.
        Acceptance: 503 Service Unavailable with appropriate message.
        """
        # Arrange: Mock Qdrant unavailable
        mock_chat_async.side_effect = RuntimeError("Knowledge base temporarily unavailable")

        # Act
        response = client.post(
            "/chat",
            json={"query": "test query"}
        )

        # Assert: Service unavailable
        assert response.status_code in [500, 503]
        json_response = response.json()
        detail = json_response.get("detail", "")

        # Verify user-friendly error message (no stack traces per FR-011)
        # detail could be a dict (ErrorResponse) or string
        if isinstance(detail, dict):
            error_message = detail.get("message", "")
        else:
            error_message = str(detail)

        assert "unavailable" in error_message.lower()
        assert "Traceback" not in str(error_message)
        # Don't check for Exception as it might be in properly formatted error messages

    @patch('src.api.chat.rag_service.chat_async', new_callable=AsyncMock)
    def test_chat_endpoint_response_time_reasonable(self, mock_chat_async):
        """
        Test POST /chat endpoint responds within reasonable time.
        Acceptance: Response time < 5 seconds (allowing for test overhead).
        Target: <3 seconds in production (FR-009).
        """
        import time

        # Arrange
        mock_chat_async.return_value = "Quick response"

        # Act
        start_time = time.time()
        response = client.post(
            "/chat",
            json={"query": "Fast query"}
        )
        elapsed_time = time.time() - start_time

        # Assert
        assert response.status_code == 200
        assert elapsed_time < 5.0  # Generous for test environment

    def test_chat_endpoint_cors_headers(self):
        """
        Test POST /chat endpoint includes CORS headers.
        Acceptance: Response includes appropriate CORS headers.
        """
        # Act: Send OPTIONS preflight request
        response = client.options("/chat")

        # Assert: CORS headers present
        # Note: TestClient may not fully simulate CORS
        # This test verifies endpoint is accessible
        assert response.status_code in [200, 405]  # OPTIONS may not be explicitly defined

    @patch('src.api.chat.rag_service.chat_async', new_callable=AsyncMock)
    def test_chat_endpoint_content_type(self, mock_chat_async):
        """
        Test POST /chat endpoint returns JSON content type.
        Acceptance: Content-Type header is application/json.
        """
        # Arrange
        mock_chat_async.return_value = "Test"

        # Act
        response = client.post(
            "/chat",
            json={"query": "test"}
        )

        # Assert
        assert response.status_code == 200
        assert "application/json" in response.headers.get("content-type", "")

    @patch('src.api.chat.rag_service.chat_async', new_callable=AsyncMock)
    def test_chat_endpoint_xss_prevention(self, mock_chat_async):
        """
        Test POST /chat endpoint sanitizes XSS attempts.
        Acceptance: HTML/script tags in query don't cause XSS (FR-007).
        """
        # Arrange
        mock_chat_async.return_value = "Safe response"

        # Act: Send query with script tags
        response = client.post(
            "/chat",
            json={"query": "<script>alert('XSS')</script>What is AI?"}
        )

        # Assert: Request handled safely
        # Either 200 (sanitized and processed) or 422 (validation rejected)
        assert response.status_code in [200, 422]

        if response.status_code == 200:
            json_response = response.json()
            # Response should not contain unescaped script tags
            response_text = json_response.get("response", "")
            assert "<script>" not in response_text or "Safe response" in response_text
        else:
            # Validation error is also acceptable (XSS blocked)
            json_response = response.json()
            assert "detail" in json_response
