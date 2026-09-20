from fastapi import APIRouter
from ..models.requests import SessionCreate, AnswerRequest
from ..engine.orchestrator import orchestrator
from ..core.exceptions import SessionNotFound

router = APIRouter()

@router.post("/api/sessions")
async def create_session(req: SessionCreate):
    s = await orchestrator.create_session(
        topic=req.topic, student_id=req.student_id,
        mode=req.mode, level=req.level)
    return {"session_id": s["session_id"], "topic": s["topic"], "state": s}

@router.get("/api/sessions/{sid}")
async def get_session(sid: str):
    s = orchestrator.get_session(sid)
    return s

@router.post("/api/sessions/{sid}/answer")
async def answer(sid: str, req: AnswerRequest):
    return await orchestrator.handle_answer(sid, req.answer)

@router.post("/api/sessions/{sid}/simpler")
async def simpler(sid: str):
    s = orchestrator.get_session(sid)
    s["strategy"] = "simpler_explanation"
    return await orchestrator.teacher.teach(s)

@router.post("/api/sessions/{sid}/example")
async def example(sid: str):
    s = orchestrator.get_session(sid)
    s["strategy"] = "real_world_example"
    return await orchestrator.teacher.teach(s)