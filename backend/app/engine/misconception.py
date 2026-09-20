from typing import Any, Dict


class MisconceptionEngine:

    def add(
        self,
        session: Dict[str, Any],
        misconception: str,
    ) -> None:

        if not misconception:
            return

        misconception = str(
            misconception
        ).strip()

        if not misconception:
            return

        current = session.setdefault(
            "misconceptions",
            [],
        )

        # Avoid duplicate misconceptions.
        if misconception not in current:
            current.append(misconception)

    def clear(
        self,
        session: Dict[str, Any],
    ) -> None:

        session["misconceptions"] = []

    def has(
        self,
        session: Dict[str, Any],
    ) -> bool:

        return bool(
            session.get(
                "misconceptions",
                [],
            )
        )

    def next_strategy(
        self,
        session: Dict[str, Any],
    ) -> str:

        misconceptions = session.get(
            "misconceptions",
            [],
        )

        if not misconceptions:
            return "direct_explanation"

        # If there is an active misconception,
        # don't immediately increase difficulty.
        return "targeted_reteach"

    def resolve(
        self,
        session: Dict[str, Any],
        misconception: str,
    ) -> None:

        current = session.setdefault(
            "misconceptions",
            [],
        )

        if misconception in current:
            current.remove(
                misconception
            )

    def resolve_all(
        self,
        session: Dict[str, Any],
    ) -> None:

        session["misconceptions"] = []

    def get_primary(
        self,
        session: Dict[str, Any],
    ) -> str:

        misconceptions = session.get(
            "misconceptions",
            [],
        )

        if not misconceptions:
            return ""

        return str(
            misconceptions[0]
        )

    def inspect(
        self,
        session: Dict[str, Any],
    ) -> Dict[str, Any]:

        misconceptions = session.get(
            "misconceptions",
            [],
        )

        return {
            "has_misconception": bool(
                misconceptions
            ),
            "count": len(
                misconceptions
            ),
            "items": list(
                misconceptions
            ),
            "recommended_strategy": (
                self.next_strategy(session)
            ),
        }


misconception_engine = MisconceptionEngine()