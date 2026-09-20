from typing import List

from pydantic import BaseModel, Field


class QuizQuestion(BaseModel):
    question: str = Field(..., min_length=1)
    qtype: str = "multiple_choice"
    options: List[str] = Field(default_factory=list)
    correct_answer: str = ""
    explanation: str = ""
    difficulty: int = Field(default=1, ge=1, le=5)