import os
import pytest
from unittest.mock import MagicMock, patch
from src.services.rag_service import RAGService, MockQdrantClient, MockSentenceTransformer, MockLLMClient

# Fixture to provide a RAGService instance with mocked dependencies
@pytest.fixture
def rag_service_mocked():
    with patch('src.services.rag_service.MockQdrantClient') as MockQdrant:
        with patch('src.services.rag_service.MockSentenceTransformer') as MockEncoder:
            with patch('src.services.rag_service.MockLLMClient') as MockLLM:
                # Configure mocks
                MockQdrant.return_value.search.return_value = [
                    {"id": "doc1", "payload": {"text": "ROS 2 is a flexible framework.", "source": "ros_ch1.md", "section": "Intro"}},
                    {"id": "doc2", "payload": {"text": "Nodes communicate via topics.", "source": "ros_ch2.md", "section": "Nodes"}}
                ]
                MockEncoder.return_value.encode.return_value = [0.1] * 384
                MockLLM.return_value.generate_response.return_value = "Mocked LLM response about ROS 2."

                service = RAGService()
                service.qdrant_client = MockQdrant.return_value
                service.embedding_model = MockEncoder.return_value
                service.llm_client = MockLLM.return_value
                yield service

def test_rag_service_initialization(rag_service_mocked):
    # Test that the service initializes its components
    assert rag_service_mocked.qdrant_client is not None
    assert rag_service_mocked.embedding_model is not None
    assert rag_service_mocked.llm_client is not None
    assert rag_service_mocked.collection_name == os.getenv("QDRANT_COLLECTION_NAME", "book_content")

def test_get_query_embedding(rag_service_mocked):
    query = "What is ROS 2?"
    embedding = rag_service_mocked.get_query_embedding(query)
    rag_service_mocked.embedding_model.encode.assert_called_once_with(query)
    assert len(embedding) == 384 # Assuming all-MiniLM-L6-v2 dimension

def test_retrieve_context(rag_service_mocked):
    query_embedding = [0.1] * 384
    context = rag_service_mocked.retrieve_context(query_embedding)
    rag_service_mocked.qdrant_client.search.assert_called_once_with(
        collection_name=rag_service_mocked.collection_name,
        query_vector=query_embedding,
        limit=5
    )
    assert len(context) == 2
    assert "ROS 2 is a flexible framework." in context[0]["payload"]["text"]

def test_generate_answer(rag_service_mocked):
    query = "How do ROS 2 nodes communicate?"
    context_data = [
        {"id": "doc1", "payload": {"text": "ROS 2 is a flexible framework.", "source": "ros_ch1.md", "section": "Intro"}},
        {"id": "doc2", "payload": {"text": "Nodes communicate via topics.", "source": "ros_ch2.md", "section": "Nodes"}}
    ]
    answer = rag_service_mocked.generate_answer(query, context_data)
    
    expected_prompt_part = "Context:\nROS 2 is a flexible framework.\nNodes communicate via topics.\n\nQuestion: How do ROS 2 nodes communicate?\nAnswer:"
    
    rag_service_mocked.llm_client.generate_response.assert_called_once()
    actual_prompt_arg = rag_service_mocked.llm_client.generate_response.call_args[0][0]
    
    assert expected_prompt_part in actual_prompt_arg
    assert answer == "Mocked LLM response about ROS 2."

def test_chat_method(rag_service_mocked):
    query = "Tell me about ROS 2."
    response = rag_service_mocked.chat(query)

    rag_service_mocked.embedding_model.encode.assert_called_once_with(query)
    rag_service_mocked.qdrant_client.search.assert_called_once()
    rag_service_mocked.llm_client.generate_response.assert_called_once()
    assert response == "Mocked LLM response about ROS 2."
