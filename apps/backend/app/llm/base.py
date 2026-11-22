from abc import ABC, abstractmethod
from typing import AsyncGenerator, Dict, Any, List
from dataclasses import dataclass

@dataclass
class LLMResponse:
    text: str
    model: str
    provider: str
    latency_ms: float
    sources: List[str]

class BaseLLMProvider(ABC):
    def __init__(self, api_key: str = "", base_url: str = ""):
        self.api_key = api_key
        self.base_url = base_url

    @abstractmethod
    async def generate(self, prompt: str, system_prompt: str, model: str, temperature: float = 0.7) -> str:
        """Generate complete answer"""
        pass

    @abstractmethod
    async def generate_stream(
        self, prompt: str, system_prompt: str, model: str, temperature: float = 0.7
    ) -> AsyncGenerator[str, None]:
        """Stream answer tokens"""
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """Check if provider is configured and available"""
        pass
