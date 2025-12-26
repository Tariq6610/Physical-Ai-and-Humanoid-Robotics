"""
RAG Service using OpenAI Agents SDK
Simplified service that leverages the Agent for RAG-based Q&A.
"""

import logging
import time
import asyncio
from typing import Optional
from agents import Runner

from src.agents import get_rag_agent, get_session_manager

logger = logging.getLogger(__name__)


class RAGService:
    """Service for handling RAG-based Q&A using OpenAI Agents SDK."""

    def __init__(self):
        """Initialize the RAG service."""
        self.agent = get_rag_agent()
        self.session_manager = get_session_manager()
        
        # Initialize metrics tracking
        self._metrics = {
            'total_queries': 0,
            'total_time_total': 0.0,
            'agent_calls': 0,
        }
        
        logger.info("RAGService initialized with OpenAI Agents SDK")

    async def chat_async(self, query: str, session_id: Optional[str] = None) -> str:
        """
        Process a chat query using the Agent asynchronously.

        Args:
            query: User's question
            session_id: Optional session ID for conversation history. If None, creates a new session.

        Returns:
            str: Agent's response

        Raises:
            Exception: If agent execution fails
        """
        logger.info(f"Processing async chat query: {query[:50]}... (session_id={session_id})")
        start_time = time.time()

        try:
            # Get or create session if session_id provided
            session = None
            if session_id:
                session = self.session_manager.get_or_create_session(session_id)
                logger.debug(f"Using session: {session_id}")

            # Run agent with query and session
            result = await Runner.run(
                self.agent,
                input=query,
                session=session
            )

            # Extract final output
            response = str(result.final_output)
            
            # Update metrics
            total_time = time.time() - start_time
            self._metrics['total_queries'] += 1
            self._metrics['total_time_total'] += total_time
            self._metrics['agent_calls'] += 1

            logger.info(f"Agent response generated successfully in {total_time:.3f}s")
            return response

        except Exception as e:
            logger.error(f"Error in chat_async: {str(e)}", exc_info=True)
            raise

    def chat(self, query: str, session_id: Optional[str] = None) -> str:
        """
        Process a chat query using the Agent (synchronous wrapper).

        Args:
            query: User's question
            session_id: Optional session ID for conversation history

        Returns:
            str: Agent's response

        Raises:
            Exception: If agent execution fails
        """
        logger.info(f"Processing sync chat query: {query[:50]}...")
        
        try:
            # Run async function in event loop
            return asyncio.run(self.chat_async(query, session_id))
        except Exception as e:
            logger.error(f"Error in chat: {str(e)}", exc_info=True)
            # Return user-friendly error message
            return "I encountered an error processing your request. Please try again or rephrase your question."

    def get_performance_metrics(self) -> dict:
        """
        Get performance metrics for the RAG service.

        Returns:
            dict: Performance metrics including query counts and timing
        """
        metrics = self._metrics.copy()
        
        # Calculate averages
        if metrics['total_queries'] > 0:
            metrics['avg_total_time'] = metrics['total_time_total'] / metrics['total_queries']
        else:
            metrics['avg_total_time'] = 0.0

        return metrics

    def clear_session(self, session_id: str) -> bool:
        """
        Clear conversation history for a session.

        Args:
            session_id: The session ID to clear

        Returns:
            bool: True if successful, False otherwise
        """
        logger.info(f"Clearing session: {session_id}")
        return self.session_manager.clear_session(session_id)
