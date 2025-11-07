import anthropic
import os

REMOTE_MCP_URL = os.environ["REMOTE_MCP_URL"]

client = anthropic.Anthropic()  # needs ANTHROPIC_API_KEY environment variable


def ask_study_summary(study_id: str):
    user_prompt = f"Can you give me the summary of study {study_id}?"

    # Claude API call with MCP server configuration
    response = client.beta.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=1000,
        messages=[{"role": "user", "content": user_prompt}],
        betas=["mcp-client-2025-04-04"],
        mcp_servers=[
            {
                "type": "url",
                "url": REMOTE_MCP_URL,
                "name": "mwb-mcp-server",
                "tool_configuration": {
                    "enabled": True,
                    "allowed_tools": ["get_study_summary"],
                },
            }
        ],
    )

    # Extract text from the response
    texts: list[str] = []
    for block in response.content:
        if block.type == "text":
            texts.append(block.text)

    return "\n".join(texts) if texts else "(no text output found)"


def main():
    summary = ask_study_summary("ST000001")
    print(summary)


if __name__ == "__main__":
    main()
