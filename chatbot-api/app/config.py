"""Configuration management for the chatbot API."""

import os
from typing import List
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings with environment variable support."""
    
    # Ollama Configuration
    ollama_model: str = Field(default="qwen3:1.7b", alias="OLLAMA_MODEL")
    ollama_base_url: str = Field(default="http://localhost:11434", alias="OLLAMA_BASE_URL")
    
    # API Configuration
    api_host: str = Field(default="0.0.0.0", alias="API_HOST")
    api_port: int = Field(default=8000, alias="API_PORT")
    api_title: str = Field(default="Chatbot API", alias="API_TITLE")
    api_version: str = Field(default="1.0.0", alias="API_VERSION")
    api_description: str = Field(
        default="A ChatGPT-like chatbot API powered by Ollama",
        alias="API_DESCRIPTION"
    )
    
    # Logging
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    
    # CORS Configuration
    allowed_origins: List[str] = Field(default=["*"], alias="ALLOWED_ORIGINS")
    allowed_credentials: bool = Field(default=True, alias="ALLOWED_CREDENTIALS")
    allowed_methods: List[str] = Field(default=["*"], alias="ALLOWED_METHODS")
    allowed_headers: List[str] = Field(default=["*"], alias="ALLOWED_HEADERS")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        # Ensure environment variables take precedence over .env file
        env_prefix = ""


# Global settings instance
settings = Settings()

# Debug logging for configuration
import logging
logger = logging.getLogger(__name__)

# Log the loaded configuration for debugging
logger.info(f"Configuration loaded - OLLAMA_MODEL from env: {os.getenv('OLLAMA_MODEL', 'Not set')}")
logger.info(f"Configuration loaded - Settings ollama_model: {settings.ollama_model}") 