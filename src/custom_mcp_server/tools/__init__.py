"""Tools package for custom MCP server.
"""

from .math_tools import register_math_tools
from .system_tools import register_system_tools

__all__ = ["register_math_tools", "register_system_tools"]
