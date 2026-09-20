from __future__ import annotations

import os
import tempfile
from uuid import uuid4

from fastapi import APIRouter, File, UploadFile

from ..engine.rag import rag_engine
from ..tools.document_parser import DocumentParserTool


router = APIRouter()


@router.post("/api/documents")
async def upload_doc(
    file: UploadFile = File(...),
    student_id: str = "default",
):
    """
    Upload a document, parse it, and ingest its text into
    Nexora's local RAG document store.
    """

    suffix = ""

    if file.filename and "." in file.filename:
        suffix = "." + file.filename.rsplit(
            ".",
            1,
        )[1]

    tmp_path = None

    try:
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=suffix,
        ) as tmp:

            tmp.write(
                await file.read()
            )

            tmp_path = tmp.name

        parsed = await DocumentParserTool().execute(
            path=tmp_path
        )

        # ---------------------------------------------------------
        # Extract parsed text
        # ---------------------------------------------------------

        if isinstance(parsed, dict):

            text = (
                parsed.get("text")
                or parsed.get("content")
                or parsed.get("data")
                or ""
            )

        else:

            text = str(parsed)

        if not isinstance(text, str):
            text = str(text)

        if not text.strip():

            return {
                "success": False,
                "error": (
                    "The document was parsed successfully "
                    "but no text could be extracted."
                ),
                "filename": file.filename,
            }

        # ---------------------------------------------------------
        # Ingest into RAG
        # ---------------------------------------------------------

        document_id = str(
            uuid4()
        )

        ingestion = rag_engine.ingest(
            document_id=document_id,
            student_id=student_id,
            filename=file.filename or "uploaded_document",
            text=text,
            content_type=file.content_type or "",
            source="upload",
        )

        return {
            "success": True,
            "document_id": document_id,
            "student_id": student_id,
            "filename": file.filename,
            "content_type": file.content_type or "",
            "characters": len(text),
            "chunks": ingestion["chunks"],
            "message": (
                "Document uploaded, parsed, and "
                "indexed for RAG."
            ),
        }

    finally:

        if (
            tmp_path
            and os.path.exists(tmp_path)
        ):
            os.unlink(tmp_path)