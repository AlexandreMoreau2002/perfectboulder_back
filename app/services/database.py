import asyncio

import psycopg

from app.config import Settings


def _run_database_probe(dsn: str) -> None:
    with psycopg.connect(conninfo=dsn, connect_timeout=5) as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1;")
            cursor.fetchone()


async def ensure_database_ready(settings: Settings) -> None:
    try:
        await asyncio.wait_for(
            asyncio.to_thread(_run_database_probe, settings.resolved_database_url),
            timeout=10,
        )
    except Exception as exc:  # pragma: no cover - defensive logging surface
        raise RuntimeError("Database connection failed") from exc
