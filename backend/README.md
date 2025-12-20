# Physical AI and Humanoid Robotics Backend

This is the backend API for the Physical AI and Humanoid Robotics RAG chatbot. It provides endpoints for chatting with the RAG system, which retrieves information from the Physical AI and Humanoid Robotics book content and generates contextual responses using an LLM.

## Features

- RAG (Retrieval-Augmented Generation) chat system
- Vector search using Qdrant
- Semantic embeddings with Sentence Transformers
- LLM integration with OpenAI
- Rate limiting and authentication
- Health check endpoints
- Comprehensive error handling and logging

## Environment Variables

The application uses the following environment variables:

### Qdrant Configuration
- `QDRANT_URL` - URL for Qdrant server (default: `http://localhost:6333`)
- `QDRANT_API_KEY` - API key for Qdrant (default: `None` for local development)
- `QDRANT_COLLECTION_NAME` - Name of the collection in Qdrant (default: `book_content`)

### OpenAI Configuration
- `OPENAI_API_KEY` - API key for OpenAI (required for production)
- `OPENAI_MODEL` - OpenAI model to use (default: `gpt-3.5-turbo`)

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

- Python 3.8+
- Qdrant vector database
- OpenAI API key (for production)

### Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file with your environment variables
4. Run the application:
   ```bash
   uvicorn src.main:app --reload
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

## Deployment

For production deployment:

1. Ensure all sensitive environment variables are properly configured
2. Set `DEBUG` to `False`
3. Use a secure `JWT_SECRET_KEY`
4. Configure proper rate limiting values
5. Ensure Qdrant is properly secured and accessible
6. Set up proper monitoring and logging