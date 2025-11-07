from openai import OpenAI
import os

REMOTE_MCP_URL = os.environ["REMOTE_MCP_URL"]

client = OpenAI()  # needs OPENAI_API_KEY


def ask_study_summary(study_id: str):
    user_prompt = f"Can you give me the summary of study {study_id}?"

    # 1) first call: model + MCP tool gets listed
    first = client.responses.create(
        model="gpt-5-nano",
        input=user_prompt,
        tools=[
            {
                "type": "mcp",
                "server_label": "studydb",
                "server_url": REMOTE_MCP_URL,
                "allowed_tools": ["get_study_summary"],
                "require_approval": "never",
            }
        ],
    )

    # 2) second call: reuse previous_response_id so the model can now call the tool
    second = client.responses.create(
        model="gpt-5-nano",
        input=user_prompt,
        previous_response_id=first.id,
    )

    # extract text from the second response
    texts: list[str] = []
    for block in second.output:
        # each block can have content
        content = getattr(block, "content", None)
        if not content:
            continue
        for part in content:
            if part.type == "output_text":
                texts.append(part.text)

    return "\n".join(texts) if texts else "(no text output found)"


def main():
    summary = ask_study_summary("ST000001")
    print(summary)


if __name__ == "__main__":
    main()
