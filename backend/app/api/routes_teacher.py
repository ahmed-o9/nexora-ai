from fastapi import APIRouter
from ..models.requests import TeachRequest
from ..engine.orchestrator import orchestrator

router = APIRouter()

@router.post("/api/teach")
async def teach(req: TeachRequest):
    """MVP-compatible one-shot teach endpoint."""
    return await orchestrator.handle_teach(
        question=req.question, student_id=req.student_id,
        mode=req.mode, level=req.level or "beginner")