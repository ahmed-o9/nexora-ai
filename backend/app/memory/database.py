import sqlite3
from pathlib import Path
from typing import Any, Dict, List, Optional

from ..core.config import get_settings


class Database:
    def __init__(self):
        settings = get_settings()

        db_url = settings.DATABASE_URL

        if db_url.startswith("sqlite:///"):
            db_path = db_url.replace("sqlite:///", "", 1)
        else:
            db_path = "./nexora.db"

        self.db_path = Path(db_path)

        if not self.db_path.is_absolute():
            self.db_path = Path.cwd() / self.db_path

        self.db_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.init_db()

    def connect(self):
        connection = sqlite3.connect(
            str(self.db_path),
            check_same_thread=False,
        )
        connection.row_factory = sqlite3.Row
        return connection

    def init_db(self):
        with self.connect() as conn:
            conn.executescript(
                """
                CREATE TABLE IF NOT EXISTS profiles (
                    student_id TEXT PRIMARY KEY,
                    turn_count INTEGER NOT NULL DEFAULT 0,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                );

                CREATE TABLE IF NOT EXISTS mastery (
                    student_id TEXT NOT NULL,
                    topic TEXT NOT NULL,
                    mastery REAL NOT NULL DEFAULT 0.0,
                    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    PRIMARY KEY (student_id, topic)
                );

                CREATE TABLE IF NOT EXISTS sessions (
                    session_id TEXT PRIMARY KEY,
                    student_id TEXT NOT NULL,
                    topic TEXT NOT NULL,
                    mode TEXT NOT NULL DEFAULT 'learn',
                    current_level TEXT NOT NULL DEFAULT 'beginner',
                    difficulty INTEGER NOT NULL DEFAULT 1,
                    mastery REAL NOT NULL DEFAULT 0.0,
                    turn INTEGER NOT NULL DEFAULT 0,
                    strategy TEXT NOT NULL DEFAULT 'direct_explanation',
                    misconceptions TEXT NOT NULL DEFAULT '[]',
                    last_question TEXT,
                    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                );
                """
            )

    def execute(
        self,
        query: str,
        params: tuple = (),
    ):
        with self.connect() as conn:
            cursor = conn.execute(
                query,
                params,
            )
            conn.commit()
            return cursor

    def fetchone(
        self,
        query: str,
        params: tuple = (),
    ) -> Optional[Dict[str, Any]]:
        with self.connect() as conn:
            row = conn.execute(
                query,
                params,
            ).fetchone()

            return dict(row) if row else None

    def fetchall(
        self,
        query: str,
        params: tuple = (),
    ) -> List[Dict[str, Any]]:
        with self.connect() as conn:
            rows = conn.execute(
                query,
                params,
            ).fetchall()

            return [dict(row) for row in rows]


database = Database()