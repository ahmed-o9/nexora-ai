from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any, Dict, List, Optional


class DocumentStore:
    """
    Persistent local document/chunk storage for Nexora.

    Uses SQLite so the initial RAG system requires:
    - no external database
    - no API
    - no vector database
    """

    def __init__(self, database_path: str = "nexora.db") -> None:
        self.database_path = self._resolve_path(database_path)
        self._initialize()

    def _resolve_path(self, database_path: str) -> str:
        if database_path.startswith("sqlite:///"):
            database_path = database_path[len("sqlite:///") :]

        path = Path(database_path)

        if not path.is_absolute():
            path = Path.cwd() / path

        return str(path)

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        return connection

    def _initialize(self) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS documents (
                    document_id TEXT PRIMARY KEY,
                    student_id TEXT NOT NULL,
                    filename TEXT NOT NULL,
                    content_type TEXT DEFAULT '',
                    source TEXT DEFAULT '',
                    metadata TEXT DEFAULT '{}',
                    created_at TEXT NOT NULL
                )
                """
            )

            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS document_chunks (
                    chunk_id TEXT PRIMARY KEY,
                    document_id TEXT NOT NULL,
                    student_id TEXT NOT NULL,
                    chunk_index INTEGER NOT NULL,
                    text TEXT NOT NULL,
                    metadata TEXT DEFAULT '{}',
                    created_at TEXT NOT NULL,
                    FOREIGN KEY(document_id)
                        REFERENCES documents(document_id)
                        ON DELETE CASCADE
                )
                """
            )

            connection.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_document_chunks_student
                ON document_chunks(student_id)
                """
            )

            connection.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_document_chunks_document
                ON document_chunks(document_id)
                """
            )

            connection.commit()

    def add_document(
        self,
        document_id: str,
        student_id: str,
        filename: str,
        content_type: str = "",
        source: str = "",
        metadata: Optional[Dict[str, Any]] = None,
        created_at: str = "",
    ) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                INSERT OR REPLACE INTO documents (
                    document_id,
                    student_id,
                    filename,
                    content_type,
                    source,
                    metadata,
                    created_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    document_id,
                    student_id,
                    filename,
                    content_type,
                    source,
                    json.dumps(metadata or {}),
                    created_at,
                ),
            )

            connection.commit()

    def add_chunks(
        self,
        document_id: str,
        student_id: str,
        chunks: List[Dict[str, Any]],
    ) -> None:
        with self._connect() as connection:
            for chunk in chunks:
                connection.execute(
                    """
                    INSERT OR REPLACE INTO document_chunks (
                        chunk_id,
                        document_id,
                        student_id,
                        chunk_index,
                        text,
                        metadata,
                        created_at
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        chunk["chunk_id"],
                        document_id,
                        student_id,
                        int(chunk.get("chunk_index", 0)),
                        chunk["text"],
                        json.dumps(chunk.get("metadata", {})),
                        chunk.get("created_at", ""),
                    ),
                )

            connection.commit()

    def get_document(
        self,
        document_id: str,
    ) -> Optional[Dict[str, Any]]:
        with self._connect() as connection:
            row = connection.execute(
                """
                SELECT *
                FROM documents
                WHERE document_id = ?
                """,
                (document_id,),
            ).fetchone()

        if row is None:
            return None

        return self._document_row(row)

    def list_documents(
        self,
        student_id: str = "default",
    ) -> List[Dict[str, Any]]:
        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT *
                FROM documents
                WHERE student_id = ?
                ORDER BY created_at DESC
                """,
                (student_id,),
            ).fetchall()

        return [self._document_row(row) for row in rows]

    def get_chunks(
        self,
        document_id: str,
    ) -> List[Dict[str, Any]]:
        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT *
                FROM document_chunks
                WHERE document_id = ?
                ORDER BY chunk_index ASC
                """,
                (document_id,),
            ).fetchall()

        return [self._chunk_row(row) for row in rows]

    def search(
        self,
        student_id: str,
        query: str,
        limit: int = 5,
    ) -> List[Dict[str, Any]]:
        """
        Simple lexical retrieval.

        RAG starts with deterministic local retrieval.
        Semantic/vector retrieval can be added later without
        changing the teacher architecture.
        """

        query_terms = self._tokenize(query)

        if not query_terms:
            return []

        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT
                    c.*,
                    d.filename,
                    d.source
                FROM document_chunks c
                JOIN documents d
                    ON c.document_id = d.document_id
                WHERE c.student_id = ?
                """,
                (student_id,),
            ).fetchall()

        scored = []

        for row in rows:
            text = row["text"]
            score = self._score(text, query_terms)

            if score <= 0:
                continue

            item = self._chunk_row(row)
            item["filename"] = row["filename"]
            item["source"] = row["source"]
            item["score"] = score

            scored.append(item)

        scored.sort(
            key=lambda item: item["score"],
            reverse=True,
        )

        return scored[: max(1, int(limit))]

    def delete_document(
        self,
        document_id: str,
    ) -> bool:
        with self._connect() as connection:
            connection.execute(
                """
                DELETE FROM document_chunks
                WHERE document_id = ?
                """,
                (document_id,),
            )

            cursor = connection.execute(
                """
                DELETE FROM documents
                WHERE document_id = ?
                """,
                (document_id,),
            )

            connection.commit()

        return cursor.rowcount > 0

    @staticmethod
    def _tokenize(text: str) -> List[str]:
        import re

        return [
            token
            for token in re.findall(
                r"[a-zA-Z0-9_]+",
                text.lower(),
            )
            if len(token) > 1
        ]

    @classmethod
    def _score(
        cls,
        text: str,
        query_terms: List[str],
    ) -> float:
        tokens = cls._tokenize(text)

        if not tokens:
            return 0.0

        frequencies: Dict[str, int] = {}

        for token in tokens:
            frequencies[token] = frequencies.get(token, 0) + 1

        score = 0.0

        for term in query_terms:
            frequency = frequencies.get(term, 0)

            if frequency:
                score += 1.0 + min(
                    frequency - 1,
                    3,
                ) * 0.25

        return score / max(len(query_terms), 1)

    @staticmethod
    def _document_row(row: sqlite3.Row) -> Dict[str, Any]:
        try:
            metadata = json.loads(row["metadata"] or "{}")
        except json.JSONDecodeError:
            metadata = {}

        return {
            "document_id": row["document_id"],
            "student_id": row["student_id"],
            "filename": row["filename"],
            "content_type": row["content_type"],
            "source": row["source"],
            "metadata": metadata,
            "created_at": row["created_at"],
        }

    @staticmethod
    def _chunk_row(row: sqlite3.Row) -> Dict[str, Any]:
        try:
            metadata = json.loads(row["metadata"] or "{}")
        except json.JSONDecodeError:
            metadata = {}

        return {
            "chunk_id": row["chunk_id"],
            "document_id": row["document_id"],
            "student_id": row["student_id"],
            "chunk_index": int(row["chunk_index"]),
            "text": row["text"],
            "metadata": metadata,
            "created_at": row["created_at"],
        }


document_store = DocumentStore()