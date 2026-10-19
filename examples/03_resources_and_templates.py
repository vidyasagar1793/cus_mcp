"""Example 03: Resources and Prompt Templates

Resources allow LLMs to read contextual documents or live data via URI schemes (like memo:// or file://).
Prompts allow LLMs or clients to invoke reusable prompt templates with parameters.
"""

try:
    from mcp.server.mcpserver import MCPServer as FastMCP
except (ImportError, ModuleNotFoundError):
    from mcp.server.fastmcp import FastMCP  # type: ignore

mcp = FastMCP("ResourcesAndPromptsServer")

# Internal mock data
DOCUMENTS = {
    "guide": "# Guide\nAlways handle errors gracefully in MCP tools.",
    "changelog": "# Changelog\n- v0.1: Initial release with FastMCP.",
}


# 1. Static Resource (fixed URI)
@mcp.resource("config://app-settings")
def get_app_settings() -> str:
    """Provides application configuration settings as a resource."""
    return "environment=development\nversion=0.1.0\ndebug=true"


# 2. Dynamic Resource with URI template parameter
@mcp.resource("docs://{doc_id}")
def get_document(doc_id: str) -> str:
    """Reads a document by its ID (URI template).

    Args:
        doc_id: Identifier of the document to fetch (e.g. 'guide' or 'changelog').
    """
    return DOCUMENTS.get(doc_id, f"Document '{doc_id}' was not found.")


# 3. Prompt Template
@mcp.prompt()
def bug_report_prompt(error_message: str, stack_trace: str = "") -> str:
    """Generates a structured prompt to analyze a software error or exception.

    Args:
        error_message: The error message observed.
        stack_trace: Optional traceback or stack trace text.
    """
    prompt = f"Analyze the following software error and explain the root cause:\nError: {error_message}"
    if stack_trace:
        prompt += f"\n\nStack Trace:\n```\n{stack_trace}\n```"
    prompt += "\n\nProvide step-by-step remediation suggestions."
    return prompt


if __name__ == "__main__":
    mcp.run()
