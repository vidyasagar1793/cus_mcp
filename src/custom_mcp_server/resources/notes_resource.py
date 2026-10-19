"""Resources demonstration for custom MCP server.

Shows:
1. Static resources (fixed URI)
2. Dynamic resources (URI template with parameters, e.g. memo://notes/{title})
3. Providing read-only documents and data directly to the LLM
"""

from typing import Dict
from custom_mcp_server.compat import FastMCP

# In-memory store for demonstration notes
SAMPLE_NOTES: Dict[str, str] = {
    "welcome": "Welcome to your custom Python Model Context Protocol (MCP) server!",
    "architecture": (
        "MCP Primitives:\n"
        "1. Tools: Functions invoked by LLMs to take action or calculate data.\n"
        "2. Resources: Data/documents read by LLMs as context (URI scheme).\n"
        "3. Prompts: Pre-defined prompt templates to guide user-LLM conversations."
    ),
    "stdio-rules": (
        "CRITICAL RULE FOR STDIO MCP SERVERS:\n"
        "Never use `print()` or write raw text to sys.stdout.\n"
        "stdout is reserved exclusively for JSON-RPC messages.\n"
        "Use `logging` or `sys.stderr.write()` for debug messages."
    ),
}


def register_notes_resource(mcp: FastMCP) -> None:
    """Register note resources on the FastMCP instance."""

    @mcp.resource("memo://quickstart")
    def get_quickstart_guide() -> str:
        """A static resource providing a quickstart overview for this MCP server."""
        return (
            "# Quickstart Guide\n\n"
            "This MCP server provides:\n"
            "- Tools: calculate, compute_statistics, get_system_info, echo_message\n"
            "- Resources: memo://quickstart, memo://notes/{title}\n"
            "- Prompts: code_review, summarize_notes\n"
        )

    @mcp.resource("memo://notes/{title}")
    def get_note_by_title(title: str) -> str:
        """A dynamic resource that retrieves a note by its title slug.

        Args:
            title: The slug or key of the note (e.g., 'welcome', 'architecture', 'stdio-rules').
        """
        key = title.lower().strip()
        if key in SAMPLE_NOTES:
            return SAMPLE_NOTES[key]

        available = ", ".join(SAMPLE_NOTES.keys())
        return f"Note '{title}' not found. Available notes: {available}"
