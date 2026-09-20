import json

from typing import Any, Optional

from .base import BaseProvider


class MockProvider(BaseProvider):
    """
    Deterministic provider used for development and tests.

    It requires no API key and makes it possible to test the complete
    Nexora engine before connecting a real LLM.

    The mock provider also respects deterministic tool results so that
    local development accurately represents Nexora's tool-grounding
    behavior.
    """

    name = "mock"

    @staticmethod
    def _extract_tool_result(
        prompt: str,
    ) -> Optional[str]:
        """
        Extract the authoritative deterministic tool result from
        the teacher prompt.
        """

        marker = (
            "AUTHORITATIVE TOOL RESULT:"
        )

        if marker not in prompt:
            return None

        section = prompt.split(
            marker,
            1,
        )[1]

        section = section.split(
            "\n\nIMPORTANT:",
            1,
        )[0].strip()

        if not section:
            return None

        return section

    @staticmethod
    def _format_tool_result(
        tool_result: str,
    ) -> tuple[str, str, str]:
        """
        Convert the internal deterministic tool-result representation
        into student-friendly text.

        Returns:
            display_result
            explanation
            example
        """

        try:
            parsed = json.loads(
                tool_result.replace(
                    "'",
                    '"',
                )
            )
        except (json.JSONDecodeError, TypeError):
            parsed = None

        if isinstance(parsed, dict):

            expression = parsed.get(
                "expression"
            )

            result = parsed.get(
                "result"
            )

            if expression is not None and result is not None:

                # Avoid displaying unnecessary .0 for whole numbers.
                if isinstance(result, float) and result.is_integer():
                    result_text = str(
                        int(result)
                    )
                else:
                    result_text = str(
                        result
                    )

                display_result = (
                    f"{expression} = {result_text}"
                )

                explanation = (
                    f"{expression} = {result_text}. "
                    f"The calculator verified that the result is "
                    f"{result_text}."
                )

                example = (
                    f"The calculation {expression} gives "
                    f"{result_text}."
                )

                return (
                    display_result,
                    explanation,
                    example,
                )

        # Safe fallback if the tool result is not a calculation dict.
        return (
            tool_result,
            (
                "The deterministic tool produced the result "
                f"{tool_result}. "
                "Because the result comes from the tool, "
                "we use it directly."
            ),
            (
                f"The tool returned {tool_result}."
            ),
        )

    async def generate(
        self,
        prompt: str,
        *,
        system_instruction: Optional[str] = None,
        json_mode: bool = False,
        temperature: float = 0.4,
        max_tokens: int = 1500,
        **kwargs: Any,
    ) -> str:

        prompt_lower = prompt.lower()

        # Quiz response.
        if (
            "quiz" in prompt_lower
            or "correct_answer" in prompt_lower
        ):
            response = {
                "question": "What is the main idea being tested?",
                "qtype": "multiple_choice",
                "options": [
                    "Understanding the fundamental concept",
                    "Memorizing an unrelated fact",
                    "Ignoring the underlying principle",
                    "None of the above",
                ],
                "correct_answer": (
                    "Understanding the fundamental concept"
                ),
                "explanation": (
                    "The correct answer focuses on understanding "
                    "the underlying concept."
                ),
                "difficulty": 1,
            }

        # Evaluation response.
        elif (
            "evaluate" in prompt_lower
            or "student answer" in prompt_lower
            or "correct" in prompt_lower
        ):
            response = {
                "correct": True,
                "score": 0.85,
                "feedback": (
                    "Good answer. You identified the main idea correctly. "
                    "Try explaining the mechanism in one more step."
                ),
                "misconception": None,
                "confidence": 0.85,
            }

        # Normal teaching response.
        else:

            tool_result = self._extract_tool_result(
                prompt
            )

            if tool_result is not None:

                (
                    display_result,
                    explanation,
                    example,
                ) = self._format_tool_result(
                    tool_result
                )

                response = {
                    "topic": "Requested topic",
                    "level": "beginner",
                    "explanation": explanation,
                    "example": example,
                    "analogy": (
                        "Think of the calculator as a reliable "
                        "checking tool: it performs the arithmetic, "
                        "and we use that verified result to explain "
                        "the answer."
                    ),
                    "key_points": [
                        f"The calculation is {display_result}.",
                        "The calculator verified the result.",
                        "The verified result should be used directly.",
                    ],
                    "understanding_check": (
                        "Can you explain what the calculated result "
                        "represents?"
                    ),
                    "strategy": "direct_explanation",
                    "difficulty": 1,
                }

            else:

                response = {
                    "topic": "Requested topic",
                    "level": "beginner",
                    "explanation": (
                        "Let's understand the idea from the basics. "
                        "First identify the main concept, then understand "
                        "how its parts interact, and finally connect it "
                        "to a practical example."
                    ),
                    "example": (
                        "Think about the concept as a simple real-world "
                        "system where each part has a specific role."
                    ),
                    "analogy": (
                        "A useful way to think about it is like a teacher "
                        "building an idea one layer at a time."
                    ),
                    "key_points": [
                        "Start with the basic definition.",
                        "Understand the role of each part.",
                        "Connect the parts to the overall behavior.",
                    ],
                    "understanding_check": (
                        "In your own words, what is the main idea?"
                    ),
                    "strategy": "direct_explanation",
                    "difficulty": 1,
                }

        if json_mode:
            return json.dumps(
                response
            )

        return response["explanation"]