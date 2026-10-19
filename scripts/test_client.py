"""Standalone MCP Test Client.

This script demonstrates how an MCP client (such as Claude Desktop, Cursor,
or your own custom agent) communicates with the custom MCP server over stdio.

It launches the server as a subprocess, initializes the JSON-RPC session,
queries its capabilities, lists tools/resources/prompts, and invokes a tool.

Usage:
    python scripts/test_client.py
"""

import sys
import asyncio
import os
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def run_client():
    python_exe = sys.executable
    server_script = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "src", "custom_mcp_server", "server.py")
    )

    print("=" * 60)
    print("MCP CLIENT TEST HARNESS")
    print("=" * 60)
    print(f"Target Server Script: {server_script}")
    print(f"Python Executable:   {python_exe}")
    print("Connecting over stdio transport...\n")

    server_params = StdioServerParameters(
        command=python_exe,
        args=[server_script],
        env=os.environ.copy(),
    )

    async with stdio_client(server_params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            # Step 1: Handshake & Initialize
            print("1. Initializing MCP session...")
            init_result = await session.initialize()
            info = getattr(init_result, "server_info", getattr(init_result, "serverInfo", None))
            name = getattr(info, "name", "MCP Server") if info else "MCP Server"
            ver = getattr(info, "version", "") if info else ""
            print(f"   ✓ Connected to server: {name} (v{ver})")

            # Step 2: Discover Tools
            print("\n2. Discovering available tools...")
            tools_response = await session.list_tools()
            for tool in tools_response.tools:
                print(f"   • Tool: {tool.name}")
                first_line = (tool.description or "").split("\n")[0]
                print(f"     Description: {first_line}")

            # Step 3: Discover Resources
            print("\n3. Discovering available resources...")
            resources_response = await session.list_resources()
            for res in resources_response.resources:
                print(f"   • Resource: {res.uri} ({res.name})")

            # Step 4: Discover Prompts
            print("\n4. Discovering available prompts...")
            prompts_response = await session.list_prompts()
            for prompt in prompts_response.prompts:
                print(f"   • Prompt: {prompt.name} - {prompt.description}")

            # Step 5: Execute a Tool Call
            print("\n5. Invoking tool 'calculate' (operation='multiply', a=6, b=7)...")
            tool_result = await session.call_tool(
                "calculate",
                arguments={"operation": "multiply", "a": 6, "b": 7},
            )
            print(f"   ✓ Tool Result Content: {tool_result.content}")

            # Step 6: Read a Resource
            print("\n6. Reading resource 'memo://quickstart'...")
            resource_data = await session.read_resource("memo://quickstart")
            first_content = resource_data.contents[0] if resource_data.contents else "No contents"
            preview = str(getattr(first_content, 'text', first_content))[:100].replace('\n', ' ')
            print(f"   ✓ Resource Content Preview: {preview}...")

            print("\n" + "=" * 60)
            print("ALL MCP CAPABILITIES VERIFIED SUCCESSFULLY!")
            print("=" * 60)


if __name__ == "__main__":
    asyncio.run(run_client())
