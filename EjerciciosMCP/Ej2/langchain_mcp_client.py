import asyncio
import os

from langchain.agents import create_agent
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_ollama import ChatOllama


async def main() -> None:
    ollama_api_key = os.getenv("OLLAMA_API_KEY")
    if not ollama_api_key:
        raise ValueError("Set OLLAMA_API_KEY before running this script.")

    client = MultiServerMCPClient(
        {
            "chinook": {
                "transport": "stdio",
                "command": "python",
                "args": ["/app/chinook_mcp_server.py"],
                "env": {**os.environ},
            }
        }
    )

    tools = await client.get_tools()

    llm = ChatOllama(
        model="gpt-oss:20b-cloud",
        base_url="https://ollama.com",
        temperature=0.2,
        headers={"Authorization": f"Bearer {ollama_api_key}"},
    )

    agent = create_agent(llm, tools=tools)
    response = await agent.ainvoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": "Who is the customer that spent the most money? Give me the name",
                }
            ]
        }
    )
    print(response["messages"][-1].content)


if __name__ == "__main__":
    asyncio.run(main())
