"""this file is user for create backend api or client side calling for the tools"""


# import asyncio
# import pytest
# from contextlib import AsyncExitStack
# from mcp import ClientSession, StdioServerParameters
# from mcp.client.stdio import stdio_client
# from google import genai
# import os
# from dotenv import load_dotenv,find_dotenv
# from fastapi import FastAPI

# dotenv_path=find_dotenv()
# load_dotenv(dotenv_path)

# client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
# SERVER_PATH = r"C:\Users\DELL\Documents\AeroLeadPrj\mcpTools\server.py"
# EXPECTED_TOOLS = [
#     "add_numbers",
#     "prompt_blogs",
#     "call_number"
# ]

# userInput=input("enter your question:- ")
# prompt=f"you are a aero ai assistant you have to do task as explain here
# {userInput}"

# @pytest.mark.asyncio
# async def test_mcp_server_connection():
#     """Connect to an MCP server and verify the tools"""

#     exit_stack = AsyncExitStack()

#     server_params = StdioServerParameters(
#         command="python", args=[SERVER_PATH], env=None
#     )

#     stdio_transport = await exit_stack.enter_async_context(
#         stdio_client(server_params)
#     )
#     stdio, write = stdio_transport

#     session = await exit_stack.enter_async_context(
#         ClientSession(stdio, write)
#     )

#     print("session is: ")
#     await session.initialize()

#     response = await session.list_tools()
#     tools = response.tools
#     responses = client.models.generate_content(
#                 model="gemini-2.0-flash",
#                 contents=[
#                         {
#                             "role": "user",
#                             "parts": [
#                                 {
#                                     "text": prompt
#                                 }
#                             ]
#                         }
#                     ],
#                 config=genai.types.GenerateContentConfig(
#                     temperature=0,
#                     tools=tools,
#                 ),
#             )
#     # print("response is: ",responses.candidates[0].content)

#     if responses.candidates[0].content.parts[0].function_call:
#         functionCall = responses.candidates[0].content.parts[0].function_call
#         tool_name = functionCall.name
#         arguments = functionCall.args  # <-- this contains num1, num2, etc

#         print("🔧 Gemini selected tool:", tool_name)
#         print("📌 With arguments:", arguments)

#         # --- Call the MCP Tool ---
#         tool_result = await session.call_tool(
#             tool_name,
#             arguments
#         )

#         print("🛠️ Tool result:", tool_result)

#         # --- Send the tool result back to Gemini so it can finish reasoning
#         final_response = client.models.generate_content(
#             model="gemini-2.0-flash",
#             contents=[
#                 prompt,
#                 {
#                     "toolResult": {
#                         "name": tool_name,
#                         "result": tool_result
#                     }
#                 }
#             ],
#         )

#         print("🤖 Final Gemini response:",
#           final_response.candidates[0].content.text)
#     else:
#         print("response is: ",responses.candidates[0].content.parts[0].text)
#     # tool_names = [tool.name for tool in tools]
#     # tool_descriptions = [tool.description for tool in tools]

#     # print("response is:{tools},{tool_names},{tool_descriptions}")
#     # print("\nYour server has the following tools:")
#     # for tool_name, tool_description in zip(tool_names, tool_descriptions):
#     #     print(f"{tool_name}: {tool_description}")

#     # assert sorted(EXPECTED_TOOLS) == sorted(tool_names)

#     await exit_stack.aclose()

# -------------------------------
import os
import sys
import asyncio
import json
from contextlib import AsyncExitStack, asynccontextmanager
from pydantic import BaseModel
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from google import genai
from dotenv import load_dotenv, find_dotenv
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException
import traceback
from fastapi import Request

sys.path.append(r"C:\Users\DELL\Documents\AeroLeadPrj")
from call.aeroCall import toolCall


# Load environment variables
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)


client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
SERVER_PATH = r"C:\Users\DELL\Documents\AeroLeadPrj\mcpTools\server.py"

app = FastAPI(title="AeroLead MCP Tools")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for testing, allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Input model for frontend
class UserPrompt(BaseModel):
    """class for gemini model"""
    prompt: str | None = None
    custPhoneNum: str | None = None
    userPhoneNum: str | None = None


