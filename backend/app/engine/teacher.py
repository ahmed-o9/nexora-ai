from typing import Any, Dict

from ..models.responses import Explanation, TeachResponse
from ..providers.router import ProviderRouter
from ..utils.json import parse_llm_json


class Teacher:

    def __init__(self):
        self.llm = ProviderRouter()

    async def teach(
        self,
        session: Dict[str, Any],
        question: str = "",
    ) -> TeachResponse:

        topic = session.get(
            "topic",
            "unknown topic",
        )

        level = session.get(
            "current_level",
            "beginner",
        )

        mode = session.get(
            "mode",
            "learn",
        )

        difficulty = int(
            session.get(
                "difficulty",
                1,
            )
        )

        mastery = float(
            session.get(
                "mastery",
                0.0,
            )
        )

        strategy = session.get(
            "strategy",
            "direct_explanation",
        )

        misconceptions = session.get(
            "misconceptions",
            [],
        )

        misconception_text = (
            "\n".join(
                f"- {item}"
                for item in misconceptions
            )
            if misconceptions
            else "None detected."
        )

        question_text = question or session.get(
            "last_question",
            "",
        )

        # ---------------------------------------------------------
        # DETERMINISTIC TOOL RESULT
        # ---------------------------------------------------------
        #
        # Tool results are authoritative outputs from deterministic
        # tools such as the calculator and SymPy.
        #
        # The teacher must use these results rather than inventing
        # or recomputing them.
        # ---------------------------------------------------------

        tool_result = session.get(
            "tool_result"
        )

        if tool_result is not None:

            tool_result_text = str(
                tool_result
            )

            tool_instruction = f"""
A deterministic tool was executed for this question.

AUTHORITATIVE TOOL RESULT:
{tool_result_text}

IMPORTANT:
- Treat the deterministic tool result as authoritative.
- Use the result directly in your explanation.
- If the question asks for a calculation, explicitly state the result.
- Do not replace, ignore, or contradict the deterministic result.
- Explain the result at the student's level.
"""

        else:

            tool_instruction = """
No deterministic tool result is available.

Do not invent a tool result.
"""

        prompt = f"""
You are Nexora, an adaptive AI teacher.

Your goal is to make the student understand the topic.

Topic:
{topic}

Student level:
{level}

Mode:
{mode}

Difficulty:
{difficulty}/5

Estimated mastery:
{mastery:.2f}

Current teaching strategy:
{strategy}

Known misconceptions:
{misconception_text}

Student's question:
{question_text}

{tool_instruction}

Teaching rules:

1. Start from what the student likely knows.
2. Match the explanation to the student's level.
3. If mastery is low, focus on fundamentals.
4. If a misconception exists, address it directly.
5. If strategy is "foundation", focus on prerequisites.
6. If strategy is "simpler_explanation", simplify substantially.
7. If strategy is "analogy", use an intuitive analogy.
8. If strategy is "worked_example", provide a structured example.
9. If strategy is "concept_plus_example", explain then demonstrate.
10. If strategy is "interview_reasoning", emphasize reasoning.
11. If strategy is "advanced_application", use a harder application.
12. If strategy is "targeted_reteach", focus on the misconception.
13. If strategy is "edge_cases_and_challenge", go deeper.
14. When a deterministic tool result exists, explicitly incorporate it into the explanation.
15. End with ONE understanding-check question.
16. Do not reveal the answer to that question.
17. Keep the explanation focused.

Return ONLY valid JSON:

{{
  "explanation": "clear teaching explanation",
  "example": "useful example",
  "analogy": "simple analogy when appropriate",
  "key_points": [
    "key point 1",
    "key point 2"
  ],
  "understanding_check": "one question testing understanding"
}}
"""

        raw = await self.llm.generate(
            prompt,
            json_mode=True,
            temperature=0.4,
            max_tokens=1400,
        )

        data = parse_llm_json(raw)

        key_points = data.get(
            "key_points",
            [],
        )

        if not isinstance(key_points, list):
            key_points = [str(key_points)]

        content = Explanation(
            explanation=str(
                data.get(
                    "explanation",
                    "",
                )
            ),
            example=str(
                data.get(
                    "example",
                    "",
                )
            ),
            analogy=str(
                data.get(
                    "analogy",
                    "",
                )
            ),
            key_points=[
                str(item)
                for item in key_points
            ],
            understanding_check=(
                str(
                    data["understanding_check"]
                )
                if data.get("understanding_check")
                else None
            ),
        )

        session["last_question"] = (
            content.understanding_check
        )

        return TeachResponse(
            session_id=session["session_id"],
            topic=topic,
            level=level,
            mode=mode,
            content=content,
            strategy=strategy,
            difficulty=difficulty,
            tool_result=tool_result,
        )


teacher = Teacher()