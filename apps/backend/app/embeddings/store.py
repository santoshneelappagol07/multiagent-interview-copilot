import chromadb
from pathlib import Path
from typing import List, Dict, Any
from app.config import settings
import logging

logger = logging.getLogger("ai_voice_copilot.vector_store")

class ChromaVectorStore:
    def __init__(self, persist_dir: str = None):
        target_dir = persist_dir or settings.vector_store_path
        self.persist_dir = Path(target_dir).resolve()
        self.persist_dir.mkdir(parents=True, exist_ok=True)
        self.client = chromadb.PersistentClient(path=str(self.persist_dir))
        self.collection = self.client.get_or_create_collection(
            name="copilot_documents",
            metadata={"hnsw:space": "cosine"}
        )

    def add_chunks(
        self,
        doc_id: str,
        chunks: List[str],
        embeddings: List[List[float]],
        metadatas: List[Dict[str, Any]],
    ):
        ids = [f"{doc_id}_{i}" for i in range(len(chunks))]
        self.collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=chunks,
            metadatas=metadatas,
        )
        logger.info(f"Indexed {len(chunks)} chunks for document {doc_id}")

    def search(self, query_embedding: List[float], top_k: int = 5) -> List[Dict[str, Any]]:
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            include=["documents", "metadatas", "distances"]
        )

        output = []
        if results and results.get("documents"):
            docs = results["documents"][0]
            metas = results["metadatas"][0] if results.get("metadatas") else []
            dists = results["distances"][0] if results.get("distances") else []

            for doc, meta, dist in zip(docs, metas, dists):
                output.append({
                    "text": doc,
                    "metadata": meta,
                    "score": 1.0 - dist if dist is not None else 0.85,
                })

        return output

    def delete_document(self, doc_id: str):
        self.collection.delete(where={"doc_id": doc_id})
        logger.info(f"Deleted vector chunks for document {doc_id}")

vector_store = ChromaVectorStore()
