FROM python:3.11-slim

WORKDIR /app

COPY chinook_mcp_server.py /app/chinook_mcp_server.py
COPY Chinook_Sqlite.sqlite /app/Chinook_Sqlite.sqlite

RUN pip install --no-cache-dir "mcp[cli]"

CMD ["python", "/app/chinook_mcp_server.py"]
