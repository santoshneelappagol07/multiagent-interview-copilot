from enum import Enum
from typing import List, Tuple

class AnswerMode(str, Enum):
    FAST = "fast"
    REASONING = "reasoning"
    RESEARCH = "research"

class RoutingStrategy:
    """Defines ordered priority chains for each mode"""
    CHAINS = {
        AnswerMode.FAST: [
            ("groq", "llama-3.1-8b-instant"),
            ("cerebras", "llama3.1-8b"),
            ("gemini", "gemini-2.0-flash"),
            ("ollama", "llama3.1"),
        ],
        AnswerMode.REASONING: [
            ("gemini", "gemini-2.0-flash"),
            ("groq", "llama-3.3-70b-versatile"),
            ("cerebras", "llama3.1-70b"),
            ("ollama", "llama3.1"),
        ],
        AnswerMode.RESEARCH: [
            ("groq", "llama-3.3-70b-versatile"),
            ("gemini", "gemini-2.0-flash"),
            ("cerebras", "llama3.1-70b"),
            ("ollama", "llama3.1"),
        ],
    }

    @classmethod
    def get_chain(cls, mode: AnswerMode) -> List[Tuple[str, str]]:
        return cls.CHAINS.get(mode, cls.CHAINS[AnswerMode.FAST])
