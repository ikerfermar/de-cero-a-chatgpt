import os

from mcp import StdioServerParameters
from smolagents import CodeAgent, LiteLLMModel, MCPClient


# This script connects to the MCP SQL server from Ej1 using stdio transport.
server_parameters = StdioServerParameters(
    command="python",
    args=["/app/chinook_mcp_server.py"],
    env={**os.environ},
)

ollama_api_key = os.getenv("OLLAMA_API_KEY")
if not ollama_api_key:
    raise ValueError("Set OLLAMA_API_KEY before running this script.")

model = LiteLLMModel(
    model_id="ollama_chat/gpt-oss:20b",
    api_base="https://ollama.com",
    api_key=ollama_api_key,
    temperature=0.2,
)

with MCPClient(server_parameters) as tools:
    agent = CodeAgent(tools=tools, model=model, add_base_tools=True)
    answer = agent.run("Who is the customer that spent the most money? Give me the name")
    print(answer)
