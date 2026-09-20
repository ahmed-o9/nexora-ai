from __future__ import annotations

import re
from typing import Any, Dict


class ImageRouter:
    """
    Determines whether a student's question would benefit from
    an educational visual and creates a focused image-search query.
    """

    VISUAL_PATTERNS = (
        r"\bdiagram\b",
        r"\bfigure\b",
        r"\bvisual\b",
        r"\bimage\b",
        r"\bpicture\b",
        r"\bshow me\b",
        r"\bshow how\b",
        r"\bvisualize\b",
        r"\bconstruction\b",
        r"\bworking\b",
        r"\bworking principle\b",
        r"\bblock diagram\b",
        r"\bcircuit diagram\b",
        r"\bwaveform\b",
        r"\bphasor\b",
        r"\bgraph\b",
        r"\bplot\b",
        r"\bstructure\b",
        r"\banatomy\b",
        r"\barchitecture\b",
        r"\bflowchart\b",
        r"\bprocess\b",
    )

    CONCEPT_PATTERNS = (
        r"\bexplain\b",
        r"\bhow does\b",
        r"\bhow do\b",
        r"\bwhat is\b",
        r"\bwhy does\b",
        r"\bwhy is\b",
        r"\bprinciple\b",
        r"\bconcept\b",
        r"\bunderstand\b",
        r"\blearn\b",
    )

    NO_IMAGE_PATTERNS = (
        r"\bcalculate\b",
        r"\bcompute\b",
        r"\bsolve\b",
        r"\bdifferentiate\b",
        r"\bintegrate\b",
        r"\bintegral\b",
        r"\bderivative\b",
        r"\bsimplify\b",
        r"\bfactor\b",
        r"\bexpand\b",
        r"\bquiz me\b",
        r"\bquiz\b",
        r"\bmcq\b",
        r"\bmultiple choice\b",
        r"\btrue or false\b",
    )

    VISUAL_KEYWORDS = (
        "transformer",
        "motor",
        "generator",
        "induction",
        "electromagnetic",
        "magnetic field",
        "electric field",
        "diode",
        "transistor",
        "mosfet",
        "bjt",
        "op amp",
        "operational amplifier",
        "rectifier",
        "oscillator",
        "amplifier",
        "circuit",
        "phasor",
        "impedance",
        "capacitor",
        "inductor",
        "resistor",
        "semiconductor",
        "microcontroller",
        "microprocessor",
        "sensor",
        "arduino",
        "iot",
        "network",
        "algorithm",
        "data structure",
        "binary tree",
        "graph",
        "stack",
        "queue",
        "linked list",
    )

    def choose(self, question: str) -> Dict[str, Any]:
        text = self._clean(question)

        if not text:
            return {
                "use_image": False,
                "reason": "Empty question.",
                "query": "",
            }

        if self._matches(text, self.NO_IMAGE_PATTERNS):
            return {
                "use_image": False,
                "reason": "The request is primarily computational or assessment-based.",
                "query": "",
            }

        explicit_visual = self._matches(text, self.VISUAL_PATTERNS)
        conceptual = self._matches(text, self.CONCEPT_PATTERNS)
        domain_visual = any(keyword in text for keyword in self.VISUAL_KEYWORDS)

        if explicit_visual:
            return {
                "use_image": True,
                "reason": "The student explicitly requested or strongly implied a visual.",
                "query": self._build_query(text),
            }

        if conceptual and domain_visual:
            return {
                "use_image": True,
                "reason": "The question describes a technical concept that benefits from a visual.",
                "query": self._build_query(text),
            }

        return {
            "use_image": False,
            "reason": "A visual is not clearly necessary for this request.",
            "query": "",
        }

    def _build_query(self, text: str) -> str:
        text = re.sub(
            r"\b(according to my notes|according to my document)\b",
            "",
            text,
            flags=re.IGNORECASE,
        )

        text = re.sub(
            r"\b(explain to me|explain|teach me|help me understand)\b",
            "",
            text,
            flags=re.IGNORECASE,
        )

        text = re.sub(
            r"\b(can you|please|show me|tell me|what is|why is|why does|how does)\b",
            "",
            text,
            flags=re.IGNORECASE,
        )

        text = re.sub(r"\s+", " ", text).strip()

        if not text:
            return "engineering educational diagram"

        return f"{text} educational diagram working principle"

    @staticmethod
    def _clean(text: str) -> str:
        return re.sub(r"\s+", " ", text.lower().strip())

    @staticmethod
    def _matches(text: str, patterns: tuple[str, ...]) -> bool:
        return any(re.search(pattern, text) for pattern in patterns)


image_router = ImageRouter()