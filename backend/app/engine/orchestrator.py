
from __future__ import annotations

from typing import Any, Dict
from uuid import uuid4

from .evaluator import evaluator
from .knowledge import knowledge_graph
from .mastery import mastery_engine
from .misconception import misconception_engine
from .planner import planner
from .rag import rag_engine
from .student_model import student_model
from .teacher import teacher
from .tool_executor import tool_executor
from .tool_router import tool_router
from .image_router import image_router

from ..core.exceptions import SessionNotFound
from ..core.config import get_settings
from ..memory.manager import memory
from ..tools.image_search import image_search_tool
from ..models.responses import VisualResult


class Orchestrator:
    def __init__(self):
        self.teacher = teacher
        self.evaluator = evaluator
        self.planner = planner
        self.mastery_engine = mastery_engine
        self.misconception_engine = misconception_engine
        self.student_model = student_model
        self.knowledge_graph = knowledge_graph
        self.tool_router = tool_router
        self.tool_executor = tool_executor
        self.rag = rag_engine
        self.image_router = image_router
        self.image_search = image_search_tool

    async def create_session(
        self,
        topic: str,
        student_id: str = "default",
        mode: str = "learn",
        level: str = "beginner",
    ) -> Dict[str, Any]:
        session = {
            "session_id": str(uuid4()),
            "student_id": student_id,
            "topic": topic,
            "mode": mode,
            "current_level": level,
            "difficulty": 1,
            "mastery": 0.0,
            "turn": 0,
            "strategy": "foundation",
            "misconceptions": [],
            "last_question": "",
            "missing_prerequisites": [],
            "next_prerequisite": None,
            "ready_for_topic": True,

            # Tool intelligence
            "tool_result": None,
            "tool_calls": 0,

            # Document / RAG intelligence
            "rag_context": "",
            "rag_sources": [],

            # Educational image intelligence
            "image_search": {
                "requested": False,
                "reason": "",
                "query": "",
                "results": [],
            },
        }

        memory.sessions.save(session)
        return session

    def get_session(
        self,
        session_id: str,
    ) -> Dict[str, Any]:
        session = memory.sessions.get(session_id)

        if session is None:
            raise SessionNotFound(session_id)

        return session

    def _save(
        self,
        session: Dict[str, Any],
    ) -> None:
        memory.sessions.save(session)

    async def _teach_with_context(
        self,
        session: Dict[str, Any],
        question: str,
    ):
        """
        Build all available teaching context before asking the teacher
        to generate the response.

        Context pipeline:
            Student question
                    |
                    +--> Mathematical tools
                    |
                    +--> Student document RAG
                    |
                    +--> Educational image intelligence
                    |
                    +--> Adaptive teacher
                    |
                    +--> Structured response + visuals

        Important:
        Image-search failure must never stop the normal teaching flow.

        Tool results are kept as structured session state so the teacher
        can explicitly ground its explanation in deterministic results.
        """

        tool_context = ""
        rag_context = ""
        image_context = ""

        # ---------------------------------------------------------
        # RESET PER-TURN TOOL STATE
        # ---------------------------------------------------------

        # A previous calculation must never leak into a later question.

        session["tool_result"] = None

        # ---------------------------------------------------------
        # TOOL INTELLIGENCE
        # ---------------------------------------------------------

        route = self.tool_router.choose(question)

        if route.get("tool"):
            tool_name = route["tool"]

            try:
                if tool_name == "calculator":
                    expression = self._extract_expression(
                        question
                    )

                    result = await self.tool_executor.calculate(
                        expression
                    )

                elif tool_name == "sympy":
                    operation = self._detect_sympy_operation(
                        question
                    )

                    expression = self._extract_symbolic_expression(
                        question
                    )

                    result = await self.tool_executor.symbolic(
                        operation=operation,
                        expression=expression,
                    )

                else:
                    result = None

                if result and result.get("success"):
                    # Preserve the structured deterministic result.
                    #
                    # The teacher receives this through session state
                    # rather than relying on the result being appended
                    # to the student's question.

                    session["tool_result"] = result["result"]

                    session["tool_calls"] = int(
                        session.get("tool_calls", 0)
                    ) + 1

                    # Keep a human-readable internal context marker
                    # for compatibility/debugging.

                    tool_context = (
                        "\n\nDeterministic tool result available."
                    )

                elif result:
                    session["tool_result"] = {
                        "error": result.get(
                            "error",
                            "Tool execution failed.",
                        )
                    }

            except Exception as exc:
                # Tool failures should not destroy the teaching flow.

                session["tool_result"] = {
                    "error": str(exc)
                }

        # ---------------------------------------------------------
        # DOCUMENT / RAG INTELLIGENCE
        # ---------------------------------------------------------

        rag = self.rag.build_context(
            student_id=session.get(
                "student_id",
                "default",
            ),
            query=question,
            limit=5,
        )

        if rag["found"]:
            session["rag_context"] = rag["context"]
            session["rag_sources"] = rag["sources"]

            rag_context = (
                "\n\nRelevant information from the "
                "student's documents:\n"
                f"{rag['context']}\n\n"
                "Use these sources when relevant. "
                "Do not invent facts that contradict them."
            )

        else:
            session["rag_context"] = ""
            session["rag_sources"] = []

        # ---------------------------------------------------------
        # EDUCATIONAL IMAGE INTELLIGENCE
        # ---------------------------------------------------------

        image_route = self.image_router.choose(
            question
        )

        session["image_search"] = {
            "requested": bool(
                image_route.get(
                    "use_image",
                    False,
                )
            ),
            "reason": str(
                image_route.get(
                    "reason",
                    "",
                )
            ),
            "query": str(
                image_route.get(
                    "query",
                    "",
                )
            ),
            "results": [],
        }

        # Read centralized image-search configuration.
        settings = get_settings()

        if (
            image_route.get("use_image")
            and settings.IMAGE_SEARCH_ENABLED
        ):
            image_query = str(
                image_route.get(
                    "query",
                    "",
                )
            ).strip()

            if image_query:
                try:
                    image_result = await self.image_search.execute(
                        query=image_query,
                        limit=settings.IMAGE_SEARCH_LIMIT,
                        image_type="lineart",
                        image_size="large",
                    )

                    if image_result.get("success"):
                        visuals = []

                        for item in image_result.get(
                            "results",
                            [],
                        ):
                            image_url = item.get(
                                "image_url",
                                "",
                            )

                            if not image_url:
                                continue

                            visual = {
                                **item,
                                "query": image_query,
                            }

                            visuals.append(
                                visual
                            )

                        session["image_search"][
                            "results"
                        ] = visuals

                        if visuals:
                            image_context = (
                                "\n\nEducational visual "
                                "search results are available "
                                "for this explanation.\n"
                                f"Search query: {image_query}\n"
                                f"Number of visuals: "
                                f"{len(visuals)}\n\n"
                                "Explain the concept normally. "
                                "The visuals will be shown "
                                "alongside the explanation "
                                "by the frontend."
                            )

                    else:
                        session["image_search"][
                            "error"
                        ] = image_result.get(
                            "error",
                            "Image search failed.",
                        )

                except Exception as exc:
                    # Image search is an enhancement.
                    # Never allow an image API failure to
                    # break the actual teacher.

                    session["image_search"][
                        "error"
                    ] = str(exc)

        # ---------------------------------------------------------
        # TEACHER
        # ---------------------------------------------------------

        # Tool results are NOT appended to the student's question.
        #
        # The Teacher receives the original question plus RAG/image
        # context while reading the authoritative tool result directly
        # from session["tool_result"].

        teaching_question = (
            question
            + rag_context
            + image_context
        )

        response = await self.teacher.teach(
            session,
            question=teaching_question,
        )

        # ---------------------------------------------------------
        # ATTACH EDUCATIONAL VISUALS
        # ---------------------------------------------------------

        # The Teacher remains responsible for generating the
        # explanation.
        #
        # The Orchestrator attaches external educational visuals
        # to the structured response.
        #
        # This keeps the LLM independent from the image provider.

        image_results = (
            session.get(
                "image_search",
                {},
            ).get(
                "results",
                [],
            )
        )

        response.content.visuals = [
            VisualResult(
                title=str(
                    item.get(
                        "title",
                        "",
                    )
                ),
                image_url=str(
                    item.get(
                        "image_url",
                        "",
                    )
                ),
                thumbnail_url=str(
                    item.get(
                        "thumbnail_url",
                        "",
                    )
                ),
                source_url=str(
                    item.get(
                        "source_url",
                        "",
                    )
                ),
                source_name=str(
                    item.get(
                        "source_name",
                        "",
                    )
                ),
                query=str(
                    item.get(
                        "query",
                        "",
                    )
                ),
                width=item.get(
                    "width"
                ),
                height=item.get(
                    "height"
                ),
            )
            for item in image_results
            if item.get("image_url")
        ]

        return response

    async def handle_teach(
        self,
        question: str,
        student_id: str = "default",
        mode: str = "learn",
        level: str = "beginner",
    ):
        session = None

        sessions = memory.sessions.all_for_student(
            student_id
        )

        if sessions:
            for candidate in reversed(sessions):
                topic = candidate.get(
                    "topic",
                    "",
                )

                if (
                    topic
                    and topic.lower() in question.lower()
                ):
                    session = candidate
                    break

        if session is None:
            session = await self.create_session(
                topic=question,
                student_id=student_id,
                mode=mode,
                level=level,
            )

        session["turn"] = int(
            session.get("turn", 0)
        ) + 1

        session["mode"] = (
            mode
            or session.get(
                "mode",
                "learn",
            )
        )

        if level:
            session["current_level"] = level

        self.student_model.enrich_session(
            session
        )

        prerequisite = session.get(
            "next_prerequisite"
        )

        if (
            prerequisite
            and not session.get(
                "ready_for_topic",
                True,
            )
        ):
            teaching_question = (
                f"Teach me {prerequisite} because "
                f"I need it as a prerequisite for "
                f"{session['topic']}."
            )

            session["strategy"] = "foundation"

        else:
            teaching_question = question

        result = await self._teach_with_context(
            session,
            teaching_question,
        )

        session["last_question"] = (
            result.content.understanding_check
            or ""
        )

        self._save(session)

        return result

    async def handle_answer(
        self,
        session_id: str,
        answer: str,
    ):
        session = self.get_session(
            session_id
        )

        question = session.get(
            "last_question",
            "",
        )

        evaluation = await self.evaluator.evaluate(
            topic=session["topic"],
            question=question,
            answer=answer,
            level=session.get(
                "current_level",
                "beginner",
            ),
            difficulty=int(
                session.get(
                    "difficulty",
                    1,
                )
            ),
        )

        if evaluation.misconception:
            self.misconception_engine.add(
                session,
                evaluation.misconception,
            )

        elif evaluation.correct:
            self.misconception_engine.resolve_all(
                session
            )

        new_mastery = self.mastery_engine.update(
            session,
            score=evaluation.score,
            difficulty=int(
                session.get(
                    "difficulty",
                    1,
                )
            ),
        )

        session["mastery"] = new_mastery

        memory.long_term.update_mastery(
            student_id=session["student_id"],
            topic=session["topic"],
            mastery=new_mastery,
        )

        self.student_model.enrich_session(
            session
        )

        decision = self.planner.next_action(
            session=session,
            evaluation=evaluation,
        )

        next_action = decision["action"]

        session["strategy"] = decision[
            "strategy"
        ]

        if "difficulty" in decision:
            session["difficulty"] = max(
                1,
                min(
                    5,
                    int(
                        decision["difficulty"]
                    ),
                ),
            )

        if (
            session.get("next_prerequisite")
            and evaluation.correct
            and evaluation.score >= 0.7
        ):
            prerequisite = session[
                "next_prerequisite"
            ]

            memory.long_term.update_mastery(
                student_id=session["student_id"],
                topic=prerequisite,
                mastery=evaluation.score,
            )

        session["turn"] = int(
            session.get("turn", 0)
        ) + 1

        self.student_model.enrich_session(
            session
        )

        next_content = None

        if next_action in {
            "reteach",
            "simplify",
            "example",
            "challenge",
            "continue",
            "prerequisite",
        }:
            if next_action == "prerequisite":
                prerequisite = decision.get(
                    "prerequisite"
                )

                teaching_question = (
                    f"Teach me {prerequisite} "
                    "from the foundations."
                )

            else:
                teaching_question = question

            result = await self._teach_with_context(
                session,
                teaching_question,
            )

            next_content = result.content

            session["last_question"] = (
                result.content.understanding_check
                or ""
            )

        self._save(session)

        return {
            "session_id": session_id,
            "evaluation": evaluation,
            "state": session,
            "next_action": next_action,
            "content": next_content,
        }

    async def teach_simpler(
        self,
        session_id: str,
    ):
        session = self.get_session(
            session_id
        )

        session["strategy"] = (
            "simpler_explanation"
        )

        result = await self._teach_with_context(
            session,
            session.get(
                "last_question",
                "",
            ),
        )

        session["last_question"] = (
            result.content.understanding_check
            or ""
        )

        self._save(session)

        return result

    async def teach_example(
        self,
        session_id: str,
    ):
        session = self.get_session(
            session_id
        )

        session["strategy"] = (
            "worked_example"
        )

        result = await self._teach_with_context(
            session,
            session.get(
                "last_question",
                "",
            ),
        )

        session["last_question"] = (
            result.content.understanding_check
            or ""
        )

        self._save(session)

        return result

    @staticmethod
    def _extract_expression(
        question: str,
    ) -> str:
        import re

        matches = re.findall(
            r"[0-9][0-9a-zA-Z_\s**\+\-\*\/\^\(\)\.,]*",
            question,
        )

        if matches:
            expression = matches[-1].strip()
            expression = expression.rstrip(
                "?."
            )
            return expression

        return question.strip()

    @staticmethod
    def _detect_sympy_operation(
        question: str,
    ) -> str:
        text = question.lower()

        if "derivative" in text or "differentiate" in text:
            return "differentiate"

        if "integral" in text or "integrate" in text:
            return "integrate"

        if "factor" in text:
            return "factor"

        if "expand" in text:
            return "expand"

        if "limit" in text:
            return "limit"

        if "solve" in text:
            return "solve"

        return "simplify"

    @staticmethod
    def _extract_symbolic_expression(
        question: str,
    ) -> str:
        import re

        patterns = [
            r"(?:of|for|expression)\s+(.+)$",
            r"(?:derivative|differentiate)\s+(.+)$",
            r"(?:integral|integrate)\s+(.+)$",
            r"(?:factor|expand|simplify)\s+(.+)$",
        ]

        text = question.strip().rstrip("?.")

        for pattern in patterns:
            match = re.search(
                pattern,
                text,
                flags=re.IGNORECASE,
            )

            if match:
                return match.group(1).strip()

        return text


orchestrator = Orchestrator()

