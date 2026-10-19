"""Math tools demonstration for custom MCP server.

Shows:
1. Type annotations (int, float, list)
2. Docstrings (used by LLMs to understand the tool's purpose and arguments)
3. Return types and validation
"""

from typing import Union
from custom_mcp_server.compat import FastMCP


def calculate(operation: str, a: float, b: float) -> Union[float, str]:
    """Perform a basic arithmetic operation.

    Args:
        operation: One of 'add', 'subtract', 'multiply', 'divide', 'power'
        a: The first number (operand)
        b: The second number (operand)

    Returns:
        The calculated numeric result or raises ValueError if invalid.
    """
    op = operation.lower().strip()
    if op == "add":
        return a + b
    elif op == "subtract":
        return a - b
    elif op == "multiply":
        return a * b
    elif op == "divide":
        if b == 0:
            raise ValueError("Division by zero is not allowed.")
        return a / b
    elif op in ("power", "pow"):
        return a**b
    else:
        raise ValueError(
            f"Unsupported operation: '{operation}'. "
            "Supported operations are: add, subtract, multiply, divide, power."
        )


def compute_statistics(numbers: list[float]) -> dict[str, float]:
    """Compute statistical summary for a list of numbers.

    Args:
        numbers: A non-empty list of float or integer values.

    Returns:
        Dictionary with count, sum, mean, min, and max.
    """
    if not numbers:
        raise ValueError("The 'numbers' list must not be empty.")

    count = len(numbers)
    total = sum(numbers)
    mean = total / count
    minimum = min(numbers)
    maximum = max(numbers)

    return {
        "count": float(count),
        "sum": round(total, 4),
        "mean": round(mean, 4),
        "min": minimum,
        "max": maximum,
    }


def register_math_tools(mcp: FastMCP) -> None:
    """Register mathematical tools on the given FastMCP instance."""
    mcp.tool()(calculate)
    mcp.tool()(compute_statistics)
