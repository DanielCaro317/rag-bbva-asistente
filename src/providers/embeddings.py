from sentence_transformers import SentenceTransformer

from src.config import settings
from src.providers.base import EmbeddingsProvider


class EmbeddingsModel(EmbeddingsProvider):
    def __init__(self, model_name=None):
        self.model = SentenceTransformer(model_name or settings.embeddings_model)

    # e5 usa prefijos distintos para documentos y consultas
    def embed_documents(self, texts):
        payload = [f"passage: {t}" for t in texts]
        return self.model.encode(payload, normalize_embeddings=True).tolist()

    def embed_query(self, text):
        return self.model.encode(f"query: {text}", normalize_embeddings=True).tolist()

    @property
    def dim(self):
        return self.model.get_sentence_embedding_dimension()
