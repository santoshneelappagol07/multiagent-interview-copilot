from app.agents.base import BaseAgent
import re
from typing import Dict, Any

class QuestionDetectionAgent(BaseAgent):
    """
    Analyzes transcribed interviewer speech to detect technical interview questions,
    distinguishing interviewer questions from remarks, greetings, or acknowledgments.
    """
    def __init__(self):
        super().__init__(
            name="QuestionDetectionAgent",
            description="Analyzes transcribed interviewer speech to detect questions and extract target query."
        )
        self.question_starters = re.compile(
            r'\b('
            r'can you|could you|explain|tell me about|how do you|what is|what are|why did|why do|'
            r'walk me through|how would you|have you worked|briefly describe|what is the difference|'
            r'how does|what happens when|give me an example|suppose you have|let\'s say you have|'
            r'in your project|how did you implement|how to handle'
            r')\b',
            re.IGNORECASE
        )

    async def run(self, transcript_text: str) -> Dict[str, Any]:
        text = transcript_text.strip()
        if not text:
            return {"is_question": False, "detected_question": None, "confidence": 0.0}

        has_question_mark = "?" in text
        has_question_pattern = bool(self.question_starters.search(text))

        # Check for conversational acknowledgement that is NOT a question
        is_mere_ack = bool(re.match(r'^(okay|yes|right|yeah|sure|got it|cool|thank you|thanks)\.?$', text, re.I))

        is_question = (has_question_mark or has_question_pattern) and not is_mere_ack
        confidence = 0.95 if (has_question_mark and has_question_pattern) else (0.8 if has_question_pattern else (0.7 if has_question_mark else 0.0))

        return {
            "is_question": is_question,
            "detected_question": text if is_question else None,
            "confidence": confidence,
        }

question_detector = QuestionDetectionAgent()
