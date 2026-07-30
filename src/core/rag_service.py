import sys

from src.config import settings
from src.providers.factory import get_embeddings, get_llm, get_vector_store

PROMPT_TEMPLATE = """Eres un asistente que responde preguntas sobre el sitio web de un banco.
Usa únicamente el CONTEXTO. Si la respuesta no está en el contexto, dilo con claridad.
Responde en español y menciona las fuentes usadas.

CONTEXTO:
{context}

PREGUNTA: {question}

RESPUESTA:"""


class RAGService:
    def __init__(self):
        self.embeddings = get_embeddings()
        self.vector_store = get_vector_store(dim=self.embeddings.dim)
        self.llm = get_llm()

    def retrieve(self, question):
        vector = self.embeddings.embed_query(question)
        return self.vector_store.search(vector, settings.top_k)

    def answer(self, question):
        hits = self.retrieve(question)
        context = "\n\n".join(f"[{h['source']}] {h['text']}" for h in hits)
        prompt = PROMPT_TEMPLATE.format(context=context, question=question)
        answer = self.llm.generate(prompt)
        return {
            "answer": answer,
            "sources": sorted({h["source"] for h in hits}),
            "hits": hits,
        }


def main():
    question = " ".join(sys.argv[1:]) or "¿Qué productos ofrece el banco?"
    result = RAGService().answer(question)
    print(result["answer"])
    print("\nFuentes:", ", ".join(result["sources"]))


if __name__ == "__main__":
    main()
