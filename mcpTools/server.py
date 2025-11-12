
from mcp.server.fastmcp import FastMCP
import sys, os
sys.path.append(r"C:\Users\DELL\Documents\AeroLeadPrj")

from call.aeroCall import toolCall
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

@mcp.tool()
async def call_number(custPhoneNum:str, userPhoneNum:str)->str:
    """
    This async function takes two phone numbers as input and calls the customer number from the user's
    phone number.
    
    :param costPhoneNum: It looks like there is a typo in the function parameters. The function
    definition mentions `costPhoneNum` but the function body uses `custPhoneNum`. You may want to
    correct this inconsistency for the function to work correctly
    :type costPhoneNum: int
    :param userphoneNum: The `userphoneNum` parameter is the phone number of the user who wants to make
    the call. It is an integer value representing the phone number
    :type userphoneNum: int
    :return: the result of calling the `toolCall` function with the provided `custPhoneNum` and
    `userPhoneNum` parameters. If either `custPhoneNum` or `userPhoneNum` is `None`, it will return the
    message "Both number are required."
    """
    
    
    if custPhoneNum is None or userPhoneNum is None:
        return "Both number are required."
    return toolCall(custPhoneNum, userPhoneNum)

# @mcp.tool()
# asunc def linkedindata(link:str)->str:
#     """user provide linkedin link you hace to find the data for this link"""
    
#     if link is None:
#         return "vaild link is require"
    # return linkeddata(link)
if __name__ == "__main__":
    mcp.run(transport="stdio")

