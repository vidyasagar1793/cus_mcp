"""System and structured tools demonstration for custom MCP server.

Shows:
1. Using Pydantic models for complex tool inputs
2. Structured JSON response formats
3. Safe stderr logging without breaking stdio protocol
"""

import sys
import logging
import platform
import os
from pydantic import BaseModel, Field
from custom_mcp_server.compat import FastMCP

logger = logging.getLogger("custom_mcp_server.tools.system")


class EchoRequest(BaseModel):
    """Pydantic model representing structured input for an echo tool."""

    message: str = Field(description="The message text to echo back")
    uppercase: bool = Field(default=False, description="Convert message to uppercase")
    repeat: int = Field(default=1, ge=1, le=10, description="Times to repeat the message (1-10)")


def get_system_info() -> dict[str, str]:
    """Get operating system, Python runtime, and host information.

    Returns:
        Dictionary containing OS name, architecture, Python version, and working directory.
    """
    logger.info("Handling get_system_info request")
    return {
        "os_name": platform.system(),
        "os_release": platform.release(),
        "architecture": platform.machine(),
        "python_version": platform.python_version(),
        "cwd": os.getcwd(),
    }


def echo_message(payload: EchoRequest) -> dict[str, str]:
    """Echo a message with formatting options using a Pydantic schema.

    Args:
        payload: Structured request with message, uppercase flag, and repetition count.

    Returns:
        Dictionary with original and transformed message.
    """
    text = payload.message.upper() if payload.uppercase else payload.message
    repeated_text = " ".join([text] * payload.repeat)

    return {
        "original": payload.message,
        "processed": repeated_text,
        "repeat_count": str(payload.repeat),
    }


def register_system_tools(mcp: FastMCP) -> None:
    """Register system and structured tools on FastMCP instance."""
    mcp.tool()(get_system_info)
    mcp.tool()(echo_message)
