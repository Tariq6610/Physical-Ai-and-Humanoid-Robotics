# Physical AI and Humanoid Robotics RAG API Documentation

## Overview

The Physical AI and Humanoid Robotics RAG (Retrieval-Augmented Generation) API provides a chat interface that retrieves relevant information from the Physical AI and Humanoid Robotics book content and generates contextual responses using an LLM.

## API Endpoints

### Authentication

#### `POST /token`
Generate a JWT token for API authentication (for testing purposes).

**Request:**
```json
{}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Chat Service

#### `POST /chat`
Main chat endpoint that processes user queries using the RAG system.

**Headers:**
- `Authorization: Bearer <token>` (Optional but recommended)
- `Content-Type: application/json`

**Request Body:**
```json
{
  "query": "string",           // User query (required, max 1000 chars)
  "session_id": "string"       // Optional session identifier
}
```

**Successful Response:**
```json
{
  "response": "string",        // Generated response from RAG system
  "request_id": "string"       // Unique identifier for the request
}
```

**Error Responses:**

**422 Validation Error:**
```json
{
  "error": "Validation Error",
  "error_code": "VALIDATION_ERROR",
  "message": "string",
  "details": [
    {
      "field": "string",
      "error": "string"
    }
  ],
  "timestamp": "2023-01-01T00:00:00Z",
  "request_id": "string"
}
```

**429 Rate Limit Exceeded:**
```json
{
  "error": "Rate Limit Exceeded",
  "error_code": "RATE_LIMIT_EXCEEDED",
  "message": "Rate limit exceeded. Please try again later.",
  "timestamp": "2023-01-01T00:00:00Z",
  "request_id": "string"
}
```

**503 Service Unavailable:**
```json
{
  "error": "Service Unavailable",
  "error_code": "RAG_SERVICE_ERROR",
  "message": "The chatbot is currently unavailable. Please try again later.",
  "timestamp": "2023-01-01T00:00:00Z",
  "request_id": "string"
}
```

**500 Internal Server Error:**
```json
{
  "error": "Internal Server Error",
  "error_code": "INTERNAL_ERROR",
  "message": "The chatbot is currently unavailable. Please try again later.",
  "timestamp": "2023-01-01T00:00:00Z",
  "request_id": "string"
}
```

### Health Check

#### `GET /health`
Health check endpoint to verify the service is running.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2023-01-01T00:00:00Z",
  "service": "Physical AI and Humanoid Robotics RAG API",
  "version": "1.0.0"
}
```

### Root Endpoint

#### `GET /`
Welcome message endpoint.

**Response:**
```json
{
  "message": "Welcome to the Physical AI and Humanoid Robotics Backend!"
}
```

## Usage Examples

### Python Example
```python
import requests

# Get authentication token (for testing)
token_response = requests.post("http://localhost:8000/token")
token = token_response.json()["access_token"]

# Make a chat request
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

data = {
    "query": "What is ROS 2?"
}

response = requests.post(
    "http://localhost:8000/chat",
    headers=headers,
    json=data
)

print(response.json()["response"])
```

### cURL Example
```bash
# Get token
TOKEN=$(curl -X POST http://localhost:8000/token | jq -r '.access_token')

# Make chat request
curl -X POST http://localhost:8000/chat \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"query": "What is robot kinematics?"}'
```

## Rate Limiting

The API implements rate limiting:
- 100 requests per hour per IP address
- Exceeding the limit returns a 429 status code

## Security

- JWT-based authentication is supported
- Input validation and sanitization for XSS prevention
- Query length limits (max 1000 characters)
- Sanitization of potentially harmful content

## Error Handling

The API follows standard HTTP status codes:
- `200`: Successful response
- `400`: Bad request
- `422`: Validation error
- `429`: Rate limit exceeded
- `500`: Internal server error
- `503`: Service unavailable

## Performance Metrics

The RAG service tracks performance metrics:
- Total queries processed
- Cache hit rate
- Average response times for each component
- Total processing time

## Query Guidelines

- Queries should be related to Physical AI, Humanoid Robotics, or the book content
- Off-topic queries will receive a specific response
- Queries are sanitized to prevent injection attacks
- Maximum query length is 1000 characters

## Troubleshooting

### Common Issues:

1. **"The chatbot is currently unavailable"**:
   - Check that Qdrant is running and accessible
   - Verify OpenAI API key is properly configured
   - Check application logs for specific errors

2. **Rate Limit Exceeded**:
   - Reduce request frequency
   - Implement exponential backoff in client applications

3. **Validation Errors**:
   - Ensure query is not empty
   - Check query length (max 1000 characters)
   - Verify no malicious content is included

## Environment Variables

For proper operation, ensure the following environment variables are set:

| Variable | Description | Default |
|----------|-------------|---------|
| QDRANT_URL | URL for Qdrant server | http://localhost:6333 |
| QDRANT_API_KEY | API key for Qdrant | None |
| QDRANT_COLLECTION_NAME | Name of the collection in Qdrant | book_content |
| OPENAI_API_KEY | API key for OpenAI | None |
| OPENAI_MODEL | OpenAI model to use | gpt-3.5-turbo |
| EMBEDDING_MODEL_NAME | Name of the Sentence Transformer model | all-MiniLM-L6-v2 |
| JWT_SECRET_KEY | Secret key for JWT token generation | your-secret-key-change-in-production |
| RETRIEVAL_LIMIT | Maximum number of documents to retrieve | 5 |
| SIMILARITY_THRESHOLD | Minimum similarity score for document retrieval | 0.5 |
| DEBUG | Enable debug mode | False |