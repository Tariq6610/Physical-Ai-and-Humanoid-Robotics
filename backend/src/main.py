from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from .api import chat as chat_api # Import the chat router
from .core.config import get_settings

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)

app = FastAPI(title="Physical AI and Humanoid Robotics Backend")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Get settings for CORS configuration
settings = get_settings()

# Add CORS middleware to allow requests from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        settings.frontend_url,  # Production frontend URL
        "http://localhost:3000",  # Local development
        "https://physical-ai-robotics-docs.onrender.com"  # Explicit production URL
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the chat router
app.include_router(chat_api.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Physical AI and Humanoid Robotics Backend!"}


@app.get("/health")
async def health_check():
    """
    Health check endpoint to verify the service is running and healthy.
    Returns status information about the API.
    """
    import datetime
    return {
        "status": "healthy",
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "service": "Physical AI and Humanoid Robotics RAG API",
        "version": "1.0.0"
    }