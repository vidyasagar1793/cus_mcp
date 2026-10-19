"""Compatibility layer for MCP Python SDK v1 and v2.

Background:
In MCP Python SDK v1.x, the high-level decorator interface was called `FastMCP`
and imported from `mcp.server.fastmcp`.
In MCP Python SDK v2.x, it was officially renamed to `MCPServer` and located at
`mcp.server.mcpserver.MCPServer`.

This module provides a unified `FastMCP` and `MCPServer` export so your code
works seamlessly across both versions.
"""

try:
    from mcp.server.mcpserver import MCPServer
    FastMCP = MCPServer
except (ImportError, ModuleNotFoundError):
    from mcp.server.fastmcp import FastMCP  # type: ignore
    MCPServer = FastMCP  # type: ignore

__all__ = ["FastMCP", "MCPServer"]
