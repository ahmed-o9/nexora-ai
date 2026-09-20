from __future__ import annotations

import re
from typing import Any, Dict, List

from ..memory.document_store import document_store


class RAGEngine:
    """
    Retrieval-Augmented Generation support for Nexora.

    Current version:
        document -> chunks -> lexical retrieval -> context

    Later versions can replace the retrieval layer with embeddings
    without changing the orchestration contract.
    """

    def __init__(self, store=document_store) -> None:
        self.store = store

    def chunk_text(
        self,
        text: str,
        chunk_size: int = 900,
        overlap: int = 150,
    ) -> List[str]:
        text = self._clean_text(text)

        if not text:
            return []

        chunk_size = max(100, int(chunk_size))
        overlap = max(0, min(int(overlap), chunk_size - 1))

        chunks: List[str] = []

        start = 0
        text_length = len(text)

        while start < text_length:
            end = min(
                start + chunk_size,
                text_length,
            )

            chunk = text[start:end].strip()

            if chunk:
                chunks.append(chunk)

            if end >= text_length:
                break

            start = end - overlap

        return chunks

    def ingest(
        self,
        document_id: str,
        student_id: str,
        filename: str,
        text: str,
        content_type: str = "",
        source: str = "",
        metadata: Dict[str, Any] | None = None,
    ) -> Dict[str, Any]:

        from datetime import datetime, timezone
        from uuid import uuid4

        created_at = datetime.now(
            timezone.utc
        ).isoformat()

        chunks = self.chunk_text(text)

        self.store.add_document(
            document_id=document_id,
            student_id=student_id,
            filename=filename,
            content_type=content_type,
            source=source,
            metadata=metadata or {},
            created_at=created_at,
        )

        chunk_records = []

        for index, chunk in enumerate(chunks):
            chunk_records.append(
                {
                    "chunk_id": str(uuid4()),
                    "chunk_index": index,
                    "text": chunk,
                    "metadata": {
                        "filename": filename,
                        "chunk_index": index,
                    },
                    "created_at": created_at,
                }
            )

        self.store.add_chunks(
            document_id=document_id,
            student_id=student_id,
            chunks=chunk_records,
        )

        return {
            "document_id": document_id,
            "filename": filename,
            "chunks": len(chunk_records),
            "characters": len(text),
        }

    def retrieve(
        self,
        student_id: str,
        query: str,
        limit: int = 5,
    ) -> List[Dict[str, Any]]:
        return self.store.search(
            student_id=student_id,
            query=query,
            limit=limit,
        )

    def build_context(
        self,
        student_id: str,
        query: str,
        limit: int = 5,
    ) -> Dict[str, Any]:

        results = self.retrieve(
            student_id=student_id,
            query=query,
            limit=limit,
        )

        if not results:
            return {
                "query": query,
                "context": "",
                "sources": [],
                "found": False,
            }

        context_parts = []
        sources = []

        for index, item in enumerate(results, start=1):
            context_parts.append(
                f"[Source {index}: {item['filename']}]\n"
                f"{item['text']}"
            )

            sources.append(
                {
                    "filename": item["filename"],
                    "document_id": item["document_id"],
                    "chunk_id": item["chunk_id"],
                    "score": item["score"],
                }
            )

        return {
            "query": query,
            "context": "\n\n".join(context_parts),
            "sources": sources,
            "found": True,
        }

    @staticmethod
    def _clean_text(text: str) -> str:
        text = text.replace("\x00", " ")
        text = re.sub(
            r"[ \t]+",
            " ",
            text,
        )
        text = re.sub(
            r"\n{3,}",
            "\n\n",
            text,
        )

        return text.strip()


rag_engine = RAGEngine()