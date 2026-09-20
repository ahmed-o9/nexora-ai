from typing import Any, Dict


class MasteryEngine:

    def update(
        self,
        session: Dict[str, Any],
        score: float,
        difficulty: int = 1,
    ) -> float:

        old_mastery = float(
            session.get(
                "mastery",
                0.0,
            )
        )

        score = max(
            0.0,
            min(
                1.0,
                float(score),
            ),
        )

        difficulty = max(
            1,
            min(
                5,
                int(difficulty),
            ),
        )

        # Harder questions provide slightly stronger
        # evidence of mastery.
        difficulty_factor = (
            0.90
            + (difficulty - 1) * 0.025
        )

        effective_score = (
            score * difficulty_factor
        )

        # Keep historical mastery while allowing
        # new evidence to influence it.
        new_mastery = (
            old_mastery * 0.65
            + effective_score * 0.35
        )

        # A very strong answer at a higher difficulty
        # should never decrease mastery.
        if score >= 0.9 and difficulty >= 3:
            new_mastery = max(
                new_mastery,
                old_mastery,
            )

        new_mastery = max(
            0.0,
            min(
                1.0,
                new_mastery,
            ),
        )

        session["mastery"] = new_mastery

        return new_mastery

    def level(
        self,
        mastery: float,
    ) -> str:

        mastery = float(mastery)

        if mastery < 0.25:
            return "beginner"

        if mastery < 0.50:
            return "developing"

        if mastery < 0.75:
            return "intermediate"

        if mastery < 0.90:
            return "advanced"

        return "mastered"

    def should_increase_difficulty(
        self,
        mastery: float,
        difficulty: int,
    ) -> bool:

        return (
            mastery >= 0.80
            and difficulty < 5
        )

    def should_reteach(
        self,
        score: float,
        misconceptions: list,
    ) -> bool:

        return (
            float(score) < 0.4
            or bool(misconceptions)
        )


mastery_engine = MasteryEngine()