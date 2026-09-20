from fastapi import APIRouter

from ..models.requests import QuizAnswerRequest, QuizRequest
from ..models.quiz import QuizQuestion
from ..providers.router import ProviderRouter
from ..prompts.quiz import quiz_prompt
from ..utils.json import parse_llm_json
from ..utils.validation import validate


router = APIRouter()
router_llm = ProviderRouter()


@router.post("/api/sessions/{sid}/quiz")
async def quiz(
    sid: str,
    req: QuizRequest,
):
    from ..engine.orchestrator import orchestrator

    session = orchestrator.get_session(sid)

    topic = req.topic or session["topic"]

    raw = await router_llm.generate(
        quiz_prompt(
            topic,
            req.difficulty,
            req.qtype,
        ),
        json_mode=True,
    )

    question = validate(
        parse_llm_json(raw),
        QuizQuestion,
    )

    session["active_quiz"] = {
        "question": question.question,
        "qtype": question.qtype,
        "options": question.options,
        "correct_answer": question.correct_answer,
        "explanation": question.explanation,
        "difficulty": question.difficulty,
    }

    return {
        "question": question.question,
        "qtype": question.qtype,
        "options": question.options,
        "difficulty": question.difficulty,
    }


@router.post("/api/sessions/{sid}/quiz/answer")
async def quiz_answer(
    sid: str,
    req: QuizAnswerRequest,
):
    from ..engine.orchestrator import orchestrator

    return await orchestrator.handle_quiz_answer(
        sid,
        req.answer,
    )