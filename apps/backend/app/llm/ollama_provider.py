from app.llm.base import BaseLLMProvider
from openai import AsyncOpenAI
from typing import AsyncGenerator
import logging

logger = logging.getLogger("ai_voice_copilot.llm.ollama")

class OllamaProvider(BaseLLMProvider):
    def __init__(self, base_url: str = "http://localhost:11434/v1"):
        super().__init__(api_key="ollama", base_url=base_url)
        self.client = AsyncOpenAI(api_key="ollama", base_url=self.base_url)

    def is_available(self) -> bool:
        return True

    async def generate(self, prompt: str, system_prompt: str, model: str = "llama3.1", temperature: float = 0.7) -> str:
        response = await self.client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
            temperature=temperature,
        )
        return response.choices[0].message.content or ""

    async def generate_stream(
        self, prompt: str, system_prompt: str, model: str = "llama3.1", temperature: float = 0.7
    ) -> AsyncGenerator[str, None]:
        stream = await self.client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
            temperature=temperature,
            stream=True,
        )
        async for chunk in stream:
            content = chunk.choices[0].delta.content
            if content:
                yield content
