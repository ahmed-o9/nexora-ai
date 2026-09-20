import ast
import math
import operator


class CalculatorTool:
    """Safe mathematical expression evaluator."""

    name = "calculator"

    _operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.Mod: operator.mod,
        ast.USub: operator.neg,
        ast.UAdd: operator.pos,
    }

    _functions = {
        "sqrt": math.sqrt,
        "sin": math.sin,
        "cos": math.cos,
        "tan": math.tan,
        "log": math.log,
        "log10": math.log10,
        "exp": math.exp,
        "abs": abs,
        "floor": math.floor,
        "ceil": math.ceil,
    }

    async def execute(self, expression: str):
        if not expression or not expression.strip():
            raise ValueError("Expression cannot be empty.")

        try:
            tree = ast.parse(expression.strip(), mode="eval")
            result = self._evaluate(tree.body)

            if isinstance(result, complex):
                raise ValueError("Complex results are not supported.")

            return {
                "expression": expression,
                "result": result,
            }

        except (SyntaxError, ValueError, TypeError, ZeroDivisionError) as exc:
            raise ValueError(f"Invalid mathematical expression: {exc}") from exc

    def _evaluate(self, node):
        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)) and not isinstance(
                node.value, bool
            ):
                return node.value
            raise ValueError("Only numeric constants are allowed.")

        if isinstance(node, ast.BinOp):
            operation = self._operators.get(type(node.op))
            if operation is None:
                raise ValueError("Unsupported operator.")

            left = self._evaluate(node.left)
            right = self._evaluate(node.right)
            return operation(left, right)

        if isinstance(node, ast.UnaryOp):
            operation = self._operators.get(type(node.op))
            if operation is None:
                raise ValueError("Unsupported unary operator.")
            return operation(self._evaluate(node.operand))

        if isinstance(node, ast.Call):
            if not isinstance(node.func, ast.Name):
                raise ValueError("Unsupported function.")

            function = self._functions.get(node.func.id)
            if function is None:
                raise ValueError(f"Unsupported function: {node.func.id}")

            if node.keywords:
                raise ValueError("Keyword arguments are not supported.")

            arguments = [self._evaluate(arg) for arg in node.args]
            return function(*arguments)

        if isinstance(node, ast.Name):
            constants = {
                "pi": math.pi,
                "e": math.e,
            }

            if node.id in constants:
                return constants[node.id]

            raise ValueError(f"Unknown constant: {node.id}")

        raise ValueError("Unsupported expression.")