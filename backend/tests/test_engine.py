import pytest

from app.engine.knowledge import knowledge_graph
from app.engine.mastery import mastery_engine
from app.core.config import get_settings
from app.engine.image_router import image_router
from app.engine.misconception import (
    misconception_engine,
)
from app.engine.planner import planner
from app.engine.rag import rag_engine
from app.engine.student_model import (
    student_model,
)
from app.engine.tool_executor import (
    ToolExecutor,
)
from app.engine.tool_router import (
    tool_router,
)
from app.memory.document_store import (
    DocumentStore,
)
@pytest.fixture(autouse=True)
def clear_settings_cache():
    get_settings.cache_clear()
    yield
    get_settings.cache_clear()

def test_knowledge_direct():
    result = knowledge_graph.prerequisites(
        "ohms law"
    )

    assert "voltage" in result
    assert "current" in result


def test_knowledge_recursive():
    result = knowledge_graph.all_prerequisites(
        "transformers"
    )

    assert "magnetic fields" in result
    assert "electromagnetic induction" in result


def test_missing_prerequisites():
    result = knowledge_graph.missing_prerequisites(
        "transformers",
        {
            "magnetic fields": 0.9,
            "electromagnetic induction": 0.2,
        },
    )

    assert "electromagnetic induction" in result


def test_student_prerequisite():
    session = {
        "student_id": "test-rag-student",
        "topic": "transformers",
        "mastery": 0.0,
        "difficulty": 1,
        "misconceptions": [],
        "turn": 0,
    }

    result = student_model.prerequisite_analysis(
        session
    )

    assert result["ready_for_topic"] is False
    assert result["missing_prerequisites"]


def test_planner_prerequisite():
    session = {
        "mastery": 0.2,
        "difficulty": 1,
        "misconceptions": [],
        "missing_prerequisites": [
            "magnetic fields"
        ],
        "mode": "learn",
    }

    result = planner.next_action(session)

    assert result["action"] == "prerequisite"


def test_planner_misconception():
    session = {
        "mastery": 0.5,
        "difficulty": 2,
        "misconceptions": [
            "voltage and current are the same thing"
        ],
        "missing_prerequisites": [],
        "mode": "learn",
    }

    result = planner.next_action(session)

    assert result["action"] == "reteach"


def test_mastery_update():
    session = {
        "mastery": 0.0,
    }

    value = mastery_engine.update(
        session,
        score=1.0,
        difficulty=1,
    )

    assert value > 0
    assert value <= 1


def test_mastery_level():
    assert mastery_engine.level(0.1) == "beginner"
    assert mastery_engine.level(0.95) == "mastered"


def test_misconception_engine():
    session = {
        "misconceptions": []
    }

    misconception_engine.add(
        session,
        "current is voltage",
    )

    assert misconception_engine.has(session)

    misconception_engine.resolve_all(
        session
    )

    assert not misconception_engine.has(
        session
    )


def test_duplicate_misconception():
    session = {
        "misconceptions": []
    }

    misconception_engine.add(
        session,
        "current is voltage",
    )

    misconception_engine.add(
        session,
        "current is voltage",
    )

    assert len(
        session["misconceptions"]
    ) == 1


def test_planner_low_score():
    session = {
        "mastery": 0.2,
        "difficulty": 2,
        "misconceptions": [],
        "missing_prerequisites": [],
        "mode": "learn",
    }

    evaluation = type(
        "Evaluation",
        (),
        {
            "score": 0.2,
            "confidence": 0.8,
        },
    )()

    result = planner.next_action(
        session,
        evaluation,
    )

    assert result["action"] == "simplify"


def test_planner_high_mastery():
    session = {
        "mastery": 0.9,
        "difficulty": 3,
        "misconceptions": [],
        "missing_prerequisites": [],
        "mode": "learn",
    }

    evaluation = type(
        "Evaluation",
        (),
        {
            "score": 0.95,
            "confidence": 0.95,
        },
    )()

    result = planner.next_action(
        session,
        evaluation,
    )

    assert result["action"] == "challenge"
    assert result["difficulty"] == 4


def test_tool_router_calculator():
    result = tool_router.choose(
        "calculate 25 * 4"
    )

    assert result["tool"] == "calculator"


def test_tool_router_sympy():
    result = tool_router.choose(
        "differentiate x^2"
    )

    assert result["tool"] == "sympy"


def test_tool_router_no_tool():
    result = tool_router.choose(
        "Explain Kirchhoff's voltage law"
    )

    assert result["tool"] is None


