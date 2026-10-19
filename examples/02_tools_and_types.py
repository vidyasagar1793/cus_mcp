"""Example 02: Tools, Types, and Pydantic Schemas

This example demonstrates how FastMCP inspects Python type hints,
docstrings, and Pydantic models to automatically generate the JSON Schema
that LLMs use to decide when and how to call your tools.
"""

from typing import List, Optional
from pydantic import BaseModel, Field

try:
    from mcp.server.mcpserver import MCPServer as FastMCP
except (ImportError, ModuleNotFoundError):
    from mcp.server.fastmcp import FastMCP  # type: ignore

mcp = FastMCP("TypesAndSchemasServer")


# 1. Basic typed parameters with defaults and docstrings
@mcp.tool()
def search_database(
    query: str,
    limit: int = 5,
    case_sensitive: bool = False,
) -> dict[str, object]:
    """Search records in the database with filtering options.

    Args:
        query: The search keywords or term.
        limit: Maximum number of records to return (default: 5).
        case_sensitive: Whether matching should respect letter casing.
    """
    mock_db = [
        "Python MCP Server Guide",
        "FastMCP Quickstart Tutorial",
        "Anthropic Model Context Protocol Specification",
        "Pydantic Validation in Python",
        "Asynchronous Programming with Asyncio",
    ]

    results = []
    for item in mock_db:
        target = item if case_sensitive else item.lower()
        search_term = query if case_sensitive else query.lower()
        if search_term in target:
            results.append(item)
        if len(results) >= limit:
            break

    return {
        "query": query,
        "match_count": len(results),
        "results": results,
    }


# 2. Advanced: Using Pydantic models for nested / validated schemas
class UserProfile(BaseModel):
    username: str = Field(..., min_length=3, max_length=20, description="Unique username")
    email: str = Field(..., description="User email address")
    role: str = Field(default="viewer", description="Role: admin, editor, or viewer")
    tags: List[str] = Field(default_factory=list, description="Associated user tags")


@mcp.tool()
def register_user(profile: UserProfile) -> dict[str, str]:
    """Register a new user profile with validation.

    Args:
        profile: Validated user profile model containing username, email, role, and tags.
    """
    return {
        "status": "success",
        "message": f"User '{profile.username}' registered as '{profile.role}'.",
    }


if __name__ == "__main__":
    mcp.run()
