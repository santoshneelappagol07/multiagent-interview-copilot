from typing import List, Dict, Any
from app.embeddings.store import vector_store
from app.rag.embeddings import embedding_service
import logging

logger = logging.getLogger("ai_voice_copilot.rag.retriever")

class MandatoryRAGRetriever:
    """
    Guarantees mandatory document retrieval consultation for EVERY question.
    Searches local ChromaDB vector index for relevant resume/project sections.
    """
    def __init__(self):
        self.store = vector_store
        self.embedder = embedding_service

    async def retrieve(self, query: str, top_k: int = 4) -> List[Dict[str, Any]]:
        logger.info(f"Executing mandatory RAG retrieval for query: {query[:80]}...")
        query_embedding = self.embedder.embed_text(query)
        results = self.store.search(query_embedding=query_embedding, top_k=top_k)

        # Filter by minimum relevance threshold
        filtered = [r for r in results if r.get("score", 0) >= 0.35]
        logger.info(f"Mandatory RAG retrieved {len(filtered)} relevant knowledge chunks.")
        return filtered

rag_retriever = MandatoryRAGRetriever()
