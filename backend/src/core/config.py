import os
from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    """
    # Qdrant settings
    qdrant_url: str = Field(default="http://localhost:6333", env="QDRANT_URL")
    qdrant_api_key: Optional[str] = Field(default=None, env="QDRANT_API_KEY")
    qdrant_collection_name: str = Field(default="book_content", env="QDRANT_COLLECTION_NAME")

    # LLM Provider settings
    llm_provider: str = Field(default="openai", env="LLM_PROVIDER")  # openai, google_openai_compat
    openai_api_key: Optional[str] = Field(default=None, env="OPENAI_API_KEY")
    google_api_key: Optional[str] = Field(default=None, env="GOOGLE_API_KEY")
    openai_model: str = Field(default="gpt-3.5-turbo", env="OPENAI_MODEL")
    google_model: str = Field(default="gemini-2.0-flash", env="GOOGLE_MODEL")

    # Embedding settings
    embedding_model_name: str = Field(default="all-MiniLM-L6-v2", env="EMBEDDING_MODEL_NAME")

    # Application settings
    app_title: str = Field(default="Physical AI and Humanoid Robotics RAG API", env="APP_TITLE")
    app_version: str = Field(default="1.0.0", env="APP_VERSION")
    debug: bool = Field(default=False, env="DEBUG")

    # RAG settings
    retrieval_limit: int = Field(default=5, env="RETRIEVAL_LIMIT")
    similarity_threshold: float = Field(default=0.5, env="SIMILARITY_THRESHOLD")

    # Rate limiting and security
    rate_limit_requests: int = Field(default=100, env="RATE_LIMIT_REQUESTS")
    rate_limit_window: int = Field(default=3600, env="RATE_LIMIT_WINDOW")  # in seconds

    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()


def get_settings() -> Settings:
    """
    Get the application settings instance.
    """
    return settings