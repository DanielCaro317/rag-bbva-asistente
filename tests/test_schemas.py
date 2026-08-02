import pytest
from pydantic import ValidationError

from src.api.schemas import ChatRequest


def test_chat_request_defaults():
    r = ChatRequest(question="hola")
    assert r.session_id == "default"


def test_chat_request_rejects_empty_question():
    with pytest.raises(ValidationError):
        ChatRequest(question="")