@pytest.mark.asyncio
async def test_tool_executor_limit():

    executor = ToolExecutor(
        max_calls=1
    )

    first = await executor.execute(
        "calculator",
        expression="2 + 2",
    )

    second = await executor.execute(
        "calculator",
        expression="3 + 3",
    )

    assert first["success"] is True
    assert first["result"]["result"] == 4

    assert second["success"] is False


def test_rag_chunking():

    text = (
        "Voltage is the electrical potential difference. "
        * 100
    )

    chunks = rag_engine.chunk_text(
        text,
        chunk_size=200,
        overlap=30,
    )

    assert len(chunks) > 1

    assert all(
        isinstance(chunk, str)
        for chunk in chunks
    )


def test_rag_cleaning():

    text = "Voltage\x00   is\n\n\n electrical."

    chunks = rag_engine.chunk_text(
        text,
        chunk_size=100,
        overlap=10,
    )

    assert chunks
    assert "\x00" not in chunks[0]


def test_document_store_ingest_and_search(
    tmp_path,
):

    database = tmp_path / "rag_test.db"

    store = DocumentStore(
        str(database)
    )

    from app.engine.rag import RAGEngine

    rag = RAGEngine(store)

    result = rag.ingest(
        document_id="doc-1",
        student_id="student-1",
        filename="circuits.txt",
        text=(
            "Ohm's law states that voltage equals "
            "current multiplied by resistance."
        ),
    )

    assert result["chunks"] >= 1

    matches = rag.retrieve(
        student_id="student-1",
        query="voltage current resistance",
    )

    assert matches
    assert (
        "voltage"
        in matches[0]["text"].lower()
    )


def test_document_store_student_isolation(
    tmp_path,
):

    database = tmp_path / "isolation.db"

    store = DocumentStore(
        str(database)
    )

    from app.engine.rag import RAGEngine

    rag = RAGEngine(store)

    rag.ingest(
        document_id="doc-student-a",
        student_id="student-a",
        filename="a.txt",
        text="transformer magnetic flux",
    )

    rag.ingest(
        document_id="doc-student-b",
        student_id="student-b",
        filename="b.txt",
        text="transformer magnetic flux",
    )

    matches = rag.retrieve(
        student_id="student-a",
        query="transformer flux",
    )

    assert matches

    assert all(
        item["student_id"] == "student-a"
        for item in matches
    )


def test_rag_context():

    from app.engine.rag import RAGEngine

    class FakeStore:

        def search(
            self,
            student_id,
            query,
            limit,
        ):
            return [
                {
                    "filename": "notes.pdf",
                    "document_id": "doc-1",
                    "chunk_id": "chunk-1",
                    "text": (
                        "A transformer transfers "
                        "electrical energy through "
                        "electromagnetic induction."
                    ),
                    "score": 2.0,
                }
            ]

    rag = RAGEngine(FakeStore())

    result = rag.build_context(
        student_id="student-1",
        query="transformer",
    )

    assert result["found"] is True
    assert "electromagnetic induction" in (
        result["context"]
    )
    assert result["sources"]

@pytest.mark.asyncio
async def test_mock_provider_grounds_deterministic_tool_result():

    from app.providers.mock import MockProvider

    provider = MockProvider()

    prompt = """
You are Nexora, an adaptive AI teacher.

Student's question:
Calculate 230 / 10

A deterministic tool was executed for this question.

AUTHORITATIVE TOOL RESULT:
{'result': 23}

IMPORTANT:
- Treat the deterministic tool result as authoritative.
- Use the result directly in your explanation.
"""

    raw = await provider.generate(
        prompt,
        json_mode=True,
    )

    import json

    result = json.loads(raw)

    assert "23" in result["explanation"]
    assert "23" in result["example"]
    assert any(
        "23" in point
        for point in result["key_points"]
    )


def test_teach_response_contains_tool_result():

    from app.models.responses import (
        Explanation,
        TeachResponse,
    )

    response = TeachResponse(
        session_id="test-session",
        topic="Calculate 230 / 10",
        level="beginner",
        mode="learn",
        content=Explanation(
            explanation="230 ÷ 10 = 23",
        ),
        strategy="direct_explanation",
        difficulty=1,
        tool_result={
            "result": 23
        },
    )

    assert response.tool_result is not None
    assert response.tool_result["result"] == 23


@pytest.mark.asyncio
async def test_mock_provider_without_tool_result_remains_generic():

    from app.providers.mock import MockProvider

    provider = MockProvider()

    raw = await provider.generate(
        """
Student's question:
Explain Kirchhoff's voltage law.

No deterministic tool result is available.
""",
        json_mode=True,
    )

    import json

    result = json.loads(raw)

    assert (
        "23"
        not in result["explanation"]
    )
