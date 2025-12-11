from fastapi import APIRouter, HTTPException
from backend.src.models.chat import ChatRequest
from backend.src.services.rag_service import RAGService
import logging
import re

router = APIRouter()
rag_service = RAGService() # Instantiate RAGService globally for reusability

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def is_off_topic_query(query: str) -> bool:
    """
    Checks if the query is off-topic based on the spec requirements.
    Returns True if the query is off-topic, False otherwise.
    """
    # Define patterns for off-topic queries
    off_topic_patterns = [
        r'joke|funny|tell me a|humor',
        r'personal opinion|your opinion|what do you think',
        r'weather|news|sports|entertainment|gossip',
        r'personal|private|secret|confidential',
        r'offensive|inappropriate|invasive|private information',
        r'non-book related|not robotics|not AI|not humanoid',
    ]

    query_lower = query.lower()
    for pattern in off_topic_patterns:
        if re.search(pattern, query_lower):
            return True

    return False

@router.post("/chat")
async def chat_endpoint(request: ChatRequest):
    """
    Handles chat requests from the frontend, processing them using the RAG service.
    Includes error handling for unavailable APIs and off-topic queries.
    """
    try:
        # Check if the query is off-topic
        if is_off_topic_query(request.query):
            logger.info(f"Off-topic query detected: {request.query}")
            return {
                "response": "I can only answer questions about the Physical AI and Humanoid Robotics book content. Please ask a question related to robotics, AI, or the topics covered in the book."
            }

        # Attempt to get response from RAG service
        response = rag_service.chat(request.query)

        # Check if response indicates API unavailability
        if "unavailable" in response.lower() or "error" in response.lower():
            logger.warning(f"RAG service returned error response for query: {request.query}")
            return {
                "response": "The chatbot is currently unavailable. Please try again later."
            }

        return {"response": response}

    except Exception as e:
        logger.error(f"Error processing chat request: {str(e)}")
        # Log the full exception for debugging
        import traceback
        logger.error(f"Full traceback: {traceback.format_exc()}")

        # Return a user-friendly error message
        return {
            "response": "The chatbot is currently unavailable. Please try again later."
        }