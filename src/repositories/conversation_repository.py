import sqlite3
from datetime import datetime, timezone
from pathlib import Path

from src.config import settings


class ConversationRepository:
    def __init__(self, db_path=None):
        self.db_path = db_path or settings.db_path
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def _init_db(self):
        with self._connect() as con:
            con.execute(
                """CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )"""
            )

    def add_message(self, session_id, role, content):
        with self._connect() as con:
            con.execute(
                "INSERT INTO messages (session_id, role, content, created_at) VALUES (?, ?, ?, ?)",
                (session_id, role, content, datetime.now(timezone.utc).isoformat()),
            )

    # últimos N en orden cronológico
    def get_recent(self, session_id, n):
        with self._connect() as con:
            rows = con.execute(
                "SELECT role, content FROM messages WHERE session_id = ? ORDER BY id DESC LIMIT ?",
                (session_id, n),
            ).fetchall()
        return [{"role": r, "content": c} for r, c in reversed(rows)]

    def all_messages(self):
        with self._connect() as con:
            rows = con.execute(
                "SELECT session_id, role, content, created_at FROM messages ORDER BY id"
            ).fetchall()
        return [
            {"session_id": s, "role": r, "content": c, "created_at": t}
            for s, r, c, t in rows
        ]
