import pytest
from app.llm.factory import llm_factory
from app.routing.strategy import AnswerMode
from app.routing.router import model_router

def test_llm_factory_providers():
    providers = llm_factory.list_providers()
    assert len(providers) >= 4
    names = [p["id"] for p in providers]
    assert "groq" in names
    assert "cerebras" in names
    assert "gemini" in names
    assert "ollama" in names

def test_model_router():
    provider, name, model = model_router.select_provider_and_model(AnswerMode.FAST)
    assert name in ["groq", "cerebras", "gemini", "ollama"]
    assert model is not None
