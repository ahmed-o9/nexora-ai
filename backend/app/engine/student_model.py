from __future__ import annotations

from typing import Any, Dict

from .knowledge import knowledge_graph


class StudentModel:

    """
    Represents Nexora's current belief about the learner.
    """

    def analyze(
        self,
        session: Dict[str, Any],
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

        turn = int(
            session.get(
                "turn",
                0,
            )
        )

        if misconceptions:

            learning_state = "misconception"

        elif mastery < 0.25:

            learning_state = "novice"

        elif mastery < 0.50:

            learning_state = "developing"

        elif mastery < 0.75:

            learning_state = "understanding"

        elif mastery < 0.90:

            learning_state = "strong"

        else:

            learning_state = "mastered"

        if mastery < 0.30:

            recommended_level = "beginner"

        elif mastery < 0.60:

            recommended_level = "intermediate"

        elif mastery < 0.85:

            recommended_level = "advanced"

        else:

            recommended_level = "expert"

        return {
            "learning_state": learning_state,
            "mastery": mastery,
            "difficulty": difficulty,
            "recommended_level": recommended_level,
            "misconception_count": len(
                misconceptions
            ),
            "turn": turn,
            "needs_reteach": (
                bool(misconceptions)
                or mastery < 0.25
            ),
        }

    # ---------------------------------------------------------
    # TOPIC MASTERY
    # ---------------------------------------------------------

    def get_topic_mastery(
        self,
        student_id: str,
    ) -> Dict[str, float]:

        from ..memory.manager import memory

        data = memory.long_term.all_mastery(
            student_id
        )

        if not isinstance(data, dict):
            return {}

        result = {}

        for topic, value in data.items():

            try:
                result[
                    knowledge_graph.normalize(
                        topic
                    )
                ] = float(value)

            except (
                TypeError,
                ValueError,
            ):
                continue

        return result

    # ---------------------------------------------------------
    # PREREQUISITE ANALYSIS
    # ---------------------------------------------------------

    def prerequisite_analysis(
        self,
        session: Dict[str, Any],
    ) -> Dict[str, Any]:

        student_id = session.get(
            "student_id",
            "default",
        )

        topic = session.get(
            "topic",
            "",
        )

        mastery = self.get_topic_mastery(
            student_id
        )

        missing = knowledge_graph.missing_prerequisites(
            topic,
            mastery,
        )

        next_prerequisite = (
            missing[0]
            if missing
            else None
        )

        return {
            "topic": topic,
            "missing_prerequisites": missing,
            "next_prerequisite": (
                next_prerequisite
            ),
            "ready_for_topic": not bool(
                missing
            ),
        }

    # ---------------------------------------------------------
    # ENRICH SESSION
    # ---------------------------------------------------------

    def enrich_session(
        self,
        session: Dict[str, Any],
    ) -> Dict[str, Any]:

        analysis = self.analyze(
            session
        )

        session["student_state"] = (
            analysis[
                "learning_state"
            ]
        )

        if analysis[
            "learning_state"
        ] in {
            "novice",
            "developing",
            "understanding",
            "strong",
            "mastered",
        }:

            session[
                "current_level"
            ] = analysis[
                "recommended_level"
            ]

        prerequisite = (
            self.prerequisite_analysis(
                session
            )
        )

        session[
            "missing_prerequisites"
        ] = prerequisite[
            "missing_prerequisites"
        ]

        session[
            "next_prerequisite"
        ] = prerequisite[
            "next_prerequisite"
        ]

        session[
            "ready_for_topic"
        ] = prerequisite[
            "ready_for_topic"
        ]

        return session


student_model = StudentModel()