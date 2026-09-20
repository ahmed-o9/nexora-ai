from typing import Any


class SymPyTool:
    """Symbolic mathematics tool with graceful fallback."""

    name = "sympy"

    async def execute(self, expression: str, operation: str = "simplify"):
        if not expression or not expression.strip():
            raise ValueError("Expression cannot be empty.")

        try:
            import sympy as sp
        except ImportError:
            return {
                "success": False,
                "error": "SymPy is not installed.",
                "hint": "Run: pip install sympy",
            }

        try:
            expr = sp.sympify(expression)

            if operation == "simplify":
                result = sp.simplify(expr)

            elif operation == "expand":
                result = sp.expand(expr)

            elif operation == "factor":
                result = sp.factor(expr)

            elif operation == "diff":
                result = sp.diff(expr)

            elif operation == "integrate":
                result = sp.integrate(expr)

            else:
                raise ValueError(
                    f"Unsupported operation: {operation}"
                )

            return {
                "success": True,
                "operation": operation,
                "input": expression,
                "result": str(result),
            }

        except Exception as exc:
            return {
                "success": False,
                "operation": operation,
                "input": expression,
                "error": str(exc),
            }