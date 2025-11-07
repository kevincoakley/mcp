from google import genai
from google.genai import types
from fastmcp import Client
import asyncio
import os

# Set your remote MCP server URL
REMOTE_MCP_URL = os.environ["REMOTE_MCP_URL"]


async def ask_study_summary(study_id: str):

    # Initialize the MCP client
    mcp_client = Client(REMOTE_MCP_URL)

    # Use 'async with' to manage the MCP client connection
    async with mcp_client:
        # Initialize the Gemini Client
        aclient = genai.Client().aio

        # Configure tool calling
        tool_config = types.ToolConfig(
            function_calling_config=types.FunctionCallingConfig(
                mode="auto"  # "auto" lets the model choose text or tool
            )
        )

        # Define the full configuration for the request
        content_config = types.GenerateContentConfig(
            tools=[mcp_client.session], tool_config=tool_config
        )

        user_prompt = f"Can you give me the summary of study {study_id}?"

        chat_history = [
            types.Content(parts=[types.Part(text=user_prompt)], role="user")
        ]

        try:
            # --- Start the conversation loop ---
            while True:
                # Generate content from the model
                response = await aclient.models.generate_content(
                    model="gemini-2.0-flash-001",
                    contents=chat_history,
                    config=content_config,
                )

                response_part = response.parts[0]

                if response_part.function_call:
                    # Add the model's call to history
                    chat_history.append(
                        types.Content(parts=[response_part], role="model")
                    )

                    function_call = response_part.function_call
                    func_name = function_call.name
                    func_args = dict(function_call.args)

                    try:
                        # Call the tool
                        tool_result_response = await mcp_client.session.call_tool(
                            name=func_name, arguments=func_args
                        )
                        # Access the result
                        tool_result = tool_result_response.structuredContent

                    except Exception as e:
                        print(f"Error calling MCP tool '{func_name}': {e}")
                        raise

                    # Package the tool's result for Gemini
                    function_response_part = types.FunctionResponse(
                        name=func_name, response={"content": tool_result}
                    )

                    # Add the tool's response to history
                    chat_history.append(
                        types.Content(
                            parts=[
                                types.Part(function_response=function_response_part)
                            ],
                            role="function",
                        )
                    )
                    # Loop continues...

                elif response_part.text:
                    # Model's response is text, we are done!
                    return response_part.text
                    break  # Exit the loop

                else:
                    # No text, no function call
                    print("\nError: Model returned an empty response.")
                    break  # Exit the loop

            # --- End of 'while' loop ---

        except Exception as e:
            print(f"\nAn error occurred during generation: {e}")


# Run the asynchronous function
if __name__ == "__main__":
    try:
        summary = asyncio.run(ask_study_summary("ST000001"))
        print(summary)
    except Exception as e:
        print(f"\nAn error occurred: {e}")
