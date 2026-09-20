from __future__ import annotations

from typing import Any, Dict

from ..tools.calculator import CalculatorTool
from ..tools.sympy_tool import SymPyTool
from ..tools.registry import registry


class ToolExecutor:
    """
    Central executor for Nexora's deterministic tools.

    Responsibilities:
    - Register available tools.
    - Execute synchronous or asynchronous tool handlers.
    - Enforce a maximum number of tool calls.
    - Return a consistent result structure.
    """

    def __init__(self, max_calls: int = 5) -> None:
        self.max_calls = max(1, int(max_calls))
        self.calls = 0

        self.calculator = CalculatorTool()
        self.sympy = SymPyTool()

        self._register_defaults()

    def _register_defaults(self) -> None:
        """
        Register the actual tool instances used by Nexora.
        """

        registry.register(
            name="calculator",
            description="Evaluate safe numerical mathematical expressions.",
            handler=self.calculator.execute,
        )

        registry.register(
            name="sympy",
            description="Perform symbolic mathematical operations.",
            handler=self.sympy.execute,
        )

    def reset(self) -> None:
        """
        Reset the tool-call counter.
        """

        self.calls = 0

    async def execute(
        self,
        tool_name: str,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        Execute a registered tool while enforcing the call limit.
        """

        if self.calls >= self.max_calls:
            return {
                "success": False,
                "tool": tool_name,
                "error": "Maximum tool-call limit reached.",
            }

        self.calls += 1

        try:
            result = await registry.execute(
                tool_name,
                **kwargs,
            )

            return {
                "success": True,
                "tool": tool_name,
                "result": result,
            }

        except Exception as exc:
            return {
                "success": False,
                "tool": tool_name,
                "error": str(exc),
            }

    async def calculate(
        self,
        expression: str,
    ) -> Dict[str, Any]:
        """
        Convenience wrapper for the calculator.
        """

        return await self.execute(
            "calculator",
            expression=expression,
        )

    async def symbolic(
        self,
        operation: str,
        expression: str,
        variable: str = "x",
    ) -> Dict[str, Any]:
        """
        Convenience wrapper for the SymPy tool.
        """

        return await self.execute(
            "sympy",
            operation=operation,
            expression=expression,
            variable=variable,
        )


tool_executor = ToolExecutor()