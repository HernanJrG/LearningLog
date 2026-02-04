import os
from contextlib import contextmanager

import psycopg2
from psycopg2.extras import RealDictCursor


def _require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def get_connection():
    """Create a new database connection using env vars or DATABASE_URL."""
    dsn = os.getenv("DATABASE_URL")
    if dsn:
        return psycopg2.connect(dsn, cursor_factory=RealDictCursor)

    host = os.getenv("DB_HOST", "localhost")
    port = int(os.getenv("DB_PORT", "5432"))
    dbname = _require_env("DB_NAME")
    user = _require_env("DB_USER")
    password = _require_env("DB_PASSWORD")

    return psycopg2.connect(
        host=host,
        port=port,
        dbname=dbname,
        user=user,
        password=password,
        cursor_factory=RealDictCursor,
    )


@contextmanager
def get_cursor():
    """Provide a cursor with automatic commit/rollback and cleanup."""
    conn = get_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                yield cur
    finally:
        conn.close()
