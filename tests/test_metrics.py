from src.analytics.metrics import compute_metrics
from src.repositories.conversation_repository import ConversationRepository


def test_metrics_counts(tmp_path):
    repo = ConversationRepository(db_path=str(tmp_path / "c.sqlite3"))
    repo.add_message("s1", "user", "hola")
    repo.add_message("s1", "assistant", "una respuesta")
    repo.add_message("s2", "user", "otra")
    repo.add_message("s2", "assistant", "no está en el contexto")
    m = compute_metrics(repo)
    assert m["total_sessions"] == 2
    assert m["total_messages"] == 4
    assert m["total_questions"] == 2
    assert m["total_answers"] == 2
    # 1 de 2 respuestas admite no saber -> 0.5
    assert m["grounding_no_answer_rate"] == 0.5


def test_metrics_empty(tmp_path):
    repo = ConversationRepository(db_path=str(tmp_path / "c.sqlite3"))
    m = compute_metrics(repo)
    assert m["total_messages"] == 0
    assert m["grounding_no_answer_rate"] == 0.0