def test_image_router_avoids_visuals_for_calculation():
    result = image_router.choose("Calculate 230 / 10")

    assert result["use_image"] is False
    assert result["query"] == ""


def test_image_router_detects_conceptual_visual_request():
    result = image_router.choose("Explain how a transformer works")

    assert result["use_image"] is True
    assert "transformer" in result["query"]
    assert "educational diagram" in result["query"]


def test_image_router_detects_explicit_diagram_request():
    result = image_router.choose("Show me a transformer diagram")

    assert result["use_image"] is True
    assert "transformer" in result["query"]


def test_image_router_avoids_visuals_for_differentiation():
    result = image_router.choose("Differentiate x^2")

    assert result["use_image"] is False


def test_image_router_detects_resistor_concept():
    result = image_router.choose("What is a resistor?")

    assert result["use_image"] is True
    assert "resistor" in result["query"]


def test_image_router_avoids_visuals_for_quiz():
    result = image_router.choose("Quiz me on transformers")

    assert result["use_image"] is False
@pytest.mark.asyncio
async def test_google_image_search_rejects_empty_query():
    from app.tools.image_search import GoogleImageSearchTool

    tool = GoogleImageSearchTool()

    result = await tool.execute("")

    assert result["success"] is False
    assert result["results"] == []
    assert "cannot be empty" in result["error"]


@pytest.mark.asyncio
async def test_google_image_search_reports_unconfigured_tool(monkeypatch):
    from app.tools.image_search import GoogleImageSearchTool

    monkeypatch.delenv("GOOGLE_CSE_API_KEY", raising=False)
    monkeypatch.delenv("GOOGLE_CSE_ID", raising=False)

    tool = GoogleImageSearchTool()

    result = await tool.execute("transformer educational diagram")

    assert result["success"] is False
    assert result["configured"] is False
    assert result["results"] == []
    assert "not configured" in result["error"]


@pytest.mark.asyncio
async def test_google_image_search_normalizes_results(monkeypatch):
    from app.tools.image_search import GoogleImageSearchTool

    monkeypatch.setenv("GOOGLE_CSE_API_KEY", "test-key")
    monkeypatch.setenv("GOOGLE_CSE_ID", "test-cse")

    tool = GoogleImageSearchTool()

    class FakeResponse:
        def raise_for_status(self):
            pass

        def json(self):
            return {
                "items": [
                    {
                        "title": "Transformer Diagram",
                        "link": "https://example.com/transformer.jpg",
                        "displayLink": "example.com",
                        "image": {
                            "thumbnailLink": "https://example.com/thumb.jpg",
                            "contextLink": "https://example.com/page",
                            "width": 1200,
                            "height": 800,
                            "byteSize": 123456,
                        },
                    }
                ]
            }

    class FakeAsyncClient:
        def __init__(self, *args, **kwargs):
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):
            pass

        async def get(self, *args, **kwargs):
            return FakeResponse()

    monkeypatch.setattr(
        "app.tools.image_search.httpx.AsyncClient",
        FakeAsyncClient,
    )

    result = await tool.execute(
        "transformer educational diagram",
        limit=4,
    )

    assert result["success"] is True
    assert result["configured"] is True
    assert result["query"] == "transformer educational diagram"
    assert result["total"] == 1

    image = result["results"][0]

    assert image["title"] == "Transformer Diagram"
    assert image["image_url"] == "https://example.com/transformer.jpg"
    assert image["thumbnail_url"] == "https://example.com/thumb.jpg"
    assert image["source_url"] == "https://example.com/page"
    assert image["source_name"] == "example.com"
    assert image["width"] == 1200
    assert image["height"] == 800
    assert image["byte_size"] == 123456


@pytest.mark.asyncio
async def test_google_image_search_skips_items_without_image_url(
    monkeypatch,
):
    from app.tools.image_search import GoogleImageSearchTool

    monkeypatch.setenv("GOOGLE_CSE_API_KEY", "test-key")
    monkeypatch.setenv("GOOGLE_CSE_ID", "test-cse")

    tool = GoogleImageSearchTool()

    class FakeResponse:
        def raise_for_status(self):
            pass

        def json(self):
            return {
                "items": [
                    {
                        "title": "Invalid image",
                        "link": "",
                        "image": {},
                    },
                    {
                        "title": "Valid image",
                        "link": "https://example.com/valid.jpg",
                        "image": {
                            "thumbnailLink": "https://example.com/thumb.jpg",
                        },
                    },
                ]
            }

    class FakeAsyncClient:
        def __init__(self, *args, **kwargs):
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):
            pass

        async def get(self, *args, **kwargs):
            return FakeResponse()

    monkeypatch.setattr(
        "app.tools.image_search.httpx.AsyncClient",
        FakeAsyncClient,
    )

    result = await tool.execute("resistor diagram")

    assert result["success"] is True
    assert result["total"] == 1
    assert result["results"][0]["title"] == "Valid image"


