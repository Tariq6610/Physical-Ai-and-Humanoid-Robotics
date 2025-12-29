# Physical AI and Humanoid Robotics Backend

This is the backend API for the Physical AI and Humanoid Robotics RAG chatbot. It provides endpoints for chatting with the RAG system, which retrieves information from the Physical AI and Humanoid Robotics book content and generates contextual responses using an LLM.

## Features

- RAG (Retrieval-Augmented Generation) chat system powered by **OpenAI Agents SDK**
- Vector search using Qdrant
- Semantic embeddings with Sentence Transformers
- LLM integration with Google Gemini (via LiteLLM)
- Conversation memory with SQLiteSession
- Rate limiting and authentication
- Health check endpoints
- Comprehensive error handling and logging

## Architecture

The backend uses the OpenAI Agents SDK for intelligent orchestration:

```
User Query → FastAPI Endpoint → RAG Agent → Function Tools:
                                              ├─ check_topic_relevance()
                                              └─ retrieve_documentation()
                                                     ├─ Embeddings (SentenceTransformer)
                                                     └─ Vector Search (Qdrant)
                                         ↓
                                    LiteLLM → Gemini API
                                         ↓
                                    SQLiteSession (conversation history)
                                         ↓
                                    Response with citations
```

### Key Components

- **Agent**: Orchestrates RAG workflow with natural language instructions
- **Function Tools**: Decorated with `@function_tool` for Qdrant retrieval and topic validation
- **SQLiteSession**: File-based conversation memory (`conversations.db`)
- **LiteLLM**: Unified interface for Gemini API (free tier)

## Environment Variables

The application uses the following environment variables:

### Qdrant Configuration
- `QDRANT_URL` - URL for Qdrant server (default: `http://localhost:6333`)
- `QDRANT_API_KEY` - API key for Qdrant (default: `None` for local development)
- `QDRANT_COLLECTION_NAME` - Name of the collection in Qdrant (default: `book_content`)

