import asyncio
import pytest
from contextlib import AsyncExitStack
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


SERVER_PATH = r"C:\Users\DELL\Documents\AeroLeadPrj\mcpTools\server.py"
EXPECTED_TOOLS = [
    "add_numbers",
    "prompt_blogs"
]

print(SERVER_PATH)
@pytest.mark.asyncio
async def test_mcp_server_connection():
    """Connect to an MCP server and verify the tools"""

    exit_stack = AsyncExitStack()

    server_params = StdioServerParameters(
        command="python", args=[SERVER_PATH], env=None
    )

    stdio_transport = await exit_stack.enter_async_context(
        stdio_client(server_params)
    )
    stdio, write = stdio_transport

    print("step1:",stdio,write)
    session = await exit_stack.enter_async_context(
        ClientSession(stdio, write)
    )

    print(f"session is:{session}")
    await session.initialize()

    response = await session.list_tools()
    tools = response.tools
    tool_names = [tool.name for tool in tools]
    tool_descriptions = [tool.description for tool in tools]

    print("response is:{tools},{tool_names},{tool_descriptions}")
    print("\nYour server has the following tools:")
    for tool_name, tool_description in zip(tool_names, tool_descriptions):
        print(f"{tool_name}: {tool_description}")

    assert sorted(EXPECTED_TOOLS) == sorted(tool_names)

    await exit_stack.aclose()
