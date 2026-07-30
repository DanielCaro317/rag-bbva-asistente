from fastapi import FastAPI

from src.config import settings

app = FastAPI(title="RAG BBVA Asistente")


@app.get("/health")
def health():
    return {"status": "ok", "env": settings.app_env}
