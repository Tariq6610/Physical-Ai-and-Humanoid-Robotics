"""
Session Manager
Wrapper for SQLiteSession to manage conversation history and session lifecycle.
"""

import logging
from typing import Optional
from agents import SQLiteSession

from src.core.config import get_settings

logger = logging.getLogger(__name__)


class SessionManager:
    """Manages chat sessions using SQLiteSession from OpenAI Agents SDK."""

    def __init__(self, db_path: Optional[str] = None):
        """
        Initialize the SessionManager.

        Args:
            db_path: Path to the SQLite database file. If None, uses default from settings.
        """
        settings = get_settings()
        self.db_path = db_path or settings.session_db_path
        logger.info(f"SessionManager initialized with database: {self.db_path}")

    def get_or_create_session(self, session_id: str) -> SQLiteSession:
        """
        Get an existing session or create a new one.

        Args:
            session_id: Unique identifier for the conversation session

        Returns:
            SQLiteSession: The session instance for managing conversation history

        Examples:
            >>> manager = SessionManager()
            >>> session = manager.get_or_create_session("user_123")
        """
        logger.info(f"Getting or creating session: {session_id}")

        try:
            # SQLiteSession automatically creates tables if they don't exist
            session = SQLiteSession(session_id, self.db_path)
            logger.debug(f"Session '{session_id}' retrieved/created successfully")
            return session
        except Exception as e:
            logger.error(f"Error creating session '{session_id}': {str(e)}", exc_info=True)
            raise

    def get_conversation_summary(self, session_id: str, limit: int = 5) -> dict:
        """
        Get a summary of the conversation history for a session.

        Args:
            session_id: The session ID to retrieve history for
            limit: Maximum number of recent message pairs to include

        Returns:
            dict: Summary with session_id, message_count, and recent_messages

        Examples:
            >>> manager = SessionManager()
            >>> summary = manager.get_conversation_summary("user_123", limit=3)
        """
        logger.info(f"Getting conversation summary for session: {session_id}")

        try:
            session = SQLiteSession(session_id, self.db_path)

            # Get session items (messages)
            items = session.get_items(limit=limit * 2)  # *2 to account for user+assistant pairs

            summary = {
                "session_id": session_id,
                "message_count": len(items),
                "recent_messages": [
                    {
                        "role": getattr(item, "role", "unknown"),
                        "content": getattr(item, "content", "")[:100]  # Truncate for summary
                    }
                    for item in items
                ]
            }

            logger.debug(f"Retrieved summary with {summary['message_count']} messages")
            return summary

        except Exception as e:
            logger.error(f"Error getting conversation summary for '{session_id}': {str(e)}", exc_info=True)
            return {
                "session_id": session_id,
                "message_count": 0,
                "recent_messages": [],
                "error": str(e)
            }

    def clear_session(self, session_id: str) -> bool:
        """
        Clear all messages from a session while keeping the session ID.

        Args:
            session_id: The session ID to clear

        Returns:
            bool: True if successful, False otherwise

        Examples:
            >>> manager = SessionManager()
            >>> manager.clear_session("user_123")
        """
        logger.info(f"Clearing session: {session_id}")

        try:
            session = SQLiteSession(session_id, self.db_path)
            session.clear_session()
            logger.info(f"Session '{session_id}' cleared successfully")
            return True
        except Exception as e:
            logger.error(f"Error clearing session '{session_id}': {str(e)}", exc_info=True)
            return False


# Global instance for reuse
_session_manager_instance = None


def get_session_manager() -> SessionManager:
    """
    Get or create the global SessionManager instance.

    Returns:
        SessionManager: The global session manager instance
    """
    global _session_manager_instance
    if _session_manager_instance is None:
        _session_manager_instance = SessionManager()
    return _session_manager_instance
