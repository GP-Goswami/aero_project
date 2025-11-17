"""define all the tools in mcp servers"""


import sys
import json
from mcp.server.fastmcp import FastMCP
sys.path.append(r"C:\Users\DELL\Documents\AeroLeadPrj")
from call.aeroCall import toolCall

mcp = FastMCP("Aero_Ai_Agent")


@mcp.tool()
async def prompt_blogs(userPrompt: str) -> str:
    """Generate a blog article based on a user-provided topic or outline."""

#     prompt = f"""
#     You are a professional blog writer, and you know the best practices
#     for blog formatting—clear structure, scannability, visuals,
#     reader value, and strong CTA.

# Write a blog post on the topic: “{userPrompt}”.

# **Follow this format:**
# 1. A **strong title**, 6-13 words long, that grabs attention and clearly
#     states what the post is about.
# 2. A compelling **introduction** that hooks the reader immediately
#     and promises value.
# 3. A **table of contents** (list of sections) right after the introduction,
#     so the reader knows what to expect.
# 4. Sections with **clear headings** (H2/H3) for each main point.
#     Use bullet points or numbered lists to make lists skimmable.
#     Keep paragraphs short (3-4 sentences max).
# 5. Incorporate **bold** or *italics* to highlight key ideas, but sparingly.
# 6. Include at least **2-3 visuals**: describe where images or infographics
#     should appear (e.g., “Insert infographic here showing trend over time”)
#     and include alt-text for them.
# 7. Use **relevant links** (internal/external) to deepen the reader’s
#     understanding.
# 8. Make the text **skimmable**: use sub-headers, bullet lists, and white space.
# 9. End with a **strong call to action (CTA)**: what should the reader do next?
#     (Subscribe, comment, explore a product, etc.)
# 10. Ensure the tone is friendly but professional, easy to understand
#     (no jargon) and packed with new insights, not just re-hashed content.

# **Important**: While following the format above, bring fresh value—new
#     examples, recent data, your own viewpoint. Don’t simply repeat generic
#     ideas.
# Write the full blog post including title, intro, table of contents, all
#     sections, visuals placeholder, links, and CTA.

# Topic: {userPrompt} 
# Convert the following blog into a well-structured Markdown blog 
#     """
    prompt:f"write 2 line blog on {userPromt}"

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
async def call_number(custPhoneNum: str, userPhoneNum: str, msg: str) -> str:
    """
    This async function takes two phone numbers as input and calls
    the customer number from the user's
    phone number.

    :param costPhoneNum: It looks like there is a typo in the function
    parameters. The function definition mentions `costPhoneNum` but the
    function body uses `custPhoneNum`. You may want to
    correct this inconsistency for the function to work correctly
    :type costPhoneNum: int
    :param userphoneNum: The `userphoneNum` parameter is the phone number
        of the user who wants to make
    the call. It is an integer value representing the phone number
    :type userphoneNum: int
    :return: the result of calling the `toolCall` function with the provided
    `custPhoneNum` and
    `userPhoneNum` parameters. If either `custPhoneNum` or `userPhoneNum` is
    `None`, it will return the message "Both number are required."
    """

    if custPhoneNum is None and userPhoneNum is None and msg is None:
        return "All the fields are required."
    callans= toolCall(custPhoneNum, msg, userPhoneNum)
    # print("ans---->",callans)
    return json.dumps(callans)

# @mcp.tool()
# asunc def linkedindata(link:str)->str:
#     """user provide linkedin link you hace to find the data for this link"""

#     if link is None:
#         return "vaild link is require"
    # return linkeddata(link)
if __name__ == "__main__":
    mcp.run(transport="stdio")
