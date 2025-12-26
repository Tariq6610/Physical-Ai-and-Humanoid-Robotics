from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from ..models.chat import ChatRequest
from ..services.rag_service import RAGService
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import logging
import re
import os
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from pydantic import BaseModel

# Error response models
class ErrorResponse(BaseModel):
    error: str
    error_code: str
    message: str
    timestamp: str
    request_id: Optional[str] = None

class ValidationErrorResponse(BaseModel):
    error: str
    error_code: str
    message: str
    details: list
    timestamp: str
    request_id: Optional[str] = None

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)
router = APIRouter()

rag_service = RAGService() # Instantiate RAGService globally for reusability

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Security scheme
security = HTTPBearer()

# JWT configuration
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify JWT token from Authorization header."""
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=401,
                detail="Could not validate credentials"
            )
        return user_id
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials"
        )

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@router.post("/token")
async def login():
    """Generate a token for testing purposes. In production, this would be a proper login endpoint."""
    user_id = "test_user"  # This would come from actual authentication
    access_token = create_access_token(data={"sub": user_id})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/api/chatkit/session")
async def create_chatkit_session():
    """
    Create a ChatKit session with client_secret for frontend authentication.

    This endpoint is called by ChatKit's getClientSecret callback to establish
    a session between the frontend and backend.

    Returns:
        dict: Contains client_secret (JWT token) and session_id
    """
    import uuid

    # Generate unique session ID
    session_id = str(uuid.uuid4())

    # Create JWT token with session_id
    # ChatKit uses this as the client_secret
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    client_secret = create_access_token(
        data={"sub": session_id, "type": "chatkit_session"},
        expires_delta=access_token_expires
    )

    logger.info(f"Created ChatKit session: {session_id}")

    return {
        "client_secret": client_secret,
        "session_id": session_id
    }

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
@limiter.limit("100/hour")  # Rate limit: 100 requests per hour per IP
async def chat_endpoint(request: Request, chat_request: ChatRequest):
    """
    Handles chat requests from the frontend, processing them using the RAG service.
    Includes error handling for unavailable APIs and off-topic queries.
    Supports session management for conversation history.
    """
    from uuid import uuid4
    request_id = str(uuid4())

    try:
        # Extract session_id from request (query param, header, or generate new)
        session_id = request.query_params.get("session_id")
        if not session_id:
            session_id = request.headers.get("X-Session-ID")
        if not session_id:
            session_id = str(uuid4())
            logger.info(f"Generated new session_id: {session_id}")
        else:
            logger.info(f"Using existing session_id: {session_id}")

        # Check if the query is off-topic (now handled by agent, but kept for backwards compatibility)
        if is_off_topic_query(chat_request.query):
            logger.info(f"Off-topic query detected: {chat_request.query}, request_id: {request_id}")
            return {
                "response": "I can only answer questions about the Physical AI and Humanoid Robotics book content. Please ask a question related to robotics, AI, or the topics covered in the book.",
                "request_id": request_id,
                "session_id": session_id
            }

        # Attempt to get response from RAG service with session management
        response = await rag_service.chat_async(chat_request.query, session_id=session_id)

        # Check if response indicates API unavailability
        if "unavailable" in response.lower() or "error" in response.lower():
            logger.warning(f"RAG service returned error response for query: {chat_request.query}, request_id: {request_id}")
            error_response = ErrorResponse(
                error="Service Unavailable",
                error_code="RAG_SERVICE_ERROR",
                message="The chatbot is currently unavailable. Please try again later.",
                timestamp=datetime.utcnow().isoformat(),
                request_id=request_id
            )
            raise HTTPException(status_code=503, detail=error_response.dict())

        return {"response": response, "request_id": request_id, "session_id": session_id}

    except RateLimitExceeded:
        logger.warning(f"Rate limit exceeded for IP: {request.client.host}, request_id: {request_id}")
        error_response = ErrorResponse(
            error="Rate Limit Exceeded",
            error_code="RATE_LIMIT_EXCEEDED",
            message="Rate limit exceeded. Please try again later.",
            timestamp=datetime.utcnow().isoformat(),
            request_id=request_id
        )
        raise HTTPException(status_code=429, detail=error_response.dict())
    except HTTPException:
        # Re-raise HTTP exceptions to maintain proper status codes
        raise
    except ValueError as ve:
        # Handle validation errors from the model
        error_response = ValidationErrorResponse(
            error="Validation Error",
            error_code="VALIDATION_ERROR",
            message=str(ve),
            details=[{"field": "query", "error": str(ve)}],
            timestamp=datetime.utcnow().isoformat(),
            request_id=request_id
        )
        logger.warning(f"Validation error for request_id: {request_id}, error: {str(ve)}")
        raise HTTPException(status_code=422, detail=error_response.dict())
    except Exception as e:
        logger.error(f"Error processing chat request: {str(e)}, request_id: {request_id}")
        # Log the full exception for debugging
        import traceback
        logger.error(f"Full traceback: {traceback.format_exc()}")

        # Return a user-friendly error message with proper HTTP status
        error_response = ErrorResponse(
            error="Internal Server Error",
            error_code="INTERNAL_ERROR",
            message="The chatbot is currently unavailable. Please try again later.",
            timestamp=datetime.utcnow().isoformat(),
            request_id=request_id
        )
        raise HTTPException(status_code=500, detail=error_response.dict())