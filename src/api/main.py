from contextlib import asynccontextmanager
from functools import lru_cache

from fastapi import Depends, FastAPI

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


@app.get("/health")
def health():
    return {"status": "ok", "env": settings.app_env}


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest, service: RAGService = Depends(get_service)):
    result = service.answer(req.question, req.session_id)
    return ChatResponse(answer=result["answer"], sources=result["sources"], session_id=req.session_id)
