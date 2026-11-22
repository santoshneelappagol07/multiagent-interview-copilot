from app.llm.base import BaseLLMProvider
import google.generativeai as genai
from typing import AsyncGenerator
import logging

logger = logging.getLogger("ai_voice_copilot.llm.gemini")

class GeminiProvider(BaseLLMProvider):
    def __init__(self, api_key: str):
        super().__init__(api_key=api_key)
        if api_key:
            genai.configure(api_key=api_key)

    def is_available(self) -> bool:
        return bool(self.api_key and self.api_key != "your_gemini_api_key_here")

    async def generate(self, prompt: str, system_prompt: str, model: str = "gemini-2.0-flash", temperature: float = 0.7) -> str:
        if not self.is_available():
            raise ValueError("Gemini API key is not configured")
        
        gen_model = genai.GenerativeModel(
            model_name=model,
            system_instruction=system_prompt,
            generation_config={"temperature": temperature}
        )
        response = await gen_model.generate_content_async(prompt)
        return response.text

    async def generate_stream(
        self, prompt: str, system_prompt: str, model: str = "gemini-2.0-flash", temperature: float = 0.7
    ) -> AsyncGenerator[str, None]:
        if not self.is_available():
            raise ValueError("Gemini API key is not configured")

        gen_model = genai.GenerativeModel(
            model_name=model,
            system_instruction=system_prompt,
            generation_config={"temperature": temperature}
        )
        response = await gen_model.generate_content_async(prompt, stream=True)
        async for chunk in response:
            if chunk.text:
                yield chunk.text
