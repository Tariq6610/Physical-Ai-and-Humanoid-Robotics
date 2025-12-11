---
sidebar_position: 1
title: Architecting the RAG System
---

## Introduction

This chapter details the architecture of the Retrieval-Augmented Generation (RAG) system that powers our book's companion chatbot. We will cover the core components, including the choice of vector database (Qdrant), the backend framework (FastAPI), and the AI SDKs (OpenAI), to create an intelligent and interactive learning experience.

## Lesson 13.1: Understanding the RAG Architecture

At its heart, our chatbot needs to answer questions based *only* on the content of this book. A standard Large Language Model (LLM) like GPT has vast general knowledge, but it hasn't read this specific book. This is where **Retrieval-Augmented Generation (RAG)** comes in.

RAG is a powerful technique that grounds an LLM in a specific set of documents, preventing it from "hallucinating" or making up answers. It works in two main steps:

1.  **Retrieval**: When a user asks a question (e.g., "How do I set up a ROS 2 node?"), the RAG system doesn't immediately ask the LLM. Instead, it first searches a specialized database (our "knowledge base") to find the most relevant snippets of text from this book that are likely to contain the answer. This is the "Retrieval" step.
2.  **Augmentation & Generation**: The system then takes the user's original question and injects the retrieved text snippets into the prompt it sends to the LLM. The prompt effectively becomes: "Using only the following information, answer this question." The LLM then "augments" its knowledge with the provided text and "generates" an answer based *only* on that context.

This process ensures that the chatbot's answers are directly tied to the book's content.

Our RAG architecture will consist of three main components:
-   **A Vector Database (Qdrant)**: To store the book's content in a way that's easy to search for relevance.
-   **A Backend API (FastAPI)**: To handle user requests, orchestrate the RAG process, and communicate with the LLM.
-   **A Content Ingestion Service**: A script that reads our book's Markdown files, splits them into chunks, converts them into numerical representations (vectors), and stores them in our vector database.

## Lesson 13.2: Setting up the Vector Database with Qdrant

To find relevant text, we need to search by *semantic meaning*, not just keywords. This is done by converting our text into numerical representations called **embeddings** or **vectors**. A vector database is a specialized database designed to store and search these vectors efficiently.

For this project, we'll use **Qdrant**, a powerful, open-source vector database. We'll use their free-tier cloud offering to get started quickly.

### Steps to Set Up Qdrant Cloud:

