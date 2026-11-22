from dataclasses import dataclass, field
from typing import Dict, Any
import time

@dataclass
class PerformanceMetrics:
    stt_latency_ms: float = 220.0
    retrieval_latency_ms: float = 180.0
    llm_first_token_ms: float = 850.0
    total_answer_ms: float = 1450.0
    recent_answers_count: int = 0

class MetricsCollector:
    def __init__(self):
        self.metrics = PerformanceMetrics()

    def record_answer_latency(self, retrieval_ms: float, first_token_ms: float, total_ms: float):
        self.metrics.retrieval_latency_ms = round(retrieval_ms, 1)
        self.metrics.llm_first_token_ms = round(first_token_ms, 1)
        self.metrics.total_answer_ms = round(total_ms, 1)
        self.metrics.recent_answers_count += 1

    def get_summary(self) -> Dict[str, Any]:
        return {
            "sttLatencyMs": self.metrics.stt_latency_ms,
            "retrievalLatencyMs": self.metrics.retrieval_latency_ms,
            "llmFirstTokenMs": self.metrics.llm_first_token_ms,
            "totalAnswerMs": self.metrics.total_answer_ms,
        }

metrics_collector = MetricsCollector()
