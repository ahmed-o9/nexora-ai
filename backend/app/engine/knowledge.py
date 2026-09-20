from __future__ import annotations

from typing import Dict, List, Set


class KnowledgeGraph:

    def __init__(self):

        self.graph: Dict[str, List[str]] = {

            # -------------------------------------------------
            # ELECTRICAL FUNDAMENTALS
            # -------------------------------------------------

            "ohms law": [
                "voltage",
                "current",
                "resistance",
            ],

            "kirchhoff laws": [
                "voltage",
                "current",
                "circuit analysis",
            ],

            "circuit analysis": [
                "voltage",
                "current",
                "resistance",
                "ohms law",
            ],

            # -------------------------------------------------
            # AC
            # -------------------------------------------------

            "ac circuits": [
                "voltage",
                "current",
                "frequency",
                "phase",
            ],

            "phasors": [
                "ac circuits",
                "complex numbers",
                "phase",
            ],

            "impedance": [
                "resistance",
                "inductance",
                "capacitance",
                "phasors",
            ],

            # -------------------------------------------------
            # MAGNETICS
            # -------------------------------------------------

            "magnetic fields": [
                "current",
                "electromagnetism",
            ],

            "electromagnetic induction": [
                "magnetic fields",
                "faradays law",
                "flux",
            ],

            "mutual inductance": [
                "inductance",
                "magnetic fields",
                "electromagnetic induction",
            ],

            # -------------------------------------------------
            # TRANSFORMERS
            # -------------------------------------------------

            "transformers": [
                "ac circuits",
                "magnetic fields",
                "electromagnetic induction",
                "mutual inductance",
            ],

            "transformer equivalent circuit": [
                "transformers",
                "impedance",
                "phasors",
            ],

            # -------------------------------------------------
            # MACHINES
            # -------------------------------------------------

            "dc machines": [
                "magnetic fields",
                "electromagnetic induction",
                "dc circuits",
            ],

            "induction motor": [
                "magnetic fields",
                "ac circuits",
                "electromagnetic induction",
            ],

            "synchronous motor": [
                "magnetic fields",
                "ac circuits",
                "phasors",
            ],

            # -------------------------------------------------
            # ELECTRONICS
            # -------------------------------------------------

            "diode": [
                "voltage",
                "current",
                "semiconductor basics",
            ],

            "transistor": [
                "diode",
                "semiconductor basics",
                "voltage",
                "current",
            ],

            "operational amplifier": [
                "transistor",
                "voltage",
                "current",
                "circuit analysis",
            ],
        }

    # ---------------------------------------------------------
    # NORMALIZATION
    # ---------------------------------------------------------

    def normalize(
        self,
        topic: str,
    ) -> str:

        return " ".join(
            topic.lower().strip().split()
        )

    # ---------------------------------------------------------
    # DIRECT PREREQUISITES
    # ---------------------------------------------------------

    def prerequisites(
        self,
        topic: str,
    ) -> List[str]:

        topic = self.normalize(topic)

        return list(
            self.graph.get(
                topic,
                [],
            )
        )

    # ---------------------------------------------------------
    # RECURSIVE PREREQUISITES
    # ---------------------------------------------------------

    def all_prerequisites(
        self,
        topic: str,
    ) -> List[str]:

        topic = self.normalize(topic)

        visited: Set[str] = set()
        result: List[str] = []

        def visit(node: str):

            if node in visited:
                return

            visited.add(node)

            for prerequisite in self.graph.get(
                node,
                [],
            ):

                visit(prerequisite)

                if prerequisite not in result:
                    result.append(
                        prerequisite
                    )

        visit(topic)

        return result

    # ---------------------------------------------------------
    # MISSING KNOWLEDGE
    # ---------------------------------------------------------

    def missing_prerequisites(
        self,
        topic: str,
        mastery: Dict[str, float],
        threshold: float = 0.65,
    ) -> List[str]:

        prerequisites = self.all_prerequisites(
            topic
        )

        missing = []

        for prerequisite in prerequisites:

            value = float(
                mastery.get(
                    prerequisite,
                    0.0,
                )
            )

            if value < threshold:
                missing.append(
                    prerequisite
                )

        return missing

    # ---------------------------------------------------------
    # NEXT PREREQUISITE
    # ---------------------------------------------------------

    def next_prerequisite(
        self,
        topic: str,
        mastery: Dict[str, float],
    ):

        missing = self.missing_prerequisites(
            topic,
            mastery,
        )

        if not missing:
            return None

        return missing[0]


knowledge_graph = KnowledgeGraph()