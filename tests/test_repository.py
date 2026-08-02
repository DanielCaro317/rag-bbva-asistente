from src.repositories.conversation_repository import ConversationRepository


def test_get_recent_returns_last_n_in_order(tmp_path):
    repo = ConversationRepository(db_path=str(tmp_path / "c.sqlite3"))
    for i in range(5):
        repo.add_message("s1", "user", f"m{i}")
    recent = repo.get_recent("s1", 2)
    assert [m["content"] for m in recent] == ["m3", "m4"]


def test_persists_across_instances(tmp_path):
    db = str(tmp_path / "c.sqlite3")
    ConversationRepository(db_path=db).add_message("s1", "user", "hola")
    repo2 = ConversationRepository(db_path=db)
    assert repo2.get_recent("s1", 5)[0]["content"] == "hola"


def test_sessions_are_isolated(tmp_path):
    repo = ConversationRepository(db_path=str(tmp_path / "c.sqlite3"))
    repo.add_message("a", "user", "x")
    repo.add_message("b", "user", "y")
    assert len(repo.get_recent("a", 10)) == 1
