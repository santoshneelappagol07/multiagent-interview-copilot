from app.llm.base import BaseLLMProvider
from openai import AsyncOpenAI
from typing import AsyncGenerator
import logging

logger = logging.getLogger("ai_voice_copilot.llm.groq")

class GroqProvider(BaseLLMProvider):
    def __init__(self, api_key: str):
        super().__init__(api_key=api_key, base_url="https://api.groq.com/openai/v1")
        if self.is_available():
            self.client = AsyncOpenAI(api_key=api_key, base_url=self.base_url)
        else:
            self.client = None

    def is_available(self) -> bool:
        return bool(self.api_key and self.api_key != "your_groq_api_key_here")

    async def generate(self, prompt: str, system_prompt: str, model: str = "llama-3.1-8b-instant", temperature: float = 0.7) -> str:
        if not self.is_available():
            raise ValueError("Groq API key is not configured")

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
        self, prompt: str, system_prompt: str, model: str = "llama-3.1-8b-instant", temperature: float = 0.7
    ) -> AsyncGenerator[str, None]:
        if not self.is_available():
            raise ValueError("Groq API key is not configured")

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