@app.post("/ask-gemini")
async def ask_gemini(data: UserPrompt):
    # """ Endpoint to take user input, send to Gemini, call MCP tool,
    #     and return result
    #     """
    async with AsyncExitStack() as exit_stack:
        try:
            if data.prompt:
                user_prompt = data.prompt
            elif data.custPhoneNum and data.userPhoneNum:
                user_prompt = f"""Call customer {data.custPhoneNum}
                    from user {data.userPhoneNum}."""
            else:
                raise HTTPException(status_code=400, detail="""Provide either
                                    prompt or both phone numbers.""")

            # Step 1: Connect to MCP Server
            # exit_stack = AsyncExitStack()
            server_params = StdioServerParameters(
                command="python", args=[SERVER_PATH], env=None
            )

            stdio_transport = await exit_stack.enter_async_context(stdio_client(server_params))
            stdio, write = stdio_transport
            session = await exit_stack.enter_async_context(ClientSession(stdio, write))
            await session.initialize()

            # Step 2: Get tools from MCP
            response = await session.list_tools()
            tools = response.tools
            print("tools")
            # Step 3: Ask Gemini what to do
            gemini_response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=[
                    {
                        "role": "user",
                        "parts": [{"text": f"You are Aero AI. Task:{user_prompt}"}]
                    }
                ],
                config=genai.types.GenerateContentConfig(
                    temperature=0,
                    tools=tools,
                ),
            )

            part = gemini_response.candidates[0].content.parts[0]

            # Step 4: Handle tool call
            if hasattr(part, "function_call") and part.function_call:
                function_call = part.function_call
                tool_name = function_call.name
                arguments = function_call.args

                print("Gemini selected tool:", tool_name)

                tool_result = await session.call_tool(tool_name, arguments)
                # print("ans----->", tool_result)
                mcp_data = tool_result.structuredContent
                # print(mcp_data, type(mcp_data))
                # print("step 5", tool_result.structuredContent)

                # Step 5: Let Gemini finish reasoning
                if tool_name == "prompt_blogs":

                    final_response = client.models.generate_content(
                        model="gemini-2.0-flash",
                        contents=[
                            {
                                "role": "model",
                                "parts": [
                                    {
                                        "function_response": {
                                            "name": tool_name,
                                            "response": mcp_data,
                                        }

                                    }
                                ]
                            }
                        ],
                    )

                    print("step6", final_response.candidates[0].content)
                    await exit_stack.aclose()
                    return {
                        "tool": "prompt_blogs",
                        "result": final_response.candidates[0].content.parts[0].text,
                    }

                # print("tool result is--->", tool_result)
                tool_output = tool_result.structuredContent  # This is a JSON string
                print("tooloutput",tool_output)
                
                # parsed = json.loads(tool_output)
                # print("parse",tool_output.result.status_code)
                # call_status = tool_output.result
                # print("CALL STATUS:", call_status)
                await exit_stack.aclose()
                return {
                    "tool": tool_name,
                    "result": tool_output ,
                }

            # Step 6: If Gemini didn’t call a tool, just return its message
            print("ggem ans is--->",part)
            await exit_stack.aclose()
            return {"response": part.text}
        except Exception as e:
            return {
                "error": str(e),
                "trace": traceback.format_exc()
            }


class CallRequest(BaseModel):
    """api for calling without gemini"""
    custPhoneNum: str
    msg: str
    userPhoneNum: str


@app.post("/calltool")
def call(data: CallRequest):
    """api calling"""
    call_tool = toolCall(data.custPhoneNum, data.msg, data.userPhoneNum)
    return call_tool


@app.get("/")
def nor():
    print("hii")
    return "welcome to aeroworld"

@app.post("/call-status")
async def call_status(request: Request):
    data = await request.form()

    call_sid = data.get("CallSid")
    call_status = data.get("CallStatus")

    print("CALL SID:", call_sid)
    print("STATUS:", call_status)

    return {"received": True}
# ngrok config add-authtoken 35bcal5nbZeMAPCaSyH3hNkedMK_4My4Mo2idaVZ59AWMu9Fi