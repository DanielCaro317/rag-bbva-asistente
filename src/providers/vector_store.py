import uuid

from qdrant_client import QdrantClient, models

from src.config import settings


class QdrantVectorStore:
    def __init__(self, dim, url=None, collection=None):
        self.client = QdrantClient(url=url or settings.qdrant_url)
        self.collection = collection or settings.collection_name
        self.dim = dim

    def reset(self):
        if self.client.collection_exists(self.collection):
            self.client.delete_collection(self.collection)
        self.client.create_collection(
            collection_name=self.collection,
            vectors_config=models.VectorParams(size=self.dim, distance=models.Distance.COSINE),
        )

    def upsert(self, records, vectors):
        points = [
            models.PointStruct(id=str(uuid.uuid4()), vector=vec, payload=rec)
            for rec, vec in zip(records, vectors)
        ]
        self.client.upsert(collection_name=self.collection, points=points)

    def search(self, vector, top_k):
        res = self.client.query_points(
            collection_name=self.collection,
            query=vector,
            limit=top_k,
            with_payload=True,
        )
        return [{"score": p.score, **p.payload} for p in res.points]
