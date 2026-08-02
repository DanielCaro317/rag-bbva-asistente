from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    question: str = Field(min_length=1, description="Pregunta del usuario")
    session_id: str = Field(default="default", description="Identificador de la conversación")


class ChatResponse(BaseModel):
    answer: str
    sources: list[str]
    session_id: str


class MetricsResponse(BaseModel):
    total_sessions: int
    total_messages: int
    total_questions: int
    total_answers: int
    avg_messages_per_session: float
    avg_question_length: float
    avg_answer_length: float
    grounding_no_answer_rate: float
    messages_by_day: dict[str, int]
