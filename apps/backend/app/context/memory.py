from typing import List, Dict, Any, Optional
from collections import deque
import time
import logging

logger = logging.getLogger("ai_voice_copilot.context.memory")

class ConversationMemoryManager:
    """
    Maintains a rolling window of recent interview questions and generated answers.
    Ensures that every new question carries the full context of the preceding 2-3 Q&A exchanges
    for natural conversation continuity and follow-up understanding.
    """
    def __init__(self, max_history: int = 15):
        self._history: deque = deque(maxlen=max_history)

    def record_turn(self, question: str, answer: str, mode: str = "fast", sources: Optional[List[str]] = None):
        if not question or not answer:
            return
        entry = {
            "question": question.strip(),
            "answer": answer.strip(),
            "mode": mode,
            "sources": sources or [],
            "timestamp": int(time.time() * 1000),
        }
        self._history.append(entry)
        logger.info(f"Recorded Q&A turn into memory. Current history length: {len(self._history)}")

    def get_recent_turns(self, count: int = 3) -> List[Dict[str, Any]]:
        """
        Retrieves the last `count` (default 3) Q&A exchanges.
        """
        return list(self._history)[-count:]

    def clear(self):
        """Clears memory (e.g. when starting a fresh interview session)."""
        self._history.clear()
        logger.info("Cleared conversation Q&A history.")

    def get_turn_count(self) -> int:
        return len(self._history)

memory_manager = ConversationMemoryManager()
