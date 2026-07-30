import sys
import uuid

from src.config import settings
from src.providers.factory import get_embeddings, get_llm, get_reranker, get_vector_store
from src.repositories.conversation_repository import ConversationRepository

PROMPT_TEMPLATE = """Eres un asistente que responde preguntas sobre el sitio web de un banco.
Usa únicamente el CONTEXTO. Si la respuesta no está en el contexto, dilo con claridad.
Ten en cuenta el HISTORIAL para entender referencias a mensajes anteriores.
Responde en español y menciona las fuentes usadas.

HISTORIAL:
{history}

CONTEXTO:
{context}

PREGUNTA: {question}

RESPUESTA:"""


class RAGService:
    def __init__(self):
        self.embeddings = get_embeddings()
        self.vector_store = get_vector_store(dim=self.embeddings.dim)
        self.llm = get_llm()
        self.reranker = get_reranker()
        self.history = ConversationRepository()

    def retrieve(self, question):
        vector = self.embeddings.embed_query(question)
        if self.reranker:
            candidates = self.vector_store.search(vector, settings.top_k * 4)
            return self.reranker.rerank(question, candidates, settings.top_k)
        return self.vector_store.search(vector, settings.top_k)

    def answer(self, question, session_id="default"):
        hits = self.retrieve(question)
        context = "\n\n".join(f"[{h['source']}] {h['text']}" for h in hits)
        recent = self.history.get_recent(session_id, settings.history_n)
        history = "\n".join(f"{m['role']}: {m['content']}" for m in recent) or "(sin mensajes previos)"

        prompt = PROMPT_TEMPLATE.format(history=history, context=context, question=question)
        answer = self.llm.generate(prompt)

        self.history.add_message(session_id, "user", question)
        self.history.add_message(session_id, "assistant", answer)
        return {
            "answer": answer,
            "sources": sorted({h["source"] for h in hits}),
            "hits": hits,
        }


def main():
    session_id = f"cli-{uuid.uuid4().hex[:8]}"
    question = " ".join(sys.argv[1:]) or "¿Qué productos ofrece el banco?"
    result = RAGService().answer(question, session_id)
    print(result["answer"])
    print("\nFuentes:", ", ".join(result["sources"]))


if __name__ == "__main__":
    main()
