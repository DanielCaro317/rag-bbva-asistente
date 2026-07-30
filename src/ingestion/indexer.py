from pathlib import Path

from src.config import settings
from src.ingestion.chunker import chunk_text
from src.providers.embeddings import EmbeddingsModel
from src.providers.vector_store import QdrantVectorStore

CLEAN_DIR = Path("data/clean")


def _load_chunks():
    records = []
    for path in sorted(CLEAN_DIR.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        for i, chunk in enumerate(chunk_text(text, settings.chunk_size, settings.chunk_overlap)):
            records.append({"text": chunk, "source": path.stem, "chunk": i})
    return records


def build_index():
    records = _load_chunks()
    if not records:
        print("No hay documentos en data/clean. Corre primero el scraper.")
        return 0
    embedder = EmbeddingsModel()
    store = QdrantVectorStore(dim=embedder.dim)
    store.reset()
    vectors = embedder.embed_documents([r["text"] for r in records])
    store.upsert(records, vectors)
    return len(records)


def main():
    n = build_index()
    print(f"Indexados {n} chunks en Qdrant")


if __name__ == "__main__":
    main()
