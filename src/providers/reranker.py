from sentence_transformers import CrossEncoder

from src.config import settings


class Reranker:
    def __init__(self, model_name=None):
        self.model = CrossEncoder(model_name or settings.reranker_model)

    # reordena los candidatos por relevancia real query-chunk
    def rerank(self, query, hits, top_k):
        pairs = [(query, h["text"]) for h in hits]
        scores = self.model.predict(pairs)
        ranked = sorted(zip(hits, scores), key=lambda pair: pair[1], reverse=True)
        return [dict(h, rerank_score=float(s)) for h, s in ranked[:top_k]]
