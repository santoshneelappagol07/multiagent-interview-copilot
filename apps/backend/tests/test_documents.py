import pytest
from app.documents.processor import TextNormalizer

def test_text_normalizer():
    raw = "Hello   world!\r\n\r\n\r\n\r\nTest   spacing."
    normalized = TextNormalizer.normalize(raw)
    assert "\r" not in normalized
    assert "Hello world!" in normalized
    assert "\n\n\n" not in normalized
