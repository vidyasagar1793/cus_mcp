"""Prompt templates demonstration for custom MCP server.

Shows:
1. Registering reusable prompts that clients can inspect and populate
2. Defining prompt parameters with default values
3. Generating structured context for LLM conversations
"""

from custom_mcp_server.compat import FastMCP


def register_prompt_templates(mcp: FastMCP) -> None:
    """Register prompt templates on the FastMCP instance."""

    @mcp.prompt()
    def code_review(code: str, language: str = "python") -> str:
        """A prompt template for requesting a comprehensive code review.

        Args:
            code: The source code to review.
            language: The programming language (default: 'python').
        """
        return (
            f"You are a principal software engineer. Please review the following {language} code:\n\n"
            f"```{language}\n{code}\n```\n\n"
            "Evaluate:\n"
            "1. Potential bugs or edge cases\n"
            "2. Readability, naming, and style\n"
            "3. Performance or security considerations\n"
            "4. Suggested improvements with concise examples"
        )

    @mcp.prompt()
    def explain_concept(concept: str, target_audience: str = "beginner") -> str:
        """A prompt template for explaining technical concepts.

        Args:
            concept: The concept to explain (e.g., 'Model Context Protocol').
            target_audience: 'beginner', 'intermediate', or 'expert'.
        """
        return (
            f"Please explain the concept of '{concept}' tailored for a {target_audience} audience.\n"
            "Use clear analogies, mention why it matters, and provide a concrete example."
        )
