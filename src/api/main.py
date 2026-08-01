from contextlib import asynccontextmanager
from functools import lru_cache

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from src.api.schemas import ChatRequest, ChatResponse
from src.config import settings
from src.core.rag_service import RAGService


@lru_cache(maxsize=1)
def get_service() -> RAGService:
    return RAGService()


@asynccontextmanager
async def lifespan(app: FastAPI):
    get_service()  # cargamos modelos una vez al arrancar, no en la primera petición
    yield


app = FastAPI(title="RAG BBVA Asistente", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok", "env": settings.app_env}


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest, service: RAGService = Depends(get_service)):
    try:
        result = service.answer(req.question, req.session_id)
    except Exception:
        raise HTTPException(
            status_code=502,
            detail="No se pudo generar la respuesta. Verifica que Ollama y Qdrant estén disponibles.",
        )
    return ChatResponse(answer=result["answer"], sources=result["sources"], session_id=req.session_id)
