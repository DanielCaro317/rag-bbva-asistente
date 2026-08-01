from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    question: str = Field(min_length=1, description="Pregunta del usuario")
    session_id: str = Field(default="default", description="Identificador de la conversación")


class ChatResponse(BaseModel):
    answer: str
    sources: list[str]
    session_id: str
