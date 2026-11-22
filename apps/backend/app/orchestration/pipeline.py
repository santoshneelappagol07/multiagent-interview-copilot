from typing import Dict, Any, List
from app.routing.strategy import AnswerMode

class OrchestrationPipeline:
    @staticmethod
    def get_pipeline_config(mode: AnswerMode) -> Dict[str, Any]:
        if mode == AnswerMode.FAST:
            return {
                "top_k_chunks": 3,
                "parallel_context": True,
                "max_tokens": 200,
            }
        elif mode == AnswerMode.REASONING:
            return {
                "top_k_chunks": 5,
                "parallel_context": True,
                "max_tokens": 600,
            }
        else:
            return {
                "top_k_chunks": 8,
                "parallel_context": False,
                "max_tokens": 1200,
            }
