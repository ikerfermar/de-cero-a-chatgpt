FROM python:3.11-slim

WORKDIR /app

COPY smolagents_mcp_client.py /app/smolagents_mcp_client.py
COPY langchain_mcp_client.py /app/langchain_mcp_client.py
COPY chinook_mcp_server.py /app/chinook_mcp_server.py
COPY Chinook_Sqlite.sqlite /app/Chinook_Sqlite.sqlite

RUN pip install --no-cache-dir \
    "mcp[cli]" \
    smolagents \
    litellm \
    langchain \
    langchain-ollama \
    langchain-mcp-adapters

# Default command runs the LangChain integration. Override CMD to run smolagents.
CMD ["python", "/app/langchain_mcp_client.py"]
