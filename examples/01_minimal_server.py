"""Example 01: Minimal MCP Server

This is the absolute simplest MCP server you can build in Python using FastMCP.
Run this directly with:
    python examples/01_minimal_server.py
or via uv:
    uv run python examples/01_minimal_server.py
"""

try:
    from mcp.server.mcpserver import MCPServer as FastMCP
except (ImportError, ModuleNotFoundError):
    from mcp.server.fastmcp import FastMCP  # type: ignore

# 1. Create a server instance with a friendly name
mcp = FastMCP("MinimalServer")


# 2. Register a tool using the @mcp.tool() decorator
@mcp.tool()
def greet(name: str = "World") -> str:
    """Return a friendly greeting to the specified person or entity.

    The docstring you write here becomes the tool description that the LLM sees!
    """
    return f"Hello, {name}! Welcome to the Model Context Protocol."


# 3. Run the server over stdio
if __name__ == "__main__":
    mcp.run()
