from typing import Dict
from pydantic_settings import BaseSettings
from functools import lru_cache
from pathlib import Path
import os

class Settings(BaseSettings):
    # API Keys
    OPENAI_API_KEY: str = ""
    GEMINI_API_KEY: str = ""
    CLAUDE_API_KEY: str = ""
    # OLLAMA_API_URL: str = "http://localhost:11434"
    
    # Search API Keys
    GOOGLE_PLACES_API_KEY: str = ""
    TRIPADVISOR_API_KEY: str = ""
    BOOKING_API_KEY: str = ""
    
    # Agent Service URLs
    ORCHESTRATOR_URL: str = "http://localhost:8000"
    SEARCH_AGENT_URL: str = "http://localhost:8001"
    ENTERTAINMENT_AGENT_URL: str = "http://localhost:8002"
    MEAL_AGENT_URL: str = "http://localhost:8003"
    STAY_AGENT_URL: str = "http://localhost:8004"
    
    # Model Configurations
    DEFAULT_MODEL: str = "gpt-4"
    TEMPERATURE: float = 0.7
    MAX_TOKENS: int = 2000
    
    # Search Configurations
    SEARCH_CACHE_DURATION: int = 24  # hours
    MAX_RESULTS_PER_CATEGORY: int = 10
    SEARCH_TIMEOUT: int = 30  # seconds
    
    # Application Settings
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()

# Constants
AGENT_PORTS = {
    "orchestrator": 8000,
    "search": 8001,
    "entertainment": 8002,
    "meal": 8003,
    "stay": 8004
}

def get_project_root() -> Path:
    """Get the project root directory."""
    return Path(__file__).parent.parent

# Create settings instance
settings = get_settings() 