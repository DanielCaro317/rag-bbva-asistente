from src.ingestion.chunker import chunk_text


def test_empty_text_returns_no_chunks():
    assert chunk_text("", 100, 20) == []


def test_short_text_single_chunk():
    text = "hola mundo banco"
    assert chunk_text(text, 100, 20) == [text]


def test_long_text_splits_and_covers_all_words():
    words = [f"w{i}" for i in range(300)]
    chunks = chunk_text(" ".join(words), 100, 20)
    assert len(chunks) > 1
    seen = " ".join(chunks).split()
    for w in words:
        assert w in seen


def test_overlap_carries_context():
    words = [f"w{i}" for i in range(300)]
    chunks = chunk_text(" ".join(words), 100, 20)
    # el inicio del 2º chunk viene del final del 1º (solape)
    assert chunks[1].split()[0] in chunks[0].split()
