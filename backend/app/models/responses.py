from typing import List, Optional

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str
    provider: str


class VisualResult(BaseModel):
    title: str = ""
    image_url: str
    thumbnail_url: str = ""
    source_url: str = ""
    source_name: str = ""
    query: str = ""
    width: Optional[int] = None
    height: Optional[int] = None


class Explanation(BaseModel):
    explanation: str
    example: str = ""
    analogy: str = ""
    key_points: List[str] = Field(default_factory=list)
    understanding_check: Optional[str] = None

    # Educational visuals retrieved by Nexora.
    visuals: List[VisualResult] = Field(default_factory=list)


class TeachResponse(BaseModel):
    session_id: str
    topic: str
    level: str
    mode: str
    content: Explanation
    strategy: str
    difficulty: int = Field(ge=1, le=5)

    # Structured deterministic tool result used during
    # this teaching turn.
    #
    # Examples:
    # {
    #     "result": 23
    # }
    #
    # or other structured results produced by SymPy/tools.
    tool_result: Optional[object] = None

    @property
    def understanding_check(self) -> Optional[str]:
        return self.content.understanding_check


class EvaluationResponse(BaseModel):
    correct: bool
    score: float = Field(ge=0.0, le=1.0)
    feedback: str
    misconception: Optional[str] = None
    confidence: float = Field(default=0.5, ge=0.0, le=1.0)


class SessionState(BaseModel):
    session_id: str
    topic: str
    student_id: str = "default"
    mode: str = "learn"
    current_level: str = "beginner"
    difficulty: int = Field(default=1, ge=1, le=5)
    mastery: float = Field(default=0.0, ge=0.0, le=1.0)
    turn: int = 0
    strategy: str = "direct_explanation"
    misconceptions: List[str] = Field(default_factory=list)
    last_question: str = ""


class AnswerResponse(BaseModel):
    session_id: str
    evaluation: EvaluationResponse
    state: SessionState
    next_action: str
    content: Optional[Explanation] = None


class QuizAnswerResponse(BaseModel):
    session_id: str
    correct: bool
    score: float
    feedback: str
    correct_answer: str
    explanation: str
    mastery: float
    difficulty: int
    current_level: str
    next_action: str
    misconception: Optional[str] = None