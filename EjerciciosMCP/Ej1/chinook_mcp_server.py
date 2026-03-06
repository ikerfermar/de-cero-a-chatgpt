from pathlib import Path
import sqlite3
from typing import Any

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Chinook MCP Server")

DB_PATH = Path(__file__).resolve().parent / "Chinook_Sqlite.sqlite"


def get_connection() -> sqlite3.Connection:
    """Create a sqlite connection with row dict-like access."""
    connection = sqlite3.connect(str(DB_PATH))
    connection.row_factory = sqlite3.Row
    return connection


def _query_select(query: str) -> dict[str, Any]:
    """Execute read-only SQL and cap response size."""
    sql = query.strip().rstrip(";")
    if not sql.lower().startswith("select"):
        return {"ok": False, "error": "Only SELECT statements are allowed."}

    try:
        with get_connection() as connection:
            cursor = connection.execute(sql)
            rows = cursor.fetchmany(100)
            columns = [d[0] for d in cursor.description] if cursor.description else []

        payload_rows = [dict(row) for row in rows]
        return {
            "ok": True,
            "columns": columns,
            "rows": payload_rows,
            "row_count": len(payload_rows),
            "truncated": len(payload_rows) == 100,
        }
    except Exception as error:  # pragma: no cover
        return {"ok": False, "error": str(error)}


@mcp.tool()
def query_database(query: str) -> dict[str, Any]:
    """Run a SELECT SQL query against Chinook and return up to 100 rows."""
    return _query_select(query)


@mcp.tool()
def show_tables() -> dict[str, Any]:
    """List database tables available in Chinook."""
    sql = "SELECT name FROM sqlite_master WHERE type = 'table' ORDER BY name"
    result = _query_select(sql)
    if not result.get("ok"):
        return result

    table_names = [row["name"] for row in result["rows"]]
    return {"ok": True, "tables": table_names, "table_count": len(table_names)}


@mcp.tool()
def describe_table(table_name: str) -> dict[str, Any]:
    """Describe table schema (column info) for a given table name."""
    cleaned_name = table_name.strip().replace("'", "''")
    sql = f"PRAGMA table_info('{cleaned_name}')"

    try:
        with get_connection() as connection:
            cursor = connection.execute(sql)
            rows = cursor.fetchall()

        columns = [dict(row) for row in rows]
        if not columns:
            return {"ok": False, "error": f"Table '{table_name}' not found."}

        return {"ok": True, "table": table_name, "columns": columns}
    except Exception as error:  # pragma: no cover
        return {"ok": False, "error": str(error)}


@mcp.prompt()
def sql_agent_instructions() -> str:
    """Prompt instructions to help clients use the SQL tools safely."""
    return (
        "Use show_tables first if schema is unknown. "
        "Use describe_table before writing complex joins. "
        "Use query_database only with SELECT statements."
    )


if __name__ == "__main__":
    mcp.run()
