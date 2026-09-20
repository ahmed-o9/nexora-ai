from fastapi import APIRouter

from ..memory.manager import memory


router = APIRouter()


@router.get("/api/student/profile")
async def profile(
    student_id: str = "default",
):
    return memory.profiles.get(
        student_id
    )


@router.get("/api/student/mastery")
async def mastery(
    student_id: str = "default",
):
    profile = memory.profiles.get(
        student_id
    )

    return {
        "student_id": student_id,
        "mastery": memory.long_term.all_mastery(
            student_id
        ),
        "profile": profile,
    }


@router.get("/api/student/sessions")
async def sessions(
    student_id: str = "default",
):
    return {
        "student_id": student_id,
        "sessions": memory.sessions.all_for_student(
            student_id
        ),
    }