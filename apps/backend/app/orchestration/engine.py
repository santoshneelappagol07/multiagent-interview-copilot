import time
from typing import Dict, Any, List, Optional, AsyncGenerator
from app.agents.document_retriever import document_retrieval_agent
from app.agents.answer_generator import answer_generator
from app.transcripts.manager import transcript_manager
from app.context.memory import memory_manager
from app.routing.strategy import AnswerMode
from app.monitoring.metrics import metrics_collector
import logging

logger = logging.getLogger("ai_voice_copilot.orchestration.engine")

class MultiAgentOrchestrator:
    """
    Coordinates the multi-agent question processing:
    1. Retrieve recent conversation history and PREVIOUS 2-3 Q&A TURNS
    2. MANDATORY: Search document knowledge base (Resume / Past Transcripts / System Design notes)
    3. Route to fastest available LLM (Groq / Cerebras / Gemini)
    4. Generate and stream answer
    5. Save generated answer into multi-turn memory for subsequent question context
    """
    async def process_question(
        self,
        question: str,
        mode: AnswerMode,
        history_override: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        overall_start = time.perf_counter()

        # Step 1: Recent transcript context & previous 2-3 Q&A turns
        recent_transcript = transcript_manager.get_recent_context(count=4)
        recent_qa = history_override if history_override is not None else memory_manager.get_recent_turns(count=3)

        # Step 2: Mandatory RAG Retrieval
        rag_start = time.perf_counter()
        doc_chunks = await document_retrieval_agent.run(question)
        rag_duration_ms = (time.perf_counter() - rag_start) * 1000.0

        # Step 3: LLM Answer Generation with conversation context
        llm_start = time.perf_counter()
        response = await answer_generator.run(
            question=question,
            conversation_context=recent_transcript,
            document_chunks=doc_chunks,
            mode=mode,
            recent_qa_turns=recent_qa,
        )
        llm_duration_ms = (time.perf_counter() - llm_start) * 1000.0
        total_duration_ms = (time.perf_counter() - overall_start) * 1000.0

        # Step 4: Record this Q&A exchange into memory for future questions
        memory_manager.record_turn(
            question=question,
            answer=response.text,
            mode=mode.value,
            sources=response.sources
        )

        # Step 5: Record performance telemetry
        metrics_collector.record_answer_latency(
            retrieval_ms=rag_duration_ms,
            first_token_ms=llm_duration_ms * 0.35,
            total_ms=total_duration_ms,
        )

        logger.info(
            f"Processed answer in {total_duration_ms:.1f}ms (RAG: {rag_duration_ms:.1f}ms, "
            f"LLM: {llm_duration_ms:.1f}ms, ContextTurns: {len(recent_qa)}) via {response.provider}"
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
            "contextCarriedCount": len(recent_qa),
            "createdAt": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        }

    async def process_question_stream(
        self,
        question: str,
        mode: AnswerMode,
        history_override: Optional[List[Dict[str, Any]]] = None
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Streaming workflow with multi-turn context carrying.
        Yields real-time events: 'status', 'meta', 'token', and 'done'.
        """
        overall_start = time.perf_counter()

        recent_transcript = transcript_manager.get_recent_context(count=4)
        recent_qa = history_override if history_override is not None else memory_manager.get_recent_turns(count=3)

        rag_start = time.perf_counter()
        yield {
            "type": "status",
            "stage": "retrieving_rag",
            "message": f"Consulting knowledge base with {len(recent_qa)} prior Q&A turns in context..."
        }
        doc_chunks = await document_retrieval_agent.run(question)
        rag_duration_ms = (time.perf_counter() - rag_start) * 1000.0
        yield {
            "type": "status",
            "stage": "rag_complete",
            "retrievalMs": round(rag_duration_ms, 1),
            "chunksFound": len(doc_chunks),
            "contextTurns": len(recent_qa),
        }

        accumulated_tokens: List[str] = []
        captured_sources: List[str] = []

        async for event in answer_generator.run_stream(
            question=question,
            conversation_context=recent_transcript,
            document_chunks=doc_chunks,
            mode=mode,
            recent_qa_turns=recent_qa,
        ):
            if event["type"] == "token":
                accumulated_tokens.append(event["token"])
            elif event["type"] == "meta":
                captured_sources = event.get("sources", [])
            elif event["type"] == "done":
                total_duration_ms = (time.perf_counter() - overall_start) * 1000.0
                first_token_ms = event.get("firstTokenMs", total_duration_ms * 0.4)
                metrics_collector.record_answer_latency(
                    retrieval_ms=rag_duration_ms,
                    first_token_ms=first_token_ms,
                    total_ms=total_duration_ms,
                )
                event["totalDurationMs"] = round(total_duration_ms, 1)

                # Record turn into memory for subsequent questions
                full_answer = "".join(accumulated_tokens)
                if full_answer.strip():
                    memory_manager.record_turn(
                        question=question,
                        answer=full_answer,
                        mode=mode.value,
                        sources=captured_sources
                    )

            yield event

orchestrator = MultiAgentOrchestrator()
