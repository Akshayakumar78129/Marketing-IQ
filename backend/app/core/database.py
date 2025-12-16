import snowflake.connector
from snowflake.connector import DictCursor
from contextlib import contextmanager
from typing import Generator, Any

from app.core.config import settings


def get_snowflake_connection() -> snowflake.connector.SnowflakeConnection:
    """Create a new Snowflake connection."""
    return snowflake.connector.connect(
        account=settings.SNOWFLAKE_ACCOUNT,
        user=settings.SNOWFLAKE_USER,
        password=settings.SNOWFLAKE_PASSWORD,
        database=settings.SNOWFLAKE_DATABASE,
        schema=settings.SNOWFLAKE_SCHEMA,
        warehouse=settings.SNOWFLAKE_WAREHOUSE,
        role=settings.SNOWFLAKE_ROLE,
    )


@contextmanager
def get_db_cursor() -> Generator[Any, None, None]:
    """Context manager for database cursor with automatic cleanup."""
    conn = get_snowflake_connection()
    cursor = conn.cursor()
    try:
        yield cursor
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()


def execute_query(
    query: str,
    params: dict[str, Any] | None = None
) -> list[dict[str, Any]]:
    """
    Execute a SQL query and return results as a list of dictionaries.

    Args:
        query: SQL query string
        params: Optional parameters for parameterized queries (prevents SQL injection)

    Returns:
        List of dictionaries, where each dict represents a row with column names as keys

    Example:
        # Simple query
        results = execute_query("SELECT * FROM campaigns WHERE status = 'Active'")

        # Parameterized query (safer)
        results = execute_query(
            "SELECT * FROM campaigns WHERE account_id = %(account_id)s",
            params={"account_id": 123}
        )
    """
    conn = get_snowflake_connection()
    try:
        cursor = conn.cursor(DictCursor)
        try:
            cursor.execute(query, params)
            results = cursor.fetchall()
            return results if results else []
        finally:
            cursor.close()
    finally:
        conn.close()
