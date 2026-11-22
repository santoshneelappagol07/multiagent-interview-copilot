from enum import Enum
from typing import List, Tuple

class AnswerMode(str, Enum):
    FAST = "fast"
    REASONING = "reasoning"
    RESEARCH = "research"

class RoutingStrategy:
    """Defines ordered priority chains for each mode with verified active free models"""
    CHAINS = {
        AnswerMode.FAST: [
            ("groq", "openai/gpt-oss-20b"),
            ("openrouter", "meta-llama/llama-3.1-8b-instruct:free"),
            ("gemini", "gemini-3.8-flash"),
            ("groq", "qwen/qwen3.8-27b"),
            ("ollama", "llama3.1"),
        ],
        AnswerMode.REASONING: [
            ("groq", "openai/gpt-oss-120b"),
            ("gemini", "gemini-3.8-flash"),
            ("openrouter", "google/gemini-2.0-flash-exp:free"),
            ("groq", "openai/gpt-oss-20b"),
            ("ollama", "llama3.1"),
        ],
        AnswerMode.RESEARCH: [
            ("groq", "openai/gpt-oss-120b"),
            ("gemini", "gemini-3.8-flash"),
            ("openrouter", "meta-llama/llama-3.1-8b-instruct:free"),
            ("ollama", "llama3.1"),
        ],
    }

    @classmethod
    def get_chain(cls, mode: AnswerMode) -> List[Tuple[str, str]]:
        return cls.CHAINS.get(mode, cls.CHAINS[AnswerMode.FAST])
