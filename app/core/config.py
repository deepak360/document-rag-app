import os
from typing import List, Optional
from pydantic import validator
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    # FastAPI settings
    PROJECT_NAME: str = "FastAPI Document"
    API_PREFIX: str = "/api/v1"
    DEBUG_MODE: bool = True
    FUTURE: bool = True
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # CORS
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000"]
    
    # Database settings
    DATABASE_URL: str ="postgresql+asyncpg://newuser:password@db/ragdb"
    MONGODB_URL: str = "mongodb://localhost:27017/"
    MONGODB_DB_NAME: str = "fastapi_db"
        
    # Security
    SECRET_KEY: str = "documentragapplication"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    OPENAI_API_KEY: str = "your_openai_key_here"
    OLLAMA_BASE_URL: str = "http://ollama:11434"
    
    
    @validator("ALLOWED_ORIGINS", pre=True)
    def parse_allowed_origins(cls, v):
        if isinstance(v, str):
            return v.split(",")
        return v

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra="allow"

settings = Settings()