from typing import List
import logging

logger = logging.getLogger("ai_voice_copilot.rag.embeddings")

class EmbeddingService:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model_name = model_name
        self._model = None

    def _load_model(self):
        if self._model is None:
            try:
                from sentence_transformers import SentenceTransformer
                logger.info(f"Loading embedding model: {self.model_name}")
                self._model = SentenceTransformer(self.model_name)
            except Exception as e:
                logger.warning(f"Could not load SentenceTransformer ({e}). Using lightweight fallback.")
                self._model = "fallback"

    def embed_text(self, text: str) -> List[float]:
        self._load_model()
        if self._model != "fallback":
            return self._model.encode(text).tolist()
        # Deterministic lightweight pseudo-embedding for testing if torch unavailable
        return [float((hash(text + str(i)) % 1000) / 1000.0) for i in range(384)]

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        self._load_model()
        if self._model != "fallback":
            return self._model.encode(texts).tolist()
        return [self.embed_text(t) for t in texts]

embedding_service = EmbeddingService()
