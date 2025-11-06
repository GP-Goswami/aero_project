import asyncio
from mcp.server.fastmcp import FastMCP
import pytest
from contextlib import AsyncExitStack
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
mcp = FastMCP("Aero_Ai_Agent")

@mcp.tool()
async def prompt_blogs(userPrompt:str)->str:
    """Generate a blog article based on a user-provided topic or outline."""

    prompt = f"""
Start with an engaging introduction: Hook your reader immediately to encourage them to continue reading.
Expand on main points: Dedicate sections of your blog to each main idea from your outline.
Use clear and concise language: Avoid jargon and get straight to the point to ensure your message is easy to understand.
Add value and evidence: Back up your points with examples, data, or personal stories to make your content more engaging and credible.

Now, you have to write a blog according to this: {userPrompt}
"""


    if not userPrompt:
        return "Customer not found"

    return prompt


@mcp.tool()
async def add_numbers(num1: int, num2: int) -> str:
    """Add two numbers and return the result as a string."""

    if num1 is None or num2 is None:
        return "Both numbers are required."
    add = num1 + num2
    return f"The sum of {num1} and {num2} is {add}"

if __name__ == "__main__":
    mcp.run(transport="stdio")

