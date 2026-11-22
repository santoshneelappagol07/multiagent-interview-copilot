from app.config import settings
from app.llm.base import BaseLLMProvider
from app.llm.gemini_provider import GeminiProvider
from app.llm.groq_provider import GroqProvider
from app.llm.cerebras_provider import CerebrasProvider
from app.llm.openrouter_provider import OpenRouterProvider
from app.llm.ollama_provider import OllamaProvider
from typing import Dict, List, Any

class LLMFactory:
    def __init__(self):
        self._providers: Dict[str, BaseLLMProvider] = {
            "gemini": GeminiProvider(api_key=settings.gemini_api_key),
            "groq": GroqProvider(api_key=settings.groq_api_key),
            "cerebras": CerebrasProvider(api_key=settings.cerebras_api_key),
            "openrouter": OpenRouterProvider(api_key=settings.openrouter_api_key),
            "ollama": OllamaProvider(base_url=settings.ollama_base_url),
        }

    def get_provider(self, name: str) -> BaseLLMProvider:
        provider = self._providers.get(name.lower())
        if not provider:
            raise ValueError(f"Unknown LLM provider: {name}")
        return provider

    def list_providers(self) -> List[Dict[str, Any]]:
        return [
            {
                "name": "Google Gemini",
                "id": "gemini",
                "isEnabled": self._providers["gemini"].is_available(),
                "models": ["gemini-2.0-flash", "gemini-1.5-flash"],
                "role": "Reasoning Mode Primary",
            },
            {
                "name": "Groq Cloud",
                "id": "groq",
                "isEnabled": self._providers["groq"].is_available(),
                "models": ["llama-3.1-8b-instant", "llama-3.3-70b-versatile"],
                "role": "Fast Mode Primary (<1s)",
            },
            {
                "name": "OpenRouter (Free Tier)",
                "id": "openrouter",
                "isEnabled": self._providers["openrouter"].is_available(),
                "models": ["meta-llama/llama-3.1-8b-instruct:free", "google/gemini-2.0-flash-exp:free"],
                "role": "100% Free Fallback (No Card Required)",
            },
            {
                "name": "Cerebras Cloud",
                "id": "cerebras",
                "isEnabled": self._providers["cerebras"].is_available(),
                "models": ["llama3.1-8b", "llama3.1-70b"],
                "role": "Optional Fast Provider",
            },
            {
                "name": "Ollama (Local)",
                "id": "ollama",
                "isEnabled": True,
                "models": ["llama3.1", "mistral"],
                "role": "Offline Fallback",
            },
        ]

llm_factory = LLMFactory()
