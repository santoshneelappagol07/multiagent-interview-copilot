import pytest
from app.routing.strategy import AnswerMode, RoutingStrategy

def test_routing_chains():
    fast_chain = RoutingStrategy.get_chain(AnswerMode.FAST)
    assert fast_chain[0][0] == "groq"
    reasoning_chain = RoutingStrategy.get_chain(AnswerMode.REASONING)
    assert reasoning_chain[0][0] == "gemini"