@pytest.mark.asyncio
async def test_google_image_search_handles_http_error(monkeypatch):
    from app.tools.image_search import GoogleImageSearchTool

    monkeypatch.setenv("GOOGLE_CSE_API_KEY", "test-key")
    monkeypatch.setenv("GOOGLE_CSE_ID", "test-cse")

    tool = GoogleImageSearchTool()

    import httpx

    request = httpx.Request(
        "GET",
        "https://www.googleapis.com/customsearch/v1",
    )

    response = httpx.Response(
        403,
        request=request,
        text="Invalid API key",
    )

    class FakeAsyncClient:
        def __init__(self, *args, **kwargs):
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):
            pass

        async def get(self, *args, **kwargs):
            raise httpx.HTTPStatusError(
                "Google API error",
                request=request,
                response=response,
            )

    monkeypatch.setattr(
        "app.tools.image_search.httpx.AsyncClient",
        FakeAsyncClient,
    )

    result = await tool.execute("transformer diagram")

    assert result["success"] is False
    assert result["configured"] is True
    assert result["results"] == []
    assert "HTTP 403" in result["error"]

@pytest.mark.asyncio
async def test_orchestrator_attaches_image_search_results():
    from app.engine.orchestrator import Orchestrator

    class FakeImageSearch:
        async def execute(self, **kwargs):
            return {
                "success": True,
                "configured": True,
                "query": kwargs["query"],
                "results": [
                    {
                        "title": "Transformer Diagram",
                        "image_url": "https://example.com/transformer.jpg",
                        "thumbnail_url": "https://example.com/thumb.jpg",
                        "source_url": "https://example.com/page",
                        "source_name": "example.com",
                        "width": 1200,
                        "height": 800,
                    },
                    {
                        "title": "Transformer Working Principle",
                        "image_url": "https://example.com/working.jpg",
                        "thumbnail_url": "https://example.com/working-thumb.jpg",
                        "source_url": "https://example.com/working",
                        "source_name": "example.com",
                        "width": 1000,
                        "height": 700,
                    },
                ],
            }

    orchestrator = Orchestrator()
    orchestrator.image_search = FakeImageSearch()

    response = await orchestrator.handle_teach(
        question="Explain how a transformer works",
        student_id="image-test-student",
        mode="learn",
        level="beginner",
    )

    assert response is not None
    assert response.content is not None
    assert len(response.content.visuals) == 2

    first = response.content.visuals[0]

    assert first.title == "Transformer Diagram"
    assert first.image_url == "https://example.com/transformer.jpg"
    assert first.thumbnail_url == "https://example.com/thumb.jpg"
    assert first.source_url == "https://example.com/page"
    assert first.source_name == "example.com"
    assert first.query != ""


@pytest.mark.asyncio
async def test_orchestrator_continues_when_image_search_fails():
    from app.engine.orchestrator import Orchestrator

    class FailingImageSearch:
        async def execute(self, **kwargs):
            return {
                "success": False,
                "configured": True,
                "query": kwargs["query"],
                "results": [],
                "error": "Simulated image search failure.",
            }

    orchestrator = Orchestrator()
    orchestrator.image_search = FailingImageSearch()

    response = await orchestrator.handle_teach(
        question="Explain how a transformer works",
        student_id="image-failure-test",
        mode="learn",
        level="beginner",
    )

    assert response is not None
    assert response.content is not None
    assert isinstance(response.content.visuals, list)
    assert response.content.visuals == []

@pytest.mark.asyncio
async def test_orchestrator_does_not_call_image_search_when_disabled(
    monkeypatch,
):
    from app.core.config import get_settings
    from app.engine.orchestrator import Orchestrator

    monkeypatch.setenv("IMAGE_SEARCH_ENABLED", "false")
    get_settings.cache_clear()

    class ForbiddenImageSearch:
        async def execute(self, **kwargs):
            pytest.fail(
                "Image search provider was called while image search was disabled."
            )

    orchestrator = Orchestrator()
    orchestrator.image_search = ForbiddenImageSearch()

    response = await orchestrator.handle_teach(
        question="Explain how a transformer works",
        student_id="image-disabled-test",
        mode="learn",
        level="beginner",
    )

    assert response is not None
    assert response.content is not None
    assert response.content.visuals == []

    get_settings.cache_clear()