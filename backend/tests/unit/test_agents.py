"""
Unit tests for Agent tools and functionality.
Tests for retrieve_documentation, check_topic_relevance, and RAG agent initialization.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from agents import Agent

import src.agents.tools as tools_module
from src.agents.tools import retrieve_documentation, check_topic_relevance
from src.agents.rag_agent import create_rag_agent, get_rag_agent


class TestRetrieveDocumentation:
    """Test suite for retrieve_documentation function tool."""

    @patch('src.agents.tools.get_qdrant_client')
    @patch('src.agents.tools.get_embedding_service')
    def test_retrieve_documentation_success(self, mock_embedding_service, mock_qdrant_client):
        """
        T010: Test retrieve_documentation returns formatted context with citations.
        Acceptance: Function returns formatted string with sources and relevance scores.
        """
        # Arrange: Mock Qdrant response
        mock_embedding = Mock()
        mock_embedding.encode.return_value = [0.1] * 384  # 384-dimensional vector
        mock_embedding_service.return_value = mock_embedding

        mock_point = Mock()
        mock_point.score = 0.85
        mock_point.payload = {
            "text": "Physical AI combines artificial intelligence with physical systems.",
            "source": "https://docs.example.com/physical-ai"
        }

        mock_result = Mock()
        mock_result.points = [mock_point]

        mock_client = Mock()
        mock_client.query_points.return_value = mock_result
        mock_qdrant_client.return_value = mock_client

        # Act
        result = retrieve_documentation("What is Physical AI?", top_k=1)

        # Assert
        assert isinstance(result, str)
        assert "Document 1" in result
        assert "Relevance: 0.85" in result
        assert "https://docs.example.com/physical-ai" in result
        assert "Physical AI combines" in result
        mock_client.query_points.assert_called_once()

    @patch('src.agents.tools.get_qdrant_client')
    @patch('src.agents.tools.get_embedding_service')
    def test_retrieve_documentation_empty_results(self, mock_embedding_service, mock_qdrant_client):
        """
        Test retrieve_documentation handles zero results gracefully.
        Acceptance: Returns user-friendly message when no relevant docs found.
        """
        # Arrange: Mock empty Qdrant response
        mock_embedding = Mock()
        mock_embedding.encode.return_value = [0.1] * 384
        mock_embedding_service.return_value = mock_embedding

        mock_result = Mock()
        mock_result.points = []  # Empty results

        mock_client = Mock()
        mock_client.query_points.return_value = mock_result
        mock_qdrant_client.return_value = mock_client

        # Act
        result = retrieve_documentation("obscure unrelated query")

        # Assert
        assert "No relevant documentation found" in result
        assert "try rephrasing" in result.lower() or "different topic" in result.lower()

    @patch('src.agents.tools.get_qdrant_client')
    @patch('src.agents.tools.get_embedding_service')
    def test_retrieve_documentation_connection_error(self, mock_embedding_service, mock_qdrant_client):
        """
        Test retrieve_documentation handles Qdrant connection failures.
        Acceptance: Raises RuntimeError with user-friendly message.
        """
        # Arrange: Mock connection error
        mock_embedding = Mock()
        mock_embedding.encode.return_value = [0.1] * 384
        mock_embedding_service.return_value = mock_embedding

        mock_client = Mock()
        mock_client.query_points.side_effect = ConnectionError("Cannot connect to Qdrant")
        mock_qdrant_client.return_value = mock_client

        # Act & Assert
        with pytest.raises(RuntimeError) as exc_info:
            retrieve_documentation("test query")

        assert "Knowledge base temporarily unavailable" in str(exc_info.value)

    @patch('src.agents.tools.get_qdrant_client')
    @patch('src.agents.tools.get_embedding_service')
    def test_retrieve_documentation_timeout_error(self, mock_embedding_service, mock_qdrant_client):
        """
        Test retrieve_documentation handles timeout errors.
        Acceptance: Raises RuntimeError with timeout-specific message.
        """
        # Arrange: Mock timeout
        mock_embedding = Mock()
        mock_embedding.encode.return_value = [0.1] * 384
        mock_embedding_service.return_value = mock_embedding

        mock_client = Mock()
        mock_client.query_points.side_effect = TimeoutError("Request timed out")
        mock_qdrant_client.return_value = mock_client

        # Act & Assert
        with pytest.raises(RuntimeError) as exc_info:
            retrieve_documentation("test query")

        assert "taking longer than expected" in str(exc_info.value)

    def test_retrieve_documentation_top_k_validation(self):
        """
        Test retrieve_documentation validates and limits top_k parameter.
        Acceptance: top_k clamped to valid range [1, 10].
        """
        with patch('src.agents.tools.get_qdrant_client') as mock_qdrant, \
             patch('src.agents.tools.get_embedding_service') as mock_embedding:

            mock_emb = Mock()
            mock_emb.encode.return_value = [0.1] * 384
            mock_embedding.return_value = mock_emb

            mock_result = Mock()
            mock_result.points = []
            mock_client = Mock()
            mock_client.query_points.return_value = mock_result
            mock_qdrant.return_value = mock_client

            # Test upper bound
            retrieve_documentation("test", top_k=100)
            call_args = mock_client.query_points.call_args
            assert call_args.kwargs['limit'] == 10

            # Test lower bound
            retrieve_documentation("test", top_k=0)
            call_args = mock_client.query_points.call_args
            assert call_args.kwargs['limit'] == 1


class TestCheckTopicRelevance:
    """Test suite for check_topic_relevance function tool."""

    def test_check_topic_relevance_on_topic(self):
        """
        Test check_topic_relevance identifies on-topic queries.
        Acceptance: Returns relevant=True for robotics/AI queries.
        """
        # Test various on-topic queries
        queries = [
            "What is a humanoid robot?",
            "How do robots use sensors?",
            "Explain Physical AI",
            "What is ROS?",
            "How does Isaac Sim work?"
        ]

        for query in queries:
            result = check_topic_relevance(query)
            assert result["relevant"] is True
            assert "domain keywords" in result["reason"].lower()
            assert result["suggested_topics"] == []

    def test_check_topic_relevance_off_topic(self):
        """
        Test check_topic_relevance identifies off-topic queries.
        Acceptance: Returns relevant=False with suggested topics.
        """
        # Test off-topic queries
        queries = [
            "What's the weather today?",
            "Tell me a joke",
            "How do I cook pasta?",
            "What is blockchain?"
        ]

        for query in queries:
            result = check_topic_relevance(query)
            assert result["relevant"] is False
            assert "off-topic" in result["reason"].lower()
            assert len(result["suggested_topics"]) > 0
            # Check suggested topics are robotics-related
            assert any("robot" in topic.lower() or "ai" in topic.lower()
                      for topic in result["suggested_topics"])

    def test_check_topic_relevance_borderline(self):
        """
        Test check_topic_relevance handles AI-adjacent topics correctly.
        Acceptance: AI-related queries marked as relevant.
        """
        # Borderline cases - should be relevant (AI-related)
        result = check_topic_relevance("How do AI systems learn?")
        assert result["relevant"] is True

        result = check_topic_relevance("What are neural networks?")
        assert result["relevant"] is True


class TestRAGAgent:
    """Test suite for RAG agent initialization and configuration."""

    @patch('src.agents.rag_agent.get_settings')
    @patch('src.agents.rag_agent.LitellmModel')
    @patch('src.agents.rag_agent.Agent')
    def test_create_rag_agent_success(self, mock_agent_class, mock_litellm_model, mock_get_settings):
        """
        T011: Test RAG agent initialization with correct configuration.
        Acceptance: Agent created with name, instructions, LiteLLM Gemini model, and tools.
        """
        # Arrange
        mock_settings = Mock()
        mock_settings.gemini_api_key = "test-api-key"
        mock_settings.llm_model = "gemini/gemini-2.5-flash"
        mock_get_settings.return_value = mock_settings

        mock_model = Mock()
        mock_litellm_model.return_value = mock_model

        mock_agent_instance = Mock()
        mock_agent_class.return_value = mock_agent_instance

        # Act
        agent = create_rag_agent()

        # Assert
        mock_litellm_model.assert_called_once_with(
            model="gemini/gemini-2.5-flash",
            api_key="test-api-key"
        )

        mock_agent_class.assert_called_once()
        call_kwargs = mock_agent_class.call_args.kwargs

        assert call_kwargs["name"] == "Physical AI and Robotics Expert"
        assert "Physical AI" in call_kwargs["instructions"]
        assert call_kwargs["model"] == mock_model
        assert len(call_kwargs["tools"]) == 2  # check_topic_relevance, retrieve_documentation

        assert agent == mock_agent_instance

    @patch('src.agents.rag_agent.get_settings')
    def test_create_rag_agent_missing_api_key(self, mock_get_settings):
        """
        Test RAG agent initialization fails without API key.
        Acceptance: Raises ValueError if GEMINI_API_KEY not set.
        """
        # Arrange
        mock_settings = Mock()
        mock_settings.gemini_api_key = None
        mock_get_settings.return_value = mock_settings

        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            create_rag_agent()

        assert "GEMINI_API_KEY" in str(exc_info.value)

    @patch('src.agents.rag_agent.get_settings')
    @patch('src.agents.rag_agent.LitellmModel')
    def test_create_rag_agent_model_initialization_error(self, mock_litellm_model, mock_get_settings):
        """
        Test RAG agent handles model initialization failures.
        Acceptance: Exception propagated with logging.
        """
        # Arrange
        mock_settings = Mock()
        mock_settings.gemini_api_key = "test-key"
        mock_settings.llm_model = "invalid-model"
        mock_get_settings.return_value = mock_settings

        mock_litellm_model.side_effect = Exception("Invalid model configuration")

        # Act & Assert
        with pytest.raises(Exception) as exc_info:
            create_rag_agent()

        assert "Invalid model configuration" in str(exc_info.value)

    @patch('src.agents.rag_agent.create_rag_agent')
    def test_get_rag_agent_singleton(self, mock_create_rag_agent):
        """
        Test get_rag_agent returns singleton instance.
        Acceptance: Agent created only once, same instance returned on subsequent calls.
        """
        # Arrange
        mock_agent = Mock()
        mock_create_rag_agent.return_value = mock_agent

        # Clear any existing instance
        from src.agents import rag_agent
        rag_agent._agent_instance = None

        # Act
        agent1 = get_rag_agent()
        agent2 = get_rag_agent()

        # Assert
        assert agent1 is agent2
        mock_create_rag_agent.assert_called_once()
