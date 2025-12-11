from pydantic import BaseModel
from typing import Optional

class ChatRequest(BaseModel):
    """
    Request model for a user query to the chatbot.
    """
    query: str
    session_id: Optional[str] = None # For tracking conversation history in the future