from app.agents.base import BaseAgent
from app.context.manager import context_manager
from app.routing.router import model_router
from app.routing.strategy import AnswerMode
from app.llm.base import LLMResponse
from typing import Dict, Any, List, Optional, AsyncGenerator
import time
import logging

logger = logging.getLogger("ai_voice_copilot.agents.answer_generator")

class AnswerGenerationAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="AnswerGenerationAgent",
            description="Synthesizes candidate context, RAG knowledge, and generates answers using routed LLM."
        )

    async def run(
        self,
        question: str,
        conversation_context: List[str],
        document_chunks: List[Dict[str, Any]],
        mode: AnswerMode,
        recent_qa_turns: Optional[List[Dict[str, Any]]] = None,
    ) -> LLMResponse:
        start_time = time.perf_counter()

        # Build prompt incorporating mandatory knowledge base and previous 2-3 Q&A pairs
        prompt = context_manager.build_generation_prompt(
            question=question,
            conversation_context=conversation_context,
            document_chunks=document_chunks,
            mode=mode.value,
            recent_qa_turns=recent_qa_turns,
        )
        system_prompt = context_manager.get_system_prompt()

        provider, provider_name, model_name = model_router.select_provider_and_model(mode)
        raw_text = await provider.generate(prompt=prompt, system_prompt=system_prompt, model=model_name)

        latency_ms = (time.perf_counter() - start_time) * 1000.0

        sources = list({
            c.get("metadata", {}).get("filename", "Uploaded Document")
            for c in document_chunks
            if "metadata" in c
        })

        return LLMResponse(
            text=raw_text,
            model=model_name,
            provider=provider_name,
            latency_ms=latency_ms,
            sources=sources,
        )

    async def run_stream(
        self,
        question: str,
        conversation_context: List[str],
        document_chunks: List[Dict[str, Any]],
        mode: AnswerMode,
        recent_qa_turns: Optional[List[Dict[str, Any]]] = None,
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Streams answer tokens one by one with metadata events for real-time UI rendering.
        Yields dicts with {"type": "token" | "meta", ...}
        """
        start_time = time.perf_counter()
        first_token_time = None

        prompt = context_manager.build_generation_prompt(
            question=question,
            conversation_context=conversation_context,
            document_chunks=document_chunks,
            mode=mode.value,
            recent_qa_turns=recent_qa_turns,
        )
        system_prompt = context_manager.get_system_prompt()

        provider, provider_name, model_name = model_router.select_provider_and_model(mode)
        sources = list({
            c.get("metadata", {}).get("filename", "Uploaded Document")
            for c in document_chunks
            if "metadata" in c
        })

        yield {
            "type": "meta",
            "provider": provider_name,
            "model": model_name,
            "sources": sources,
            "contextCarriedTurns": len(recent_qa_turns) if recent_qa_turns else 0,
        }

        try:
            async for chunk in provider.generate_stream(
                prompt=prompt,
                system_prompt=system_prompt,
                model=model_name
            ):
                if first_token_time is None:
                    first_token_time = time.perf_counter()
                yield {"type": "token", "token": chunk}
        except Exception as e:
            logger.warning(f"Streaming failed with {provider_name}: {e}. Attempting fallback...")
            yield {"type": "token", "token": f"\n\n*[Streaming error from {provider_name}: {str(e)}]*"}

        total_latency = (time.perf_counter() - start_time) * 1000.0
        first_token_ms = ((first_token_time - start_time) * 1000.0) if first_token_time else total_latency

        yield {
            "type": "done",
            "firstTokenMs": round(first_token_ms, 1),
            "totalMs": round(total_latency, 1),
        }

answer_generator = AnswerGenerationAgent()
