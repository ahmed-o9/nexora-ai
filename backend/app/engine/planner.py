from typing import Any, Dict


class Planner:

    def next_action(
        self,
        session: Dict[str, Any],
        evaluation: Any = None,
    ) -> Dict[str, Any]:

        mastery = float(
            session.get(
                "mastery",
                0.0,
            )
        )

        difficulty = int(
            session.get(
                "difficulty",
                1,
            )
        )

        misconceptions = session.get(
            "misconceptions",
            [],
        )

        missing_prerequisites = session.get(
            "missing_prerequisites",
            [],
        )

        mode = session.get(
            "mode",
            "learn",
        )

        score = 0.0
        confidence = 0.5

        if evaluation is not None:

            score = float(
                getattr(
                    evaluation,
                    "score",
                    0.0,
                )
            )

            confidence = float(
                getattr(
                    evaluation,
                    "confidence",
                    0.5,
                )
            )

        # -----------------------------------------------------
        # 1. MISCONCEPTION
        # -----------------------------------------------------

        if misconceptions:

            return {
                "action": "reteach",
                "strategy": "targeted_reteach",
                "difficulty": max(
                    1,
                    difficulty - 1,
                ),
                "reason": (
                    "An unresolved misconception "
                    "requires targeted reteaching."
                ),
            }

        # -----------------------------------------------------
        # 2. PREREQUISITE GAP
        # -----------------------------------------------------

        if missing_prerequisites:

            return {
                "action": "prerequisite",
                "strategy": "foundation",
                "difficulty": 1,
                "prerequisite": (
                    missing_prerequisites[0]
                ),
                "reason": (
                    "A prerequisite concept "
                    "has insufficient mastery."
                ),
            }

        # -----------------------------------------------------
        # 3. WEAK ANSWER
        # -----------------------------------------------------

        if score < 0.4:

            return {
                "action": "simplify",
                "strategy": "simpler_explanation",
                "difficulty": max(
                    1,
                    difficulty - 1,
                ),
                "reason": (
                    "The demonstrated understanding "
                    "is weak."
                ),
            }

        # -----------------------------------------------------
        # 4. PARTIAL + LOW CONFIDENCE
        # -----------------------------------------------------

        if (
            score < 0.7
            and confidence < 0.6
        ):

            return {
                "action": "example",
                "strategy": "concept_plus_example",
                "difficulty": difficulty,
                "reason": (
                    "Understanding is incomplete "
                    "and confidence is low."
                ),
            }

        # -----------------------------------------------------
        # 5. PARTIAL
        # -----------------------------------------------------

        if score < 0.7:

            return {
                "action": "example",
                "strategy": "worked_example",
                "difficulty": difficulty,
                "reason": (
                    "The student needs another "
                    "representation of the concept."
                ),
            }

        # -----------------------------------------------------
        # 6. GOOD
        # -----------------------------------------------------

        if score < 0.9:

            strategy = "worked_example"

            if mode == "exam":
                strategy = "exam_application"

            elif mode == "interview":
                strategy = "interview_reasoning"

            elif mode == "socratic":
                strategy = "socratic_challenge"

            return {
                "action": "continue",
                "strategy": strategy,
                "difficulty": difficulty,
                "reason": (
                    "Understanding is good "
                    "but should be reinforced."
                ),
            }

        # -----------------------------------------------------
        # 7. MASTERED
        # -----------------------------------------------------

        if mastery >= 0.8:

            new_difficulty = min(
                5,
                difficulty + 1,
            )

            if mode == "interview":

                strategy = (
                    "interview_reasoning"
                )

            elif mode == "exam":

                strategy = (
                    "edge_cases_and_challenge"
                )

            elif mode == "socratic":

                strategy = (
                    "socratic_challenge"
                )

            else:

                strategy = (
                    "advanced_application"
                )

            return {
                "action": "challenge",
                "strategy": strategy,
                "difficulty": new_difficulty,
                "reason": (
                    "Strong mastery demonstrated; "
                    "increase challenge."
                ),
            }

        return {
            "action": "continue",
            "strategy": "concept_plus_example",
            "difficulty": difficulty,
            "reason": (
                "Continue strengthening understanding."
            ),
        }

    def plan(
        self,
        session: Dict[str, Any],
    ) -> Dict[str, Any]:

        mastery = float(
            session.get(
                "mastery",
                0.0,
            )
        )

        misconceptions = session.get(
            "misconceptions",
            [],
        )

        missing = session.get(
            "missing_prerequisites",
            [],
        )

        difficulty = int(
            session.get(
                "difficulty",
                1,
            )
        )

        if misconceptions:

            strategy = "targeted_reteach"

        elif missing:

            strategy = "foundation"

        elif mastery < 0.3:

            strategy = "foundation"

        elif mastery < 0.7:

            strategy = "concept_plus_example"

        elif mastery < 0.9:

            strategy = "worked_example"

        else:

            strategy = "advanced_application"

        return {
            "strategy": strategy,
            "difficulty": difficulty,
            "mastery": mastery,
        }


planner = Planner()