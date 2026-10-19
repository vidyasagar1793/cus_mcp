"""Tests for custom MCP server capabilities and tool handlers."""

import pytest
from custom_mcp_server.server import create_server
from custom_mcp_server.tools.math_tools import calculate, compute_statistics
from custom_mcp_server.tools.system_tools import get_system_info, echo_message, EchoRequest
from custom_mcp_server.resources.notes_resource import SAMPLE_NOTES


@pytest.fixture
def test_server():
    """Fixture providing a fresh configured MCP server."""
    return create_server()


def test_server_initialization(test_server):
    """Verify server instance is created with correct name."""
    assert test_server.name == "CustomLearningMCP"


def test_calculate_operations():
    """Verify arithmetic operations."""
    assert calculate("add", 10, 5) == 15
    assert calculate("subtract", 10, 5) == 5
    assert calculate("multiply", 10, 5) == 50
    assert calculate("divide", 10, 5) == 2.0
    assert calculate("power", 2, 3) == 8

    with pytest.raises(ValueError, match="Division by zero"):
        calculate("divide", 5, 0)

    with pytest.raises(ValueError, match="Unsupported operation"):
        calculate("modulo", 5, 2)


def test_compute_statistics():
    """Verify statistical summary computation."""
    data = [10.0, 20.0, 30.0]
    stats = compute_statistics(data)
    assert stats["count"] == 3.0
    assert stats["sum"] == 60.0
    assert stats["mean"] == 20.0
    assert stats["min"] == 10.0
    assert stats["max"] == 30.0

    with pytest.raises(ValueError, match="must not be empty"):
        compute_statistics([])


def test_system_info():
    """Verify system info returns valid operating environment data."""
    info = get_system_info()
    assert "os_name" in info
    assert "python_version" in info
    assert "cwd" in info


def test_echo_message():
    """Verify echo formatting and Pydantic validation."""
    req = EchoRequest(message="mcp", uppercase=True, repeat=3)
    result = echo_message(req)
    assert result["original"] == "mcp"
    assert result["processed"] == "MCP MCP MCP"

    # Verify invalid repeat raises ValidationError
    with pytest.raises(Exception):
        EchoRequest(message="test", repeat=0)


def test_sample_notes_resource():
    """Verify notes resources dictionary contains key documentation topics."""
    assert "welcome" in SAMPLE_NOTES
    assert "architecture" in SAMPLE_NOTES
    assert "stdio-rules" in SAMPLE_NOTES
    assert "stdout" in SAMPLE_NOTES["stdio-rules"]
