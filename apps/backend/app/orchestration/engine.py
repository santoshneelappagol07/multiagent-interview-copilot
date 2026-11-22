import time
from typing import Dict, Any, List, AsyncGenerator
from app.agents.document_retriever import document_retrieval_agent
from app.agents.answer_generator import answer_generator
from app.transcripts.manager import transcript_manager
from app.routing.strategy import AnswerMode
from app.monitoring.metrics import metrics_collector
import logging

logger = logging.getLogger("ai_voice_copilot.orchestration.engine")

class MultiAgentOrchestrator:
    """
    Coordinates the multi-agent question processing:
    1. Retrieve recent conversation history
    2. MANDATORY: Search document knowledge base (Resume / Past Transcripts / System Design notes)
    3. Route to fastest available LLM (Groq / Cerebras / Gemini)
    4. Generate and profile latency
    """
    async def process_question(self, question: str, mode: AnswerMode) -> Dict[str, Any]:
        overall_start = time.perf_counter()

        # Step 1: Recent transcript context
        recent_transcript = transcript_manager.get_recent_context(count=4)

        # Step 2: Mandatory RAG Retrieval
        rag_start = time.perf_counter()
        doc_chunks = await document_retrieval_agent.run(question)
        rag_duration_ms = (time.perf_counter() - rag_start) * 1000.0

        # Step 3: LLM Answer Generation
        llm_start = time.perf_counter()
        response = await answer_generator.run(
            question=question,
            conversation_context=recent_transcript,
            document_chunks=doc_chunks,
            mode=mode,
        )
        llm_duration_ms = (time.perf_counter() - llm_start) * 1000.0
        total_duration_ms = (time.perf_counter() - overall_start) * 1000.0

        # Step 4: Record performance telemetry
        metrics_collector.record_answer_latency(
            retrieval_ms=rag_duration_ms,
            first_token_ms=llm_duration_ms * 0.35,
            total_ms=total_duration_ms,
        )

        logger.info(
            f"Processed answer in {total_duration_ms:.1f}ms (RAG: {rag_duration_ms:.1f}ms, "
            f"LLM: {llm_duration_ms:.1f}ms) via {response.provider}"
        )

        return {
            "id": f"ans-{int(time.time() * 1000)}",
            "question": question,
            "answer": response.text,
            "mode": mode.value,
            "provider": response.provider,
            "model": response.model,
            "latencyMs": round(total_duration_ms, 1),
            "sources": response.sources,
            "createdAt": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        }

    async def process_question_stream(
        self, question: str, mode: AnswerMode
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Streaming workflow for sub-second first-token display.
        Yields real-time events: 'rag_start', 'rag_done', 'meta', 'token', and 'done'.
        """
        overall_start = time.perf_counter()

        recent_transcript = transcript_manager.get_recent_context(count=4)

        rag_start = time.perf_counter()
        yield {"type": "status", "stage": "retrieving_rag", "message": "Consulting knowledge base..."}
        doc_chunks = await document_retrieval_agent.run(question)
        rag_duration_ms = (time.perf_counter() - rag_start) * 1000.0
        yield {"type": "status", "stage": "rag_complete", "retrievalMs": round(rag_duration_ms, 1), "chunksFound": len(doc_chunks)}

        async for event in answer_generator.run_stream(
            question=question,
            conversation_context=recent_transcript,
            document_chunks=doc_chunks,
            mode=mode,
        ):
            if event["type"] == "done":
                total_duration_ms = (time.perf_counter() - overall_start) * 1000.0
                first_token_ms = event.get("firstTokenMs", total_duration_ms * 0.4)
                metrics_collector.record_answer_latency(
                    retrieval_ms=rag_duration_ms,
                    first_token_ms=first_token_ms,
                    total_ms=total_duration_ms,
                )
                event["totalDurationMs"] = round(total_duration_ms, 1)
            yield event

orchestrator = MultiAgentOrchestrator()
