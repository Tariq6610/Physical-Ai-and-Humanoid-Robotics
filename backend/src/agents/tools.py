"""
Agent Function Tools
Defines function tools that can be called by the RAG agent.
"""

import logging
from typing import List, Dict
from agents import function_tool
from qdrant_client import QdrantClient

from src.core.config import get_settings
from src.services.embeddings import get_embedding_service

logger = logging.getLogger(__name__)

# Initialize Qdrant client (shared across tool calls)
_qdrant_client = None


def get_qdrant_client() -> QdrantClient:
    """Get or create the Qdrant client instance."""
    global _qdrant_client
    if _qdrant_client is None:
        settings = get_settings()
        if settings.qdrant_api_key:
            _qdrant_client = QdrantClient(
                url=settings.qdrant_url,
                api_key=settings.qdrant_api_key,
                timeout=10
            )
            logger.info(f"Initialized Qdrant client with URL: {settings.qdrant_url}")
        else:
            _qdrant_client = QdrantClient(host="localhost", port=6333, timeout=10)
            logger.info("Initialized Qdrant client for local development")
    return _qdrant_client


@function_tool
def retrieve_documentation(query: str, top_k: int = 5) -> str:
    """
    Retrieve relevant Physical AI and Humanoid Robotics documentation chunks from the knowledge base.

    This tool searches the vector database for documentation most relevant to the user's query.
    Use this tool whenever you need specific information from the documentation to answer a question.

    Args:
        query: The user's question or search query
        top_k: Number of most relevant documentation chunks to retrieve (default: 5, max: 10)

    Returns:
        str: Formatted context string with source citations, or error message if retrieval fails

    Examples:
        >>> retrieve_documentation("What is Physical AI?", top_k=3)
        >>> retrieve_documentation("How do humanoid robots use sensors?")
    """
    settings = get_settings()
    embedding_service = get_embedding_service()
    qdrant_client = get_qdrant_client()

    # Validate and limit top_k
    top_k = min(max(1, top_k), 10)

    logger.info(f"Retrieving documentation for query: '{query[:50]}...' (top_k={top_k})")

    try:
        # Generate query embedding
        logger.debug("Generating query embedding...")
        query_vector = embedding_service.encode(query)
        logger.debug(f"Generated embedding vector of length {len(query_vector)}")

        # Search Qdrant for similar documents
        logger.debug(f"Searching Qdrant collection '{settings.qdrant_collection_name}'...")
        search_results = qdrant_client.query_points(
            collection_name=settings.qdrant_collection_name,
            query=query_vector,
            limit=top_k,
            score_threshold=settings.similarity_threshold,
        ).points

        if not search_results:
            logger.warning(f"No relevant documentation found for query: '{query[:50]}...'")
            return "No relevant documentation found for your query. Please try rephrasing your question or ask about a different topic related to Physical AI and Humanoid Robotics."

        # Format results with citations
        formatted_chunks = []
        for i, result in enumerate(search_results, 1):
            source_url = result.payload.get("source", "Unknown source")
            text_content = result.payload.get("text", "")
            relevance_score = result.score

            # Format each chunk with clear delimiters
            chunk_text = f"""--- Document {i} (Relevance: {relevance_score:.2f}) ---
Source: {source_url}
Content: {text_content}
"""
            formatted_chunks.append(chunk_text)

        formatted_context = "\n".join(formatted_chunks)
        logger.info(f"Successfully retrieved {len(search_results)} documentation chunks")
        return formatted_context

    except ConnectionError as e:
        error_msg = "Knowledge base temporarily unavailable. Please try again in a moment."
        logger.error(f"Qdrant connection error: {str(e)}", exc_info=True)
        raise RuntimeError(error_msg)

    except TimeoutError as e:
        error_msg = "Search is taking longer than expected. Please try a more specific query."
        logger.error(f"Qdrant timeout error: {str(e)}", exc_info=True)
        raise RuntimeError(error_msg)

    except Exception as e:
        error_msg = f"Documentation retrieval failed: {str(e)}"
        logger.error(f"Unexpected error during documentation retrieval: {str(e)}", exc_info=True)
        raise RuntimeError(error_msg)


@function_tool
def check_topic_relevance(query: str) -> dict:
    """
    Check if the user's query is related to Physical AI and Humanoid Robotics.

    This tool helps filter out off-topic questions and guide users back to relevant topics.
    Use this tool before retrieving documentation to ensure the query is within scope.

    Args:
        query: The user's question to check for relevance

    Returns:
        dict: Dictionary with keys:
            - relevant (bool): Whether the query is on-topic
            - reason (str): Explanation of the relevance decision
            - suggested_topics (List[str]): Suggested topics if off-topic

    Examples:
        >>> check_topic_relevance("What is a humanoid robot?")
        {'relevant': True, 'reason': 'Query matches domain keywords', 'suggested_topics': []}
        >>> check_topic_relevance("What's the weather today?")
        {'relevant': False, 'reason': 'Query off-topic', 'suggested_topics': [...]}
    """
    logger.info(f"Checking topic relevance for query: '{query[:50]}...'")

    # Domain-specific keywords
    domain_keywords = [
        "robot", "robotic", "humanoid", "ai", "artificial intelligence",
        "physical ai", "sensor", "actuator", "motor", "servo",
        "ros", "isaac", "simulation", "gazebo", "nvidia", "omniverse",
        "navigation", "manipulation", "perception", "locomotion",
        "kinematics", "dynamics", "control", "vision", "lidar",
        "gripper", "end effector", "joint", "torque", "trajectory"
    ]

    query_lower = query.lower()

    # Check for keyword matches
    is_relevant = any(keyword in query_lower for keyword in domain_keywords)

    # Suggested topics for off-topic queries
    suggested_topics = [
        "Humanoid robot design and components",
        "Physical AI concepts and applications",
        "Robot sensors and perception systems",
        "Robot actuation and control",
        "ROS (Robot Operating System)",
        "Simulation environments (Isaac Sim, Gazebo)"
    ]

    result = {
        "relevant": is_relevant,
        "reason": "Query matches domain keywords" if is_relevant else "Query appears to be off-topic",
        "suggested_topics": [] if is_relevant else suggested_topics
    }

    logger.info(f"Topic relevance check result: {result['relevant']}")
    return result
