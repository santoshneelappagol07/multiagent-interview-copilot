from typing import List, Dict, Any
from collections import deque
import time

class TranscriptManager:
    def __init__(self, max_history: int = 50):
        self.history = deque(maxlen=max_history)

    def add_segment(self, text: str, is_partial: bool = False, timestamp: int = None):
        if not text.strip():
            return
        entry = {
            "text": text.strip(),
            "is_partial": is_partial,
            "timestamp": timestamp or int(time.time() * 1000),
            "is_question": "?" in text,
        }
        if not is_partial:
            self.history.append(entry)
        return entry

    def get_recent_context(self, count: int = 5) -> List[str]:
        return [item["text"] for item in list(self.history)[-count:]]

transcript_manager = TranscriptManager()
