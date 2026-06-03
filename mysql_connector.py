import os
from typing import Any, Generator, Optional
import pymysql
from dotenv import load_dotenv
from pymysql.cursors import DictCursor
from contextlib import contextmanager

load_dotenv('.env')

config: dict[str, Optional[str]] = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_DATABASE'),
}


@contextmanager
def get_cursor() -> Generator[DictCursor, None, None]:
    """Context manager to safely instantiate, yield, and close a MySQL connection and cursor."""
    try:
        with pymysql.connect(**config) as connection:
            with connection.cursor(DictCursor) as cursor:
                yield cursor
    except pymysql.Error as e:
        print(f"Database error: {e}")
        raise


def execute_query(query: str, parameter: Optional[tuple[Any, ...]] = None) -> list[dict[str, Any]]:
    """Executes a parameterized SQL query against the MySQL database and returns all matching records.

    Args:
        query: The raw SQL statement string to execute.
        parameter: Values to bind securely to the query parameters.
    """
    with get_cursor() as cursor:
        cursor.execute(query, parameter)
        return cursor.fetchall()