### LLM Configuration (Gemini via LiteLLM)
- `GEMINI_API_KEY` - **Required**: API key for Google Gemini (get from https://makersuite.google.com/app/apikey)
- `LLM_MODEL` - Gemini model to use (default: `gemini/gemini-2.5-flash` for low-latency, free tier)

### Session Management (OpenAI Agents SDK)
- `SESSION_DB_PATH` - Path to SQLiteSession database file (default: `./conversations.db`)
- `SESSION_EXPIRY_HOURS` - Hours before session expires (default: `24`)

### Embedding Configuration
- `EMBEDDING_MODEL_NAME` - Name of the Sentence Transformer model (default: `all-MiniLM-L6-v2`)

### Application Configuration
- `APP_TITLE` - Title of the application (default: `Physical AI and Humanoid Robotics RAG API`)
- `APP_VERSION` - Version of the application (default: `1.0.0`)
- `DEBUG` - Enable debug mode (default: `False`)

### RAG Service Configuration
- `RETRIEVAL_LIMIT` - Maximum number of documents to retrieve (default: `5`)
- `SIMILARITY_THRESHOLD` - Minimum similarity score for document retrieval (default: `0.5`)

### Rate Limiting Configuration
- `RATE_LIMIT_REQUESTS` - Number of requests allowed per window (default: `100`)
- `RATE_LIMIT_WINDOW` - Time window in seconds (default: `3600` for 1 hour)

### Security Configuration
- `JWT_SECRET_KEY` - Secret key for JWT token generation (default: `your-secret-key-change-in-production`)

## Setup

### Prerequisites

- Python 3.11+ (required for OpenAI Agents SDK)
- Qdrant vector database (free tier cloud or local)
- Google Gemini API key (free tier from https://makersuite.google.com/app/apikey)

### Installation

1. Clone the repository
2. Install dependencies (includes OpenAI Agents SDK with LiteLLM):
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file with required environment variables:
   ```bash
   # Required
   GEMINI_API_KEY=your-gemini-api-key-here
   QDRANT_URL=https://your-cluster.qdrant.io
   QDRANT_API_KEY=your-qdrant-key

   # Optional (with defaults)
   SESSION_DB_PATH=./conversations.db
   LLM_MODEL=gemini/gemini-2.5-flash
   QDRANT_COLLECTION_NAME=book_content
   ```
4. Initialize the session database (auto-created on first run):
   ```bash
   touch conversations.db
   ```
5. Run the application:
   ```bash
   uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
   ```

### Running Tests

```bash
pytest
```

### Content Ingestion

To ingest content into the vector database, run:

```bash
python scripts/ingest.py
```

This will scan markdown files in the `docs/docs/` directory, chunk them, and store them in Qdrant.

## API Endpoints

- `GET /` - Root endpoint with welcome message
- `GET /health` - Health check endpoint
- `POST /token` - Generate authentication token (for testing)
- `POST /chat` - Chat endpoint with RAG functionality

## Development

### Running locally

1. Set up your environment variables in a `.env` file
2. Start Qdrant locally (or connect to a remote instance)
3. Run the application:
   ```bash
   uvicorn src.main:app --reload
   ```

### Testing

The project includes comprehensive tests in the `tests/` directory. Run them with:
```bash
pytest
```

## Session Management & Cleanup

### Conversation History

The application uses SQLiteSession (OpenAI Agents SDK) to persist conversation history:

- **Storage**: `conversations.db` file (SQLite database)
- **Auto-creation**: Tables created automatically on first session
- **Schema**: Managed by Agents SDK (messages, sessions tables)
- **Retention**: Sessions expire after 24 hours of inactivity

### Cleanup Job (Required for Production)

To prevent database bloat, run a daily cron job to delete expired sessions:

```bash
# Add to crontab: Run daily at 2 AM
0 2 * * * cd /path/to/backend && python -c "
import sqlite3
from datetime import datetime, timedelta

conn = sqlite3.connect('conversations.db')
cursor = conn.cursor()

# Delete sessions older than 24 hours
expiry_time = datetime.now() - timedelta(hours=24)
cursor.execute(
    'DELETE FROM sessions WHERE last_activity_at < ?',
    (expiry_time.isoformat(),)
)
conn.commit()
conn.close()
"
```

**Alternative**: Create a dedicated cleanup script:

```python
# scripts/cleanup_sessions.py
import sqlite3
import os
from datetime import datetime, timedelta
from src.core.config import get_settings

settings = get_settings()
db_path = settings.session_db_path

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

expiry_hours = settings.session_expiry_hours or 24
expiry_time = datetime.now() - timedelta(hours=expiry_hours)

cursor.execute(
    'DELETE FROM sessions WHERE last_activity_at < ?',
    (expiry_time.isoformat(),)
)
deleted_count = cursor.rowcount
conn.commit()
conn.close()

print(f"Deleted {deleted_count} expired sessions")
```

Run with: `python scripts/cleanup_sessions.py`

## Deployment

### Live Deployment

The backend is deployed on Railway and accessible at:

**Production URL:** https://physical-ai-and-humanoid-robotics-production-5817.up.railway.app

#### Production Endpoints

| Endpoint | URL |
|----------|-----|
| Root | https://physical-ai-and-humanoid-robotics-production-5817.up.railway.app/ |
| Health Check | https://physical-ai-and-humanoid-robotics-production-5817.up.railway.app/health |
| Chat | https://physical-ai-and-humanoid-robotics-production-5817.up.railway.app/chat |

### Self-Hosting

For self-hosted deployment:

1. Ensure all sensitive environment variables are properly configured
2. Set `DEBUG` to `False`
3. Use a secure `JWT_SECRET_KEY`
4. Configure proper rate limiting values (Gemini free tier: 15 req/min)
5. Ensure Qdrant is properly secured and accessible
6. **Mount persistent disk** for `conversations.db` (Render, AWS, etc.)
7. Set up daily cleanup cron job (see Session Management above)
8. Set up proper monitoring and logging