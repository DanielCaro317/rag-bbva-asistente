from collections import Counter

from src.repositories.conversation_repository import ConversationRepository

# heurística: respuestas donde el asistente admite no tener la información (grounding)
NO_ANSWER_HINTS = (
    "no está en el contexto",
    "no se encuentra en el contexto",
    "no tengo esa información",
    "no dispongo de",
    "no hay información",
    "no puedo responder",
)


def _avg(values):
    return round(sum(values) / len(values), 1) if values else 0.0


def compute_metrics(repo=None):
    repo = repo or ConversationRepository()
    messages = repo.all_messages()

    sessions = {m["session_id"] for m in messages}
    questions = [m for m in messages if m["role"] == "user"]
    answers = [m for m in messages if m["role"] == "assistant"]

    by_day = Counter(m["created_at"][:10] for m in messages if m["created_at"])
    no_answer = sum(
        1 for m in answers if any(h in m["content"].lower() for h in NO_ANSWER_HINTS)
    )

    return {
        "total_sessions": len(sessions),
        "total_messages": len(messages),
        "total_questions": len(questions),
        "total_answers": len(answers),
        "avg_messages_per_session": round(len(messages) / len(sessions), 2) if sessions else 0.0,
        "avg_question_length": _avg([len(m["content"]) for m in questions]),
        "avg_answer_length": _avg([len(m["content"]) for m in answers]),
        "grounding_no_answer_rate": round(no_answer / len(answers), 3) if answers else 0.0,
        "messages_by_day": dict(sorted(by_day.items())),
    }
