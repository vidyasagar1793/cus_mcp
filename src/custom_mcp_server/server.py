"""Main entry point for the Custom MCP Server.

This module initializes the FastMCP server, registers all tools,
resources, and prompts, and runs using stdio transport by default.
"""

import sys
import logging
from custom_mcp_server.compat import FastMCP

from custom_mcp_server.tools import register_math_tools, register_system_tools
from custom_mcp_server.resources import register_notes_resource
from custom_mcp_server.prompts import register_prompt_templates

# Configure logging to sys.stderr ONLY.
# stdout MUST remain pristine for JSON-RPC messages.
logging.basicConfig(
    stream=sys.stderr,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("custom_mcp_server")


def create_server() -> FastMCP:
    """Create and configure the FastMCP server instance."""
    mcp = FastMCP(
        name="CustomLearningMCP",
        instructions=(
            "Custom Learning MCP Server: provides calculation tools, system diagnostics, "
            "developer memo resources, and code review prompt templates."
        ),
    )

    # Register modular capabilities
    register_math_tools(mcp)
    register_system_tools(mcp)
    register_notes_resource(mcp)
    register_prompt_templates(mcp)

    logger.info("CustomLearningMCP initialized with all tools, resources, and prompts")
    return mcp


# Global server instance for direct imports or script execution
mcp_server = create_server()


def main() -> None:
    """Run the MCP server over standard I/O (stdio)."""
    logger.info("Starting CustomLearningMCP via stdio transport...")
    mcp_server.run(transport="stdio")


if __name__ == "__main__":
    main()
