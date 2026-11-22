from app.agents.base import BaseAgent
from app.rag.retriever import rag_retriever
from typing import List, Dict, Any

class DocumentRetrievalAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="DocumentRetrievalAgent",
            description="Executes mandatory local semantic search against uploaded resume and project documents."
        )

    async def run(self, query: str) -> List[Dict[str, Any]]:
        return await rag_retriever.retrieve(query=query, top_k=4)

document_retrieval_agent = DocumentRetrievalAgent()
