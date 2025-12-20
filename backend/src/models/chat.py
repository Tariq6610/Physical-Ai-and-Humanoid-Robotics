import re
from pydantic import BaseModel, validator
from typing import Optional

class ChatRequest(BaseModel):
    """
    Request model for a user query to the chatbot.
    """
    query: str
    session_id: Optional[str] = None  # For tracking conversation history in the future

    @validator('query')
    def validate_query(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError('Query cannot be empty or whitespace only')

        # Sanitize the input - remove potentially harmful characters/sequences
        sanitized = v.strip()

        # Check for potential injection attempts
        injection_patterns = [
            r'<script.*?>.*?</script>',  # HTML/JS injection
            r'javascript:',              # JS protocol
            r'vbscript:',               # VBScript protocol
            r'on\w+\s*=',               # Event handlers
        ]

        for pattern in injection_patterns:
            if re.search(pattern, sanitized, re.IGNORECASE):
                raise ValueError('Query contains potentially unsafe content')

        # Limit query length to prevent abuse
        if len(sanitized) > 1000:
            raise ValueError('Query must be less than 1000 characters')

        # Additional sanitization - remove excessive whitespace
        sanitized = re.sub(r'\s+', ' ', sanitized)

        return sanitized