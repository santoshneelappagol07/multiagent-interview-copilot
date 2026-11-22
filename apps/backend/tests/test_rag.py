import pytest
from app.rag.chunker import text_chunker
from app.rag.embeddings import embedding_service

def test_text_chunker():
    sample_text = "Paragraph 1 with some details.\n\nParagraph 2 with more architectural design."
    chunks = text_chunker.chunk(sample_text)
    assert len(chunks) >= 1
    assert "Paragraph 1" in chunks[0]["text"]

def test_embedding_service():
    text = "FastAPI backend performance with async database"
    emb = embedding_service.embed_text(text)
    assert isinstance(emb, list)
    assert len(emb) > 0
