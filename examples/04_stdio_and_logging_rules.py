"""Example 04: The Golden Rule of stdio Transports & Logging

=============================================================================
CRITICAL LESSON FOR BUILDING CUSTOM MCP SERVERS OVER STDIO:
=============================================================================
When your MCP server communicates with a client (like Claude Desktop, Cursor,
or the MCP Inspector) via the "stdio" transport:

1. `sys.stdout` is EXCLUSIVELY RESERVED for JSON-RPC messages.
2. If you call `print("Hello debug")`, your text will be sent to stdout!
3. The MCP client will try to parse "Hello debug" as a JSON-RPC message,
   fail with a JSON parse error, and terminate or hang the connection.

SAFE PRACTICES:
- ALWAYS use Python's `logging` module directed to `sys.stderr`.
- OR write explicitly to `sys.stderr.write(...)`.
- FastMCP automatically handles JSON-RPC framing on stdout.
=============================================================================
"""

import sys
import logging

try:
    from mcp.server.mcpserver import MCPServer as FastMCP
except (ImportError, ModuleNotFoundError):
    from mcp.server.fastmcp import FastMCP  # type: ignore

# Safe: Configure logging to sys.stderr
logging.basicConfig(
    stream=sys.stderr,
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("LoggingDemo")

mcp = FastMCP("StdioLoggingDemo")


@mcp.tool()
def safe_logging_tool(action: str) -> dict[str, str]:
    """Demonstrates safe stderr logging inside a tool without corrupting stdio.

    Args:
        action: The action name to log and perform.
    """
    # SAFE: Sent to stderr (does NOT corrupt the client's JSON-RPC parser)
    logger.info("Executing safe_logging_tool with action='%s'", action)
    logger.debug("Additional debugging details sent to stderr")

    # DANGEROUS (DON'T DO THIS IN PRODUCTION MCP STDIO SERVERS):
    # print("I will break your client JSON-RPC stream!")

    return {
        "status": "completed",
        "action": action,
        "note": "Check stderr or server logs to see debugging output safely emitted.",
    }


if __name__ == "__main__":
    logger.info("Starting StdioLoggingDemo server...")
    mcp.run()
