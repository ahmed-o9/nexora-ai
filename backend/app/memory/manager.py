import json
from typing import Any, Dict

from .database import database


class ProfileStore:
    def get(self, student_id: str) -> Dict[str, Any]:
        row = database.fetchone(
            """
            SELECT student_id, turn_count,
                   created_at, updated_at
            FROM profiles
            WHERE student_id = ?
            """,
            (student_id,),
        )

        if row:
            return row

        database.execute(
            """
            INSERT INTO profiles (student_id)
            VALUES (?)
            """,
            (student_id,),
        )

        return self.get(student_id)

    def increment_turn(self, student_id: str):
        self.get(student_id)

        database.execute(
            """
            UPDATE profiles
            SET turn_count = turn_count + 1,
                updated_at = CURRENT_TIMESTAMP
            WHERE student_id = ?
            """,
            (student_id,),
        )


class LongTermMemory:
    def get_mastery(
        self,
        student_id: str,
        topic: str,
    ) -> float:
        row = database.fetchone(
            """
            SELECT mastery
            FROM mastery
            WHERE student_id = ?
              AND topic = ?
            """,
            (
                student_id,
                topic,
            ),
        )

        if not row:
            return 0.0

        return float(row["mastery"])

    def update_mastery(
        self,
        student_id: str,
        topic: str,
        mastery_value: float,
    ):
        mastery_value = max(
            0.0,
            min(1.0, float(mastery_value)),
        )

        database.execute(
            """
            INSERT INTO mastery
                (student_id, topic, mastery)
            VALUES (?, ?, ?)
            ON CONFLICT(student_id, topic)
            DO UPDATE SET
                mastery = excluded.mastery,
                updated_at = CURRENT_TIMESTAMP
            """,
            (
                student_id,
                topic,
                mastery_value,
            ),
        )

    def all_mastery(
        self,
        student_id: str = None,
    ):
        if student_id:
            rows = database.fetchall(
                """
                SELECT topic, mastery, updated_at
                FROM mastery
                WHERE student_id = ?
                ORDER BY updated_at DESC
                """,
                (student_id,),
            )

            return {
                row["topic"]: row["mastery"]
                for row in rows
            }

        rows = database.fetchall(
            """
            SELECT student_id, topic, mastery
            FROM mastery
            ORDER BY updated_at DESC
            """
        )

        result = {}

        for row in rows:
            result.setdefault(
                row["student_id"],
                {},
            )[row["topic"]] = row["mastery"]

        return result


class SessionMemory:
    def save(self, session: Dict[str, Any]):
        database.execute(
            """
            INSERT INTO sessions (
                session_id,
                student_id,
                topic,
                mode,
                current_level,
                difficulty,
                mastery,
                turn,
                strategy,
                misconceptions,
                last_question
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(session_id)
            DO UPDATE SET
                student_id = excluded.student_id,
                topic = excluded.topic,
                mode = excluded.mode,
                current_level = excluded.current_level,
                difficulty = excluded.difficulty,
                mastery = excluded.mastery,
                turn = excluded.turn,
                strategy = excluded.strategy,
                misconceptions = excluded.misconceptions,
                last_question = excluded.last_question,
                updated_at = CURRENT_TIMESTAMP
            """,
            (
                session["session_id"],
                session["student_id"],
                session["topic"],
                session["mode"],
                session["current_level"],
                session["difficulty"],
                session["mastery"],
                session["turn"],
                session["strategy"],
                json.dumps(
                    session.get(
                        "misconceptions",
                        [],
                    )
                ),
                session.get("last_question"),
            ),
        )

    def get(self, session_id: str):
        row = database.fetchone(
            """
            SELECT *
            FROM sessions
            WHERE session_id = ?
            """,
            (session_id,),
        )

        if not row:
            return None

        row["misconceptions"] = json.loads(
            row["misconceptions"] or "[]"
        )

        return row

    def all_for_student(self, student_id: str):
        rows = database.fetchall(
            """
            SELECT *
            FROM sessions
            WHERE student_id = ?
            ORDER BY updated_at DESC
            """,
            (student_id,),
        )

        for row in rows:
            row["misconceptions"] = json.loads(
                row["misconceptions"] or "[]"
            )

        return rows


class MemoryManager:
    def __init__(self):
        self.profiles = ProfileStore()
        self.long_term = LongTermMemory()
        self.sessions = SessionMemory()

    def record_turn(
        self,
        student_id: str,
        topic: str,
    ):
        self.profiles.increment_turn(student_id)

    def get_context(
        self,
        student_id: str,
        topic: str,
    ):
        return {
            "profile": self.profiles.get(
                student_id
            ),
            "mastery": self.long_term.get_mastery(
                student_id,
                topic,
            ),
            "all_mastery": self.long_term.all_mastery(
                student_id
            ),
        }


memory = MemoryManager()