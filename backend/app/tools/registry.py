from __future__ import annotations

from typing import Any, Callable, Dict


class ToolRegistry:
    """
    Central registry for Nexora tools.

    The orchestrator can ask for a tool by name without
    knowing the implementation details of that tool.
    """

    def __init__(self) -> None:
        self._tools: Dict[str, Dict[str, Any]] = {}

    def register(
        self,
        name: str,
        description: str,
        handler: Callable[..., Any],
    ) -> None:
        self._tools[name] = {
            "name": name,
            "description": description,
            "handler": handler,
        }

    def get(
        self,
        name: str,
    ) -> Dict[str, Any] | None:
        return self._tools.get(name)

    def names(self) -> list[str]:
        return list(self._tools.keys())

    def describe(self) -> list[Dict[str, str]]:
        return [
            {
                "name": item["name"],
                "description": item["description"],
            }
            for item in self._tools.values()
        ]

    async def execute(
        self,
        name: str,
        **kwargs: Any,
    ) -> Any:

        tool = self.get(name)

        if tool is None:
            raise ValueError(
                f"Unknown tool: {name}"
            )

        handler = tool["handler"]

        result = handler(**kwargs)

        if hasattr(result, "__await__"):
            result = await result

        return result


registry = ToolRegistry()