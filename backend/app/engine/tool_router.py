from __future__ import annotations

import re
from typing import Any, Dict


class ToolRouter:
    """
    Lightweight deterministic router.

    It deliberately uses rules before an LLM planner.
    This keeps obvious calculations fast and predictable.
    """

    CALCULATION_PATTERNS = (
        r"\bcalculate\b",
        r"\bcompute\b",
        r"\bsolve\b",
        r"\bwhat is\b",
        r"\bevaluate\b",
        r"\bderivative\b",
        r"\bintegral\b",
        r"\bdifferentiate\b",
        r"\bintegrate\b",
        r"\bsimplify\b",
        r"\bfactor\b",
        r"\bexpand\b",
    )

    SYMPY_PATTERNS = (
        r"\bdifferentiat",
        r"\bintegrat",
        r"\bsimplif",
        r"\bfactor",
        r"\bexpand",
        r"\blimit\b",
        r"\bsolve equation",
    )

    def choose(
        self,
        question: str,
    ) -> Dict[str, Any]:

        text = question.lower().strip()

        if not text:
            return {
                "tool": None,
                "reason": "Empty question.",
            }

        if self._matches(
            text,
            self.SYMPY_PATTERNS,
        ):
            return {
                "tool": "sympy",
                "reason": (
                    "The request appears to "
                    "require symbolic mathematics."
                ),
            }

        if self._matches(
            text,
            self.CALCULATION_PATTERNS,
        ) and self._contains_math(
            text
        ):
            return {
                "tool": "calculator",
                "reason": (
                    "The request appears to "
                    "require numerical calculation."
                ),
            }

        return {
            "tool": None,
            "reason": (
                "No deterministic tool is "
                "required."
            ),
        }

    def _matches(
        self,
        text: str,
        patterns: tuple[str, ...],
    ) -> bool:

        return any(
            re.search(pattern, text)
            for pattern in patterns
        )

    def _contains_math(
        self,
        text: str,
    ) -> bool:

        return bool(
            re.search(
                r"\d",
                text,
            )
        ) and bool(
            re.search(
                r"[\+\-\*\/\^\=\(\)]",
                text,
            )
        )


tool_router = ToolRouter()