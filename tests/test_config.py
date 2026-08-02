from src.config import Settings


def test_cors_origins_list_parsing():
    s = Settings(cors_origins="http://a, http://b ,http://c")
    assert s.cors_origins_list == ["http://a", "http://b", "http://c"]


def test_cors_origins_list_empty():
    s = Settings(cors_origins="")
    assert s.cors_origins_list == []