1.  **Create a Qdrant Cloud Account**: Navigate to [cloud.qdrant.io](https://cloud.qdrant.io/) and sign up for a free account.
2.  **Create a Cluster**: Once logged in, create a new cluster. The free tier is sufficient for our project. Qdrant will provide you with a **Cluster URL** and an **API Key**. Keep these safe; you'll need them for your backend.
3.  **Install the Python Client**: We'll interact with Qdrant from our Python backend. Install the client library:
    ```bash
    pip install qdrant-client
    ```

### Connecting to Qdrant from our Backend

In our FastAPI backend (which we'll build in the next lesson), we'll create a file, for instance `backend/src/services/rag_service.py`, to manage the Qdrant connection.

```python
# In backend/src/services/rag_service.py
from qdrant_client import QdrantClient
import os

class RAGService:
    def __init__(self):
        self.qdrant_client = QdrantClient(
            url=os.environ.get("QDRANT_URL"), 
            api_key=os.environ.get("QDRANT_API_KEY"),
        )
        self.collection_name = "robotics_book_content"

    def check_and_create_collection(self):
        """Checks if the collection exists, and creates it if not."""
        from qdrant_client.models import VectorParams, Distance

        try:
            self.qdrant_client.get_collection(collection_name=self.collection_name)
            print(f"Collection '{self.collection_name}' already exists.")
        except Exception:
            print(f"Creating collection '{self.collection_name}'.")
            self.qdrant_client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=384, distance=Distance.COSINE), # Size depends on the embedding model
            )

# We will use environment variables to store our credentials for security.
# Create a .env file in the backend directory:
# QDRANT_URL="YOUR_CLUSTER_URL"
# QDRANT_API_KEY="YOUR_API_KEY"
```

This setup gives us a persistent, searchable knowledge base for our book's content.

## Lesson 13.3: Building the Backend with FastAPI

Our backend will be a simple but powerful API built with **FastAPI**. FastAPI is a modern, fast (high-performance) web framework for building APIs with Python based on standard Python type hints.

### Project Structure

Our backend will live in the `backend/` directory with the following structure:

```
backend/
├── src/
│   ├── api/
│   │   └── chat.py      # The /chat endpoint
│   ├── core/
│   │   └── __init__.py
│   ├── models/
│   │   └── chat.py      # Pydantic models for request/response
│   ├── services/
│   │   └── rag_service.py # Our Qdrant and RAG logic
│   └── main.py          # Main FastAPI app entrypoint
└── requirements.txt
```

### Creating the FastAPI App

1.  **Install Dependencies**: Make sure `fastapi` and an ASGI server like `uvicorn` are in your `requirements.txt` and installed.
    ```bash
    pip install fastapi uvicorn
    ```

2.  **Create the main app file**:

    ```python
    # In backend/src/main.py
    from fastapi import FastAPI
    from .api import chat

    app = FastAPI(
        title="Robotics Book Chatbot API",
        description="API for the RAG-powered chatbot.",
        version="1.0.0",
    )

    app.include_router(chat.router, prefix="/api")

    @app.get("/")
    def read_root():
        return {"message": "Welcome to the Chatbot API"}
    ```

3.  **Define API Models**: We use Pydantic models to define the shape of our API requests and responses. This gives us automatic data validation and documentation.

    ```python
    # In backend/src/models/chat.py
    from pydantic import BaseModel
    from typing import List

    class ChatRequest(BaseModel):
        query: str
        
    class ChatResponse(BaseModel):
        answer: str
        sources: List[str]
    ```

4.  **Create the Chat Endpoint**: This is where the magic happens. The endpoint will receive a user's query, use the `RAGService` to get context, and then call the LLM to generate an answer.

    ```python
    # In backend/src/api/chat.py
    from fastapi import APIRouter, Depends
    from ..models.chat import ChatRequest, ChatResponse
    from ..services.rag_service import RAGService

    router = APIRouter()

    # Dependency to get a single instance of our RAGService
    def get_rag_service():
        return RAGService()

    @router.post("/chat", response_model=ChatResponse)
    async def chat_with_bot(
        request: ChatRequest,
        rag_service: RAGService = Depends(get_rag_service)
    ):
        # This is a simplified placeholder for the full RAG logic
        # In the full implementation, we would:
        # 1. Embed the user's query: rag_service.embed_query(request.query)
        # 2. Search Qdrant for relevant documents: rag_service.search(query_vector)
        # 3. Call an LLM with the documents and query
        # 4. Format and return the response

        # For now, a simple echo response
        answer = f"You asked: '{request.query}'. The RAG pipeline is not fully implemented yet."
        sources = ["docs/intro.md"]
        
        return ChatResponse(answer=answer, sources=sources)
    ```

This structure provides a clean, scalable, and well-documented backend for our chatbot, ready for the full RAG logic and frontend integration.

## Summary

In this chapter, we designed the complete architecture for our RAG-powered chatbot. We explored the core concepts of Retrieval-Augmented Generation, set up a cloud-based vector database with Qdrant, and scaffolded a robust backend API using FastAPI. This architecture lays a solid foundation for an intelligent, context-aware chatbot that can accurately answer questions about the book's content.

## Key Takeaways

*   RAG is a two-step process (Retrieve and Generate) that grounds LLMs in specific knowledge.
*   Vector databases like Qdrant are essential for efficient semantic search in RAG systems.
*   FastAPI is a modern Python framework ideal for building high-performance APIs.
*   A well-defined project structure separates concerns (API, services, models) and improves maintainability.
*   Environment variables should be used for storing sensitive credentials like API keys.