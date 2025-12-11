# Data Models for "Physical AI and Humanoid Robotics" Project

This document outlines the data models for the backend services supporting the book project, primarily for the RAG chatbot.

## 1. Core Data: Book Content

The primary data source is the book's content itself, which is unstructured. The content is processed as follows:

- **Source**: Markdown files (`.md`) from the `docs/docs` directory.
- **Processing**:
  1.  Content is parsed and cleaned.
  2.  Text is split into smaller chunks (e.g., paragraphs or sections).
  3.  Each chunk is converted into a vector embedding.
- **Storage**: The embeddings and the original text chunks are stored in a **Qdrant** vector collection.

### Qdrant Vector Schema

- **`id`**: A unique identifier for the chunk (e.g., UUID).
- **`vector`**: The embedding of the text chunk.
- **`payload`**:
  - `text`: The original text content of the chunk.
  - `source`: The originating file path or chapter name (e.g., `chapter1.md`).
  - `section`: The specific section or heading the chunk belongs to.

## 2. API Data Models (Pydantic)

These models define the structure of data sent to and from the FastAPI backend.

### Chat Endpoint (`/chat`)

#### Request Model

```python
from pydantic import BaseModel
from typing import Optional

class ChatRequest(BaseModel):
    """
    Request model for a user query to the chatbot.
    """
    query: str
    session_id: Optional[str] = None # For tracking conversation history in the future
```

#### Response Model

The response is a stream of text. However, if we were to include metadata, the payload for each message in the stream might look like this:

```python
from pydantic import BaseModel
from typing import List

class Source(BaseModel):
    """
    Represents a source document used to generate the answer.
    """
    text: str
    source_url: str # A direct link to the chapter/section

class ChatResponse(BaseModel):
    """
    Response model for a chatbot answer.
    """
    answer_chunk: str
    sources: List[Source] = []
```
*(For the initial implementation, a simple text stream (`StreamingResponse`) will be used.)*

## 3. Future Considerations

### User Feedback Model

If a feedback system is implemented, we would need a model to capture user ratings or comments on the chatbot's answers.

```python
from pydantic import BaseModel

class FeedbackRequest(BaseModel):
    """
    Model for capturing user feedback on an answer.
    """
    query: str
    answer: str
    is_helpful: bool
    comment: Optional[str] = None
    session_id: str
```
This data could be stored in a simple relational database (like SQLite or PostgreSQL) or a NoSQL database to help evaluate and improve the RAG system.
