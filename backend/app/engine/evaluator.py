from typing import Any, Dict

from ..models.responses import EvaluationResponse
from ..providers.router import ProviderRouter
from ..utils.json import parse_llm_json


class Evaluator:

    def __init__(self):
        self.llm = ProviderRouter()

    async def evaluate(
        self,
        topic: str,
        answer: str,
        level: str = "beginner",
        difficulty: int = 1,
        question: str = "",
    ) -> EvaluationResponse:

        prompt = f"""
You are evaluating a student's understanding.

Topic:
{topic}

Student level:
{level}

Difficulty:
{difficulty}/5

Question asked to the student:
{question}

Student answer:
{answer}

Evaluate the student's conceptual understanding.

Do not judge grammar or writing style unless it changes the meaning.

Return ONLY valid JSON:

{{
  "correct": true,
  "score": 0.0,
  "feedback": "short useful feedback",
  "misconception": null,
  "confidence": 0.0
}}

Rules:

- score must be between 0 and 1.
- 1.0 = completely correct.
- 0.7-0.9 = mostly correct with minor gaps.
- 0.4-0.69 = partially correct.
- below 0.4 = weak or incorrect understanding.
- correct should normally be true only when sufficient understanding is demonstrated.
- Identify the actual conceptual misconception when one exists.
- Do not invent a misconception merely because the answer is incomplete.
- For a partially correct answer, explain what is correct and what is missing.
- Feedback should help the student improve.
- confidence must be between 0 and 1.
"""

        raw = await self.llm.generate(
            prompt,
            json_mode=True,
            temperature=0.1,
            max_tokens=700,
        )

        data: Dict[str, Any] = parse_llm_json(raw)

        score = float(
            data.get(
                "score",
                0.0,
            )
        )

        score = max(
            0.0,
            min(1.0, score),
        )

        confidence = float(
            data.get(
                "confidence",
                0.5,
            )
        )

        confidence = max(
            0.0,
            min(1.0, confidence),
        )

        misconception = data.get(
            "misconception"
        )

        if misconception is not None:
            misconception = str(
                misconception
            ).strip()

            if not misconception:
                misconception = None

        correct_value = data.get(
            "correct"
        )

        if correct_value is None:
            correct_value = score >= 0.85

        return EvaluationResponse(
            correct=bool(correct_value),
            score=score,
            feedback=str(
                data.get(
                    "feedback",
                    "",
                )
            ),
            misconception=misconception,
            confidence=confidence,
        )


evaluator = Evaluator()