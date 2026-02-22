import os
from pathlib import Path
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Sarvam AI
    SARVAM_API_KEY: str
    SARVAM_EMBEDDING_MODEL: str = "sarvam-embeddings-1"
    SARVAM_RESPONSE_MODEL: str = "sarvam-chat-1"
    SARVAM_API_BASE: str = "https://api.sarvam.ai"
    
    # App
    APP_ENV: str = "production"
    LOG_LEVEL: str = "INFO"
    MAX_RESPONSE_LENGTH: int = 1000
    MIN_CONTEXT_CHUNKS: int = 2
    MAX_CONTEXT_CHUNKS: int = 5
    
    # Security
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_WINDOW: int = 3600
    ALLOWED_ORIGINS: list = ["*"]
    
    # Paths
    DATABASE_PATH: str = "./data/adoca.db"
    VECTOR_DB_PATH: str = "./data/vectors.db"
    KB_PATH: str = "./knowledge_base"
    LOG_PATH: str = "./logs"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
