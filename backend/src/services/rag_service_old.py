import os
import time
from typing import List, Dict
from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.http.models import PointStruct, VectorParams, Distance
from src.core.config import get_settings
import logging
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
import openai
from openai import OpenAI, APIError, RateLimitError, AuthenticationError, APIConnectionError
from sentence_transformers import SentenceTransformer
import asyncio
from functools import lru_cache
import hashlib
import json

# Configure logger
logger = logging.getLogger(__name__)


class RAGService:
    def __init__(self):
        settings = get_settings()

        # Initialize Qdrant client with real implementation
        if settings.qdrant_api_key:
            self.qdrant_client = QdrantClient(
                url=settings.qdrant_url,
                api_key=settings.qdrant_api_key,
                timeout=10  # 10 second timeout
            )
        else:
            # For local development without API key
            self.qdrant_client = QdrantClient(
                host="localhost",
                port=6333,
                timeout=10
            )

        self.collection_name = settings.qdrant_collection_name

        # Initialize Sentence Transformer for embeddings with real implementation
        from sentence_transformers import SentenceTransformer
        self.embedding_model = SentenceTransformer(settings.embedding_model_name)

        # Initialize LLM client for responses (supporting both OpenAI and Google's OpenAI-compatible endpoint)
        import openai
        from openai import OpenAI
        settings = get_settings()

        if settings.llm_provider == "google_openai_compat" and settings.google_api_key:
            # Use Google's OpenAI-compatible endpoint for Gemini
            self.llm_client = OpenAI(
                api_key=settings.google_api_key,
                base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
            )
            self.model_name = settings.google_model
            logger.info(f"Initialized Google Gemini client with model: {self.model_name}")
        elif settings.openai_api_key:
            # Use OpenAI
            self.llm_client = OpenAI(api_key=settings.openai_api_key)
            self.model_name = settings.openai_model
            logger.info(f"Initialized OpenAI client with model: {self.model_name}")
        else:
            # For testing purposes only - in production, this should not happen
            self.llm_client = None
            self.model_name = settings.openai_model  # Default fallback
            logger.warning("No LLM API key found. LLM functionality will be limited.")

        # Initialize cache for query results
        self._query_cache = {}
        self._cache_ttl = 300  # 5 minutes TTL for cache entries

        # Initialize metrics tracking
        self._metrics = {
            'total_queries': 0,
            'cache_hits': 0,
            'embedding_time_total': 0.0,
            'embedding_calls': 0,
            'retrieval_time_total': 0.0,
            'retrieval_calls': 0,
            'generation_time_total': 0.0,
            'generation_calls': 0,
            'total_time_total': 0.0,
        }

    def _get_cache_key(self, query: str) -> str:
        """Generate a cache key for the given query."""
        return hashlib.md5(query.encode()).hexdigest()

    def _is_cache_valid(self, timestamp: float) -> bool:
        """Check if cached entry is still valid based on TTL."""
        import time
        return (time.time() - timestamp) < self._cache_ttl

    def _get_from_cache(self, query: str) -> str:
        """Get result from cache if available and valid."""
        cache_key = self._get_cache_key(query)
        if cache_key in self._query_cache:
            result, timestamp = self._query_cache[cache_key]
            if self._is_cache_valid(timestamp):
                logger.info(f"Cache hit for query: {query[:30]}...")
                self._metrics['cache_hits'] += 1
                return result
            else:
                # Remove expired entry
                del self._query_cache[cache_key]
        return None

    def _put_in_cache(self, query: str, result: str):
        """Put result in cache."""
        import time
        cache_key = self._get_cache_key(query)
        self._query_cache[cache_key] = (result, time.time())
        logger.info(f"Stored result in cache for query: {query[:30]}...")

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type((Exception,))
    )
    def get_query_embedding(self, query: str) -> List[float]:
        """Generate embedding for the input query using SentenceTransformer with retry logic."""
        logger.info(f"Generating embedding for query: {query[:50]}...")
        start_time = time.time()
        try:
            embedding = self.embedding_model.encode(query).tolist()
            embedding_time = time.time() - start_time
            logger.debug(f"Generated embedding of length {len(embedding)} for query in {embedding_time:.3f}s")

            # Update metrics
            self._metrics['embedding_time_total'] += embedding_time
            self._metrics['embedding_calls'] += 1

            return embedding
        except Exception as e:
            logger.error(f"Error generating query embedding for query '{query[:30]}...': {str(e)}", exc_info=True)
            raise

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type((Exception,))
    )
    def retrieve_context(self, query_embedding: List[float]) -> List[Dict]:
        """Retrieve relevant context from Qdrant vector database with retry logic."""
        logger.info(f"Retrieving context from collection '{self.collection_name}' with embedding vector of length {len(query_embedding)}")
        start_time = time.time()
        try:
            # Query similar vectors in the collection
            search_results = self.qdrant_client.query_points(
                collection_name=self.collection_name,
                query=query_embedding,
                limit=get_settings().retrieval_limit,
                score_threshold=get_settings().similarity_threshold
            ).points

            # Format results to match the expected structure
            formatted_results = []
            for result in search_results:
                formatted_results.append({
                    "id": result.id,
                    "payload": result.payload,
                    "score": result.score
                })

            retrieval_time = time.time() - start_time
            logger.info(f"Retrieved {len(formatted_results)} relevant chunks from Qdrant in {retrieval_time:.3f}s")

            # Update metrics
            self._metrics['retrieval_time_total'] += retrieval_time
            self._metrics['retrieval_calls'] += 1

            return formatted_results
        except Exception as e:
            logger.error(f"Error retrieving context from Qdrant collection '{self.collection_name}': {str(e)}", exc_info=True)
            # Return empty list if there's an error
            return []

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type((APIError, RateLimitError, APIConnectionError))
    )
    def generate_answer(self, query: str, context: List[Dict]) -> str:
        """Generate an answer using OpenAI based on the query and retrieved context with retry logic."""
        logger.info(f"Generating answer for query with {len(context)} context chunks")
        start_time = time.time()

        if not context:
            logger.info("No relevant context found for query, returning appropriate response")
            return "I couldn't find any relevant information in the book to answer your question. Please try rephrasing your question or ask about a different topic related to Physical AI and Humanoid Robotics."

        # Format context for the LLM with better structure and relevance scoring
        formatted_context_parts = []
        for i, chunk in enumerate(context):
            source = chunk['payload'].get('source', 'Unknown')
            content = chunk['payload'].get('text', '')
            score = chunk.get('score', 0.0)
            section = chunk['payload'].get('section', 'General')

            formatted_context_parts.append(
                f"--- Document {i+1} (Relevance: {score:.3f}) ---\n"
                f"Source: {source}\n"
                f"Section: {section}\n"
                f"Content: {content}\n"
            )

        context_str = "\n".join(formatted_context_parts)

        # Create a comprehensive prompt for the LLM with better instructions
        prompt = (
            "You are an expert AI assistant for the book 'Physical AI and Humanoid Robotics'. "
            "Your role is to provide accurate, helpful answers based ONLY on the provided context from the book. "
            "Follow these guidelines strictly:\n"
            "1. Base your answer ONLY on the information provided in the context below\n"
            "2. If the answer is not in the context, clearly state that you don't know and suggest checking the book\n"
            "3. Be concise but comprehensive in your response\n"
            "4. Cite specific sources when possible\n"
            "5. Maintain a professional, educational tone\n"
            "6. Structure your response logically with clear explanations\n\n"
            f"USER QUESTION: {query}\n\n"
            f"BOOK CONTEXT:\n{context_str}\n\n"
            "Please provide a detailed answer to the user's question based on the above context. "
            "Structure your response with:\n"
            "1. A direct answer to the question\n"
            "2. Supporting details from the context\n"
            "3. Citations to specific sources when available\n"
            "4. If relevant, mention related concepts from the context\n\n"
            "RESPONSE:"
        )

        try:
            if self.llm_client:
                logger.debug(f"Sending request to LLM model: {self.model_name}")
                response = self.llm_client.chat.completions.create(
                    model=self.model_name,
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant for the book 'Physical AI and Humanoid Robotics'. Answer questions based on the provided context only."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=500,
                    temperature=0.3,
                )
                generation_time = time.time() - start_time
                logger.info(f"Successfully received response from LLM in {generation_time:.3f}s")

                # Update metrics
                self._metrics['generation_time_total'] += generation_time
                self._metrics['generation_calls'] += 1

                return response.choices[0].message.content
            else:
                # Fallback response if LLM is not configured
                logger.warning("LLM client not configured, returning fallback response")
                return "LLM API is not configured. Please set the appropriate API key environment variable (OPENAI_API_KEY or GOOGLE_API_KEY) to get detailed answers. The system has found relevant content but cannot generate a complete response without the LLM service."
        except RateLimitError:
            logger.warning("LLM rate limit exceeded")
            return "The chatbot is currently experiencing high demand. Please try again in a moment."
        except AuthenticationError:
            logger.error("LLM authentication failed - check API key")
            return "The chatbot is temporarily unavailable due to a configuration issue. Please contact the system administrator."
        except APIConnectionError:
            logger.error("Failed to connect to LLM API")
            return "The chatbot is temporarily unavailable. Please try again later."
        except APIError as e:
            logger.error(f"LLM API error: {str(e)}", exc_info=True)
            # Fallback: return the raw context if LLM fails
            return f"I found relevant information but encountered an error generating a response. The most relevant content from the book is: {context_str[:500]}... (truncated)"
        except Exception as e:
            logger.error(f"Unexpected error generating answer with LLM: {str(e)}", exc_info=True)
            # Fallback: return the raw context if LLM fails
            return f"I found relevant information but encountered an error generating a response. The most relevant content from the book is: {context_str[:500]}... (truncated)"

    @retry(
        stop=stop_after_attempt(2),
        wait=wait_exponential(multiplier=1, min=2, max=5),
        retry=retry_if_exception_type((Exception,))
    )
    def chat(self, query: str) -> str:
        """Main method to process a chat query through the RAG pipeline with retry logic and caching."""
        logger.info(f"Processing chat query: {query[:50]}...")
        start_time = time.time()

        # Check cache first
        cached_result = self._get_from_cache(query)
        if cached_result:
            logger.info("Returning cached result for query")
            # Update total queries counter
            self._metrics['total_queries'] += 1
            total_time = time.time() - start_time
            self._metrics['total_time_total'] += total_time
            return cached_result

        try:
            # 1. Generate query embedding
            query_embedding = self.get_query_embedding(query)
            logger.debug("Query embedding generated successfully")

            # 2. Retrieve relevant context from Qdrant
            context = self.retrieve_context(query_embedding)
            logger.debug(f"Retrieved {len(context)} context chunks from vector database")

            # 3. Generate answer using LLM
            answer = self.generate_answer(query, context)
            logger.info("Successfully generated answer for query")

            # Store result in cache
            self._put_in_cache(query, answer)

            # Update metrics
            self._metrics['total_queries'] += 1
            total_time = time.time() - start_time
            self._metrics['total_time_total'] += total_time

            return answer
        except Exception as e:
            logger.error(f"Error in RAG chat processing for query '{query[:30]}...': {str(e)}", exc_info=True)
            # Update metrics even when there's an error
            self._metrics['total_queries'] += 1
            total_time = time.time() - start_time
            self._metrics['total_time_total'] += total_time
            return "I'm sorry, but I encountered an error processing your request. Please try again later."

    def get_performance_metrics(self) -> Dict:
        """Get performance metrics for monitoring and reporting."""
        # Calculate averages and percentages
        avg_embedding_time = (
            self._metrics['embedding_time_total'] / self._metrics['embedding_calls']
            if self._metrics['embedding_calls'] > 0 else 0
        )
        avg_retrieval_time = (
            self._metrics['retrieval_time_total'] / self._metrics['retrieval_calls']
            if self._metrics['retrieval_calls'] > 0 else 0
        )
        avg_generation_time = (
            self._metrics['generation_time_total'] / self._metrics['generation_calls']
            if self._metrics['generation_calls'] > 0 else 0
        )
        avg_total_time = (
            self._metrics['total_time_total'] / self._metrics['total_queries']
            if self._metrics['total_queries'] > 0 else 0
        )
        cache_hit_rate = (
            (self._metrics['cache_hits'] / self._metrics['total_queries']) * 100
            if self._metrics['total_queries'] > 0 else 0
        )

        return {
            'total_queries': self._metrics['total_queries'],
            'cache_hits': self._metrics['cache_hits'],
            'cache_hit_rate_percent': round(cache_hit_rate, 2),
            'embedding_calls': self._metrics['embedding_calls'],
            'retrieval_calls': self._metrics['retrieval_calls'],
            'generation_calls': self._metrics['generation_calls'],
            'avg_embedding_time_seconds': round(avg_embedding_time, 4),
            'avg_retrieval_time_seconds': round(avg_retrieval_time, 4),
            'avg_generation_time_seconds': round(avg_generation_time, 4),
            'avg_total_time_seconds': round(avg_total_time, 4),
            'total_embedding_time_seconds': round(self._metrics['embedding_time_total'], 4),
            'total_retrieval_time_seconds': round(self._metrics['retrieval_time_total'], 4),
            'total_generation_time_seconds': round(self._metrics['generation_time_total'], 4),
            'total_processing_time_seconds': round(self._metrics['total_time_total'], 4),
        }