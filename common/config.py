from typing import Dict, Any
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
    
    # LLM Base URLs
    OPENAI_BASE_URL: str = "https://api.openai.com/v1"
    GEMINI_BASE_URL: str = "https://generativelanguage.googleapis.com/v1beta"
    CLAUDE_BASE_URL: str = "https://api.anthropic.com/v1"
    
    # Search API Keys
    GOOGLE_API_KEY: str = ""
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
    MODEL_CONFIGS: Dict[str, Dict[str, Any]] = {
        "gpt-4o": {
            "complexity": "HIGH",
            "context_length": 8000,
            "cost_per_token": 0.03,
            "strengths": ["complex_reasoning", "creative_tasks", "detailed_planning"]
        },
        "gpt-4o-mini": {
            "complexity": "MEDIUM",
            "context_length": 4000,
            "cost_per_token": 0.015,
            "strengths": ["complex_reasoning", "basic_planning"]
        },
        "gemini-2.0-flash": {
            "complexity": "MEDIUM",
            "context_length": 4000,
            "cost_per_token": 0.01,
            "strengths": ["factual_queries", "basic_planning", "information_extraction"]
        },
        "claude-3.7-sonnet": {
            "complexity": "HIGH",
            "context_length": 6000,
            "cost_per_token": 0.02,
            "strengths": ["analysis", "structured_output", "travel_planning"]
        }
    }
    
    # Default Model Settings
    DEFAULT_TEMPERATURE: float = 0.7
    DEFAULT_MAX_TOKENS: int = 2000
    DEFAULT_MODEL: str = "gpt-4o"  # Default model to use
    
    # Search Configurations
    SEARCH_CACHE_DURATION: int = 24  # hours
    MAX_RESULTS_PER_CATEGORY: int = 10
    SEARCH_TIMEOUT: int = 30  # seconds
    
    # Application Settings
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"
    
    # ADK Configuration
    ADK_CONFIG: Dict[str, Any] = {
        "DEFAULT_MODEL": "gpt-4o",  # Updated to match our default model
        "TEMPERATURE": 0.7,
        "MAX_TOKENS": 2000,
        "USE_TOOLS": True
    }
    
    # A2A Protocol Configuration
    A2A_CONFIG: Dict[str, Any] = {
        "MAX_RETRIES": 3,
        "TIMEOUT": 60,
        "CIRCUIT_BREAKER_THRESHOLD": 5
    }
    
    # Agent-specific settings
    AGENT_SETTINGS: Dict[str, Dict[str, Any]] = {
        "search": {
            "max_results": 10,
            "search_providers": ["google"]
        },
        "entertainment": {
            "max_suggestions": 5
        }
        # ... other agent settings
    }
    
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