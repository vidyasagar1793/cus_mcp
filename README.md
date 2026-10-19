# 🛠️ Custom Python MCP Server Starter & Learning Kit

A hands-on, progressive repository for learning and building custom **Model Context Protocol (MCP)** servers in Python using the official `mcp` SDK.

---

## 🚀 Quickstart (30 Seconds)

### 1. Requirements
- Python 3.10+ (Python 3.12 recommended)
- [`uv`](https://docs.astral.sh/uv/) (recommended) or standard `pip`

### 2. Environment Setup
```powershell
# Create virtual environment and install dependencies
uv venv
uv pip install -e ".[dev]"
```
*(Or if using standard pip: `python -m venv .venv` then `.\.venv\Scripts\pip install -e ".[dev]"`)*

### 3. Verify Everything Works
Run the included test client:
```powershell
uv run python scripts/test_client.py
```
You will see the client connect over stdio, list tools, call `calculate`, and read resources!

---

## 📂 Repository Structure

```
cus_mcp/
├── pyproject.toml              # Project dependencies, packaging & script entry points
├── LEARNING_GUIDE.md           # In-depth architectural concepts & developer guide
├── README.md                   # This overview
│
├── src/custom_mcp_server/      # Modular production-ready MCP server
│   ├── server.py               # Main server entry point & assembly
│   ├── compat.py               # SDK v1 (FastMCP) & v2 (MCPServer) compat layer
│   ├── tools/                  # Custom tools
│   │   ├── math_tools.py       # Functions with typed params, docstrings, validation
│   │   └── system_tools.py     # Pydantic input models & safe stderr logging
│   ├── resources/              # Custom resources
│   │   └── notes_resource.py   # Static & dynamic URI templates (memo://notes/{title})
│   └── prompts/                # Custom prompt templates
│       └── templates.py        # Reusable workflow prompt generators
│
├── examples/                   # Progressive standalone learning scripts
│   ├── 01_minimal_server.py    # 15-line "Hello World" MCP server
│   ├── 02_tools_and_types.py   # Pydantic schemas, types, and JSON schema generation
│   ├── 03_resources_and_templates.py # Resources vs Tools vs Prompts
│   └── 04_stdio_and_logging_rules.py # The stdio golden rule & safe logging
│
├── scripts/
│   └── test_client.py          # Automated Python client testing stdio JSON-RPC
│
├── tests/
│   └── test_server.py          # Pytest unit tests
│
└── client_configs/
    ├── claude_desktop_config.json # Claude Desktop configuration snippet
    └── cursor_mcp.json            # Cursor / VS Code configuration snippet
```

---

## 📚 Progressive Learning Examples

Start with the files in `examples/` to learn one concept at a time:

| Example | Concept | How to Run |
| :--- | :--- | :--- |
| `01_minimal_server.py` | Minimal 15-line server, `@mcp.tool()` decorator | `uv run python examples/01_minimal_server.py` |
| `02_tools_and_types.py` | Type annotations, Pydantic models, JSON schema | `uv run python examples/02_tools_and_types.py` |
| `03_resources_and_templates.py` | Static & dynamic URI resources, prompt templates | `uv run python examples/03_resources_and_templates.py` |
| `04_stdio_and_logging_rules.py` | Why `print()` breaks stdio, safe stderr logging | `uv run python examples/04_stdio_and_logging_rules.py` |

---

## 🧪 Testing & Debugging

### Run Unit Tests
```powershell
uv run pytest
```

### Run the In-Python Client Test Harness
```powershell
uv run python scripts/test_client.py
```

### Inspect with the Official Web UI (MCP Inspector)
Anthropic provides an interactive web inspector to test tools and see live JSON-RPC messages:
```powershell
npx @modelcontextprotocol/inspector uv run cus-mcp
```

---

## 🔌 Connecting to LLM Clients

### Claude Desktop
Add to `%APPDATA%\Claude\claude_desktop_config.json` (Windows):
```json
{
  "mcpServers": {
    "custom-learning-mcp": {
      "command": "uv",
      "args": [
        "--directory",
        "D:\\cus_mcp",
        "run",
        "cus-mcp"
      ]
    }
  }
}
```

### Cursor
Add to your Cursor MCP settings (`.cursor/mcp.json` or Global Settings):
```json
{
  "mcpServers": {
    "custom-learning-mcp": {
      "command": "uv",
      "args": [
        "--directory",
        "D:\\cus_mcp",
        "run",
        "cus-mcp"
      ]
    }
  }
}
```

---

## 📖 Deep Dive
For an in-depth conceptual breakdown, check out [LEARNING_GUIDE.md](file:///d:/cus_mcp/LEARNING_GUIDE.md).
