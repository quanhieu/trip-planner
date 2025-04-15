from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
import httpx
import json
import logging
from .config import settings

logger = logging.getLogger(__name__)

class AIClient(ABC):
    """Abstract base class for AI/LLM clients."""
    
    @abstractmethod
    async def generate(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """Generate a response from the AI model."""
        pass

    @abstractmethod
    async def generate_with_context(self, messages: List[Dict[str, str]], **kwargs) -> Dict[str, Any]:
        """Generate a response using conversation context."""
        pass

class OpenAIClient(AIClient):
    """OpenAI API client implementation."""
    
    def __init__(self):
        self.api_key = settings.OPENAI_API_KEY
        self.model = settings.DEFAULT_MODEL
        self.base_url = "https://api.openai.com/v1"
        
    async def generate(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """Generate a response using OpenAI's completion API."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": kwargs.get("model", self.model),
                        "messages": [{"role": "user", "content": prompt}],
                        "temperature": kwargs.get("temperature", settings.TEMPERATURE),
                        "max_tokens": kwargs.get("max_tokens", settings.MAX_TOKENS)
                    }
                )
                response.raise_for_status()
                result = response.json()
                return {
                    "text": result["choices"][0]["message"]["content"],
                    "model": result["model"],
                    "usage": result.get("usage", {})
                }
        except Exception as e:
            logger.error(f"OpenAI API call failed: {str(e)}")
            return {"error": str(e)}

    async def generate_with_context(self, messages: List[Dict[str, str]], **kwargs) -> Dict[str, Any]:
        """Generate a response using conversation context."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": kwargs.get("model", self.model),
                        "messages": messages,
                        "temperature": kwargs.get("temperature", settings.TEMPERATURE),
                        "max_tokens": kwargs.get("max_tokens", settings.MAX_TOKENS)
                    }
                )
                response.raise_for_status()
                result = response.json()
                return {
                    "text": result["choices"][0]["message"]["content"],
                    "model": result["model"],
                    "usage": result.get("usage", {})
                }
        except Exception as e:
            logger.error(f"OpenAI API call failed: {str(e)}")
            return {"error": str(e)}

class GeminiClient(AIClient):
    """Google Gemini API client implementation."""
    
    def __init__(self):
        self.api_key = settings.GEMINI_API_KEY
        self.base_url = "https://generativelanguage.googleapis.com/v1beta"
        
    async def generate(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """Generate a response using Gemini API."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/models/gemini-pro:generateContent",
                    params={"key": self.api_key},
                    json={
                        "contents": [{"parts": [{"text": prompt}]}],
                        "generationConfig": {
                            "temperature": kwargs.get("temperature", settings.TEMPERATURE),
                            "maxOutputTokens": kwargs.get("max_tokens", settings.MAX_TOKENS)
                        }
                    }
                )
                response.raise_for_status()
                result = response.json()
                return {
                    "text": result["candidates"][0]["content"]["parts"][0]["text"],
                    "model": "gemini-pro",
                    "usage": {}  # Gemini doesn't provide usage stats in the same way
                }
        except Exception as e:
            logger.error(f"Gemini API call failed: {str(e)}")
            return {"error": str(e)}

    async def generate_with_context(self, messages: List[Dict[str, str]], **kwargs) -> Dict[str, Any]:
        """Generate a response using conversation context."""
        try:
            # Convert messages to Gemini format
            contents = []
            for msg in messages:
                contents.append({
                    "role": "user" if msg["role"] == "user" else "model",
                    "parts": [{"text": msg["content"]}]
                })
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/models/gemini-pro:generateContent",
                    params={"key": self.api_key},
                    json={
                        "contents": contents,
                        "generationConfig": {
                            "temperature": kwargs.get("temperature", settings.TEMPERATURE),
                            "maxOutputTokens": kwargs.get("max_tokens", settings.MAX_TOKENS)
                        }
                    }
                )
                response.raise_for_status()
                result = response.json()
                return {
                    "text": result["candidates"][0]["content"]["parts"][0]["text"],
                    "model": "gemini-pro",
                    "usage": {}
                }
        except Exception as e:
            logger.error(f"Gemini API call failed: {str(e)}")
            return {"error": str(e)}

class ClaudeClient(AIClient):
    """Anthropic Claude API client implementation."""
    
    def __init__(self):
        self.api_key = settings.CLAUDE_API_KEY
        self.base_url = "https://api.anthropic.com/v1"
        
    async def generate(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """Generate a response using Claude API."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/messages",
                    headers={
                        "x-api-key": self.api_key,
                        "anthropic-version": "2023-06-01",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "claude-3-sonnet-20240229",
                        "messages": [{"role": "user", "content": prompt}],
                        "max_tokens": kwargs.get("max_tokens", settings.MAX_TOKENS),
                        "temperature": kwargs.get("temperature", settings.TEMPERATURE)
                    }
                )
                response.raise_for_status()
                result = response.json()
                return {
                    "text": result["content"][0]["text"],
                    "model": result["model"],
                    "usage": result.get("usage", {})
                }
        except Exception as e:
            logger.error(f"Claude API call failed: {str(e)}")
            return {"error": str(e)}

    async def generate_with_context(self, messages: List[Dict[str, str]], **kwargs) -> Dict[str, Any]:
        """Generate a response using conversation context."""
        try:
            # Convert messages to Claude format
            claude_messages = [
                {"role": msg["role"], "content": msg["content"]}
                for msg in messages
            ]
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/messages",
                    headers={
                        "x-api-key": self.api_key,
                        "anthropic-version": "2023-06-01",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "claude-3-sonnet-20240229",
                        "messages": claude_messages,
                        "max_tokens": kwargs.get("max_tokens", settings.MAX_TOKENS),
                        "temperature": kwargs.get("temperature", settings.TEMPERATURE)
                    }
                )
                response.raise_for_status()
                result = response.json()
                return {
                    "text": result["content"][0]["text"],
                    "model": result["model"],
                    "usage": result.get("usage", {})
                }
        except Exception as e:
            logger.error(f"Claude API call failed: {str(e)}")
            return {"error": str(e)}

class AIClientFactory:
    """Factory class for creating AI clients."""
    
    @staticmethod
    def create_client(provider: str = "openai") -> AIClient:
        """Create an AI client instance based on the provider."""
        if provider == "openai":
            return OpenAIClient()
        elif provider == "gemini":
            return GeminiClient()
        elif provider == "claude":
            return ClaudeClient()
        else:
            raise ValueError(f"Unsupported AI provider: {provider}")

# Helper function to get default AI client
def get_default_ai_client() -> AIClient:
    """Get the default AI client based on configuration."""
    # You can modify this logic based on your preferences
    if settings.OPENAI_API_KEY:
        return AIClientFactory.create_client("openai")
    elif settings.GEMINI_API_KEY:
        return AIClientFactory.create_client("gemini")
    elif settings.CLAUDE_API_KEY:
        return AIClientFactory.create_client("claude")
    else:
        raise ValueError("No AI provider API keys configured")