"""
RAG Agent Definition
Defines the main agent for Physical AI and Humanoid Robotics Q&A using OpenAI Agents SDK.
"""

import logging
import os
from agents import Agent
from agents.extensions.models.litellm_model import LitellmModel

from src.core.config import get_settings
from src.agents.tools import retrieve_documentation, check_topic_relevance

logger = logging.getLogger(__name__)

# Agent instructions
AGENT_INSTRUCTIONS = """You are an expert Physical AI and Humanoid Robotics assistant.

Your role is to:
1. Answer questions ONLY based on information retrieved from the documentation using the retrieve_documentation tool
2. Always check topic relevance before retrieving documentation using the check_topic_relevance tool
3. Maintain conversation context across multiple exchanges to resolve pronouns and implicit references
4. Provide clear, accurate answers with proper citations from the retrieved documentation
5. If information is not available in the documentation, clearly state this and suggest related topics

IMPORTANT GUIDELINES:
- Always use the retrieve_documentation tool before answering technical questions
- For off-topic queries, politely redirect users to Physical AI and Robotics topics
- Format your responses in clear, easy-to-read markdown
- Include source citations when referencing specific documentation
- If context from previous messages is relevant, reference it naturally in your response
- If retrieval fails, inform the user of temporary unavailability and suggest trying again

When handling errors:
- Qdrant unavailable: "The knowledge base is temporarily unavailable. Please try again in a moment."
- Zero results: "I don't have specific information about that topic in the current documentation."
- Off-topic: "This question appears to be outside the scope of Physical AI and Humanoid Robotics. I can help you with topics like..."
"""


def create_rag_agent() -> Agent:
    """
    Create and configure the RAG agent with function tools and LiteLLM model.

    Returns:
        Agent: Configured agent instance ready for use with Runner

    Raises:
        ValueError: If required environment variables are missing
        Exception: If agent initialization fails

    Examples:
        >>> agent = create_rag_agent()
        >>> from agents import Runner, SQLiteSession
        >>> session = SQLiteSession("user_123", "conversations.db")
        >>> result = await Runner.run(agent, "What is Physical AI?", session=session)
    """
    settings = get_settings()

    # Validate required settings
    if not settings.gemini_api_key:
        raise ValueError("GEMINI_API_KEY environment variable is required")

    logger.info("Creating RAG agent with LiteLLM Gemini model...")

    try:
        # Initialize LiteLLM model for Gemini
        model = LitellmModel(
            model=settings.llm_model,  # "gemini/gemini-2.0-flash"
            api_key=settings.gemini_api_key
        )
        logger.info(f"Initialized LiteLLM model: {settings.llm_model}")

        # Create agent with tools
        agent = Agent(
            name="Physical AI and Robotics Expert",
            instructions=AGENT_INSTRUCTIONS,
            model=model,
            tools=[check_topic_relevance, retrieve_documentation]
        )

        logger.info("RAG agent created successfully with tools: check_topic_relevance, retrieve_documentation")
        return agent

    except Exception as e:
        logger.error(f"Failed to create RAG agent: {str(e)}", exc_info=True)
        raise


# Global agent instance (created lazily)
_agent_instance = None


def get_rag_agent() -> Agent:
    """
    Get or create the global RAG agent instance.

    Returns:
        Agent: The global RAG agent instance

    Examples:
        >>> agent = get_rag_agent()
    """
    global _agent_instance
    if _agent_instance is None:
        _agent_instance = create_rag_agent()
    return _agent_instance
