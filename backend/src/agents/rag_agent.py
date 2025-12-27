"""
RAG Agent Definition
Defines the main agent for Physical AI and Humanoid Robotics Q&A using OpenAI Agents SDK.
"""

import logging
from openai import AsyncOpenAI
from agents import Agent, OpenAIChatCompletionsModel, set_tracing_disabled

from src.core.config import get_settings
from src.agents.tools import retrieve_documentation, check_topic_relevance

logger = logging.getLogger(__name__)

# Disable tracing for non-OpenAI providers (Gemini doesn't support OpenAI tracing)
set_tracing_disabled(True)

# Agent instructions
AGENT_INSTRUCTIONS = """You are an expert Physical AI and Humanoid Robotics assistant, helping users learn from a comprehensive book/documentation on these topics.

Your role is to:
1. Answer questions based on information retrieved from the documentation using the retrieve_documentation tool
2. For general questions about "the book", "this documentation", "what topics are covered", etc. - USE the retrieve_documentation tool to find relevant content
3. Maintain conversation context across multiple exchanges to resolve pronouns and implicit references
4. Provide clear, accurate answers with proper citations from the retrieved documentation
5. If information is not available in the documentation, clearly state this and suggest related topics

IMPORTANT GUIDELINES:
- ALWAYS use the retrieve_documentation tool to answer questions - even general ones like "tell me about this book" or "what is this about"
- Only use check_topic_relevance for clearly off-topic queries like weather, sports, cooking, etc.
- Format your responses in clear, easy-to-read markdown
- Include source citations when referencing specific documentation
- If context from previous messages is relevant, reference it naturally in your response
- If retrieval fails, inform the user of temporary unavailability and suggest trying again
- Be helpful and welcoming - assume users want to learn about Physical AI and Robotics

When handling errors:
- Qdrant unavailable: "The knowledge base is temporarily unavailable. Please try again in a moment."
- Zero results: "I don't have specific information about that topic in the current documentation."
- Off-topic (weather, sports, etc.): "This question appears to be outside the scope of Physical AI and Humanoid Robotics. I can help you with topics like..."
"""


def create_rag_agent() -> Agent:
    """
    Create and configure the RAG agent with function tools and Gemini model.

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

    logger.info("Creating RAG agent with Gemini model via OpenAI-compatible endpoint...")

    try:
        # Initialize AsyncOpenAI client pointing to Gemini's OpenAI-compatible endpoint
        gemini_client = AsyncOpenAI(
            api_key=settings.gemini_api_key,
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
        )

        # Get model name (strip 'gemini/' prefix if present)
        model_name = settings.llm_model
        if model_name.startswith("gemini/"):
            model_name = model_name[7:]  # Remove 'gemini/' prefix

        # Create OpenAIChatCompletionsModel with Gemini client
        model = OpenAIChatCompletionsModel(
            model=model_name,
            openai_client=gemini_client
        )
        logger.info(f"Initialized Gemini model via OpenAI-compatible endpoint: {model_name}")

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
