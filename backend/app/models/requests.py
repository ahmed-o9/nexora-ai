from typing import Optional
from pydantic import BaseModel, Field


class TeachRequest(BaseModel):
    question: str = Field(..., min_length=1)
    mode: str = "learn"
    student_id: str = "default"
    level: Optional[str] = None


class SessionCreate(BaseModel):
    topic: str = Field(..., min_length=1)
    student_id: str = "default"
    mode: str = "learn"
    level: str = "beginner"


class AnswerRequest(BaseModel):
    answer: str = Field(..., min_length=1)


class QuizRequest(BaseModel):
    topic: Optional[str] = None
    difficulty: int = Field(default=1, ge=1, le=5)
    qtype: str = "multiple_choice"


class QuizAnswerRequest(BaseModel):
    answer: str = Field(..., min_length=1)