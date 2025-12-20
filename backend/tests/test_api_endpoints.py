import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from src.api.chat import router
from src.models.chat import ChatRequest
from main import app  # Assuming the main app is in main.py


def test_chat_endpoint_success():
    """
    Test that the chat endpoint returns a successful response with a mock RAG service.
    """
    client = TestClient(app)

    # Mock the RAG service
    with patch('src.api.chat.rag_service') as mock_rag_service:
        mock_rag_service.chat.return_value = "This is a test response for the query."

        # Send a test request
        response = client.post("/chat", json={"query": "What is ROS 2?"})

        # Check response status
        assert response.status_code == 200

        # Check response content
        assert "response" in response.json()
        assert response.json()["response"] == "This is a test response for the query."


def test_chat_endpoint_off_topic_query():
    """
    Test that the chat endpoint properly handles off-topic queries.
    """
    client = TestClient(app)

    # Send an off-topic query
    response = client.post("/chat", json={"query": "Tell me a joke"})

    # Check response status
    assert response.status_code == 200

    # Check that the response indicates the query was off-topic
    assert "response" in response.json()
    response_text = response.json()["response"]
    assert "only answer questions about the Physical AI and Humanoid Robotics book content" in response_text


def test_chat_endpoint_empty_query():
    """
    Test that the chat endpoint handles empty queries gracefully.
    """
    client = TestClient(app)

    # Send an empty query
    response = client.post("/chat", json={"query": ""})

    # Check response status - should still be 200 but with appropriate response
    assert response.status_code == 200


def test_chat_endpoint_error_handling():
    """
    Test that the chat endpoint handles errors gracefully.
    """
    client = TestClient(app)

    # Mock the RAG service to raise an exception
    with patch('src.api.chat.rag_service') as mock_rag_service:
        mock_rag_service.chat.side_effect = Exception("Mocked error")

        # Send a test request
        response = client.post("/chat", json={"query": "What causes errors?"})

        # Check response status
        assert response.status_code == 200  # Should still return 200 with error message

        # Check that the response indicates the service is unavailable
        assert "response" in response.json()
        response_text = response.json()["response"]
        assert "currently unavailable" in response_text


def test_chat_request_model_validation():
    """
    Test that the ChatRequest model properly validates inputs.
    """
    # Test valid request
    valid_request = ChatRequest(query="What is a node in ROS 2?")
    assert valid_request.query == "What is a node in ROS 2?"

    # Test request with session_id
    request_with_session = ChatRequest(query="How do nodes communicate?", session_id="session_123")
    assert request_with_session.session_id == "session_123"


def test_off_topic_query_detection():
    """
    Test the off-topic query detection function with various inputs.
    """
    from src.api.chat import is_off_topic_query

    # Test off-topic queries
    off_topic_queries = [
        "Tell me a joke",
        "What do you think about politics?",
        "How's the weather today?",
        "Can you keep a secret?",
        "Say something offensive"
    ]

    for query in off_topic_queries:
        assert is_off_topic_query(query) == True, f"Query '{query}' should be detected as off-topic"

    # Test on-topic queries
    on_topic_queries = [
        "What is ROS 2?",
        "How do nodes communicate?",
        "Explain humanoid robotics",
        "What is Qdrant?"
    ]

    for query in on_topic_queries:
        assert is_off_topic_query(query) == False, f"Query '{query}' should not be detected as off-topic"


def test_api_response_format():
    """
    Test that the API consistently returns responses in the expected format.
    """
    client = TestClient(app)

    with patch('src.api.chat.rag_service') as mock_rag_service:
        mock_rag_service.chat.return_value = "Test response content"

        response = client.post("/chat", json={"query": "Test query"})

        # Check that response has the correct structure
        json_response = response.json()
        assert isinstance(json_response, dict)
        assert "response" in json_response
        assert isinstance(json_response["response"], str)


if __name__ == "__main__":
    pytest.main([__file__])