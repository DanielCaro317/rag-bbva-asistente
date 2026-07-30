from abc import ABC, abstractmethod


class EmbeddingsProvider(ABC):
    @abstractmethod
    def embed_documents(self, texts):
        ...

    @abstractmethod
    def embed_query(self, text):
        ...

    @property
    @abstractmethod
    def dim(self):
        ...


class VectorStore(ABC):
    @abstractmethod
    def reset(self):
        ...

    @abstractmethod
    def upsert(self, records, vectors):
        ...

    @abstractmethod
    def search(self, vector, top_k):
        ...


class LLMProvider(ABC):
    @abstractmethod
    def generate(self, prompt):
        ...
