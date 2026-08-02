from src.config import settings
from src.providers.embeddings import EmbeddingsModel
from src.providers.llm import OllamaLLM, OpenAICompatLLM
from src.providers.reranker import Reranker
from src.providers.vector_store import QdrantVectorStore


def get_embeddings():
    return EmbeddingsModel()


def get_vector_store(dim):
    if settings.vector_store == "qdrant":
        return QdrantVectorStore(dim=dim)
    raise ValueError(f"vector store no soportado: {settings.vector_store}")


def get_llm():
    if settings.llm_provider == "ollama":
        return OllamaLLM()
    if settings.llm_provider == "openai":
        return OpenAICompatLLM()
    raise ValueError(f"proveedor LLM no soportado: {settings.llm_provider}")


def get_reranker():
    if settings.reranker_enabled:
        return Reranker()
    return None
