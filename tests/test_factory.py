import pytest

from src.config import settings
from src.providers import factory


def test_get_llm_rejects_unknown_provider(monkeypatch):
    monkeypatch.setattr(settings, "llm_provider", "desconocido")
    with pytest.raises(ValueError):
        factory.get_llm()


def test_get_vector_store_rejects_unknown_store(monkeypatch):
    monkeypatch.setattr(settings, "vector_store", "desconocido")
    with pytest.raises(ValueError):
        factory.get_vector_store(dim=768)
