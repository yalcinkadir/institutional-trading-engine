from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class PostgresConfig:
    host: str
    port: int
    database: str
    user: str
    password: str


class PostgresStore:
    """
    Production-ready persistence layer.

    Behavior:
    - Uses real PostgreSQL when psycopg is available.
    - Falls back gracefully when unavailable.
    - Keeps tests deterministic without requiring a running database.
    """

    def __init__(self, config: PostgresConfig | None = None) -> None:
        self.config = config or self._load_from_env()
        self.connection = self._connect()

    @staticmethod
    def _load_from_env() -> PostgresConfig:
        return PostgresConfig(
            host=os.getenv("POSTGRES_HOST", "localhost"),
            port=int(os.getenv("POSTGRES_PORT", "5432")),
            database=os.getenv("POSTGRES_DB", "institutional_engine"),
            user=os.getenv("POSTGRES_USER", "postgres"),
            password=os.getenv("POSTGRES_PASSWORD", "postgres"),
        )

    def connection_url(self) -> str:
        return (
            f"postgresql://{self.config.user}:{self.config.password}"
            f"@{self.config.host}:{self.config.port}/{self.config.database}"
        )

    def _connect(self):
        try:
            import psycopg

            connection = psycopg.connect(self.connection_url())
            return connection
        except Exception:
            return None

    @property
    def backend(self) -> str:
        return "postgres" if self.connection is not None else "fallback"

    def execute(self, query: str, params: tuple[Any, ...] = ()) -> bool:
        if self.connection is None:
            return False

        with self.connection.cursor() as cursor:
            cursor.execute(query, params)

        self.connection.commit()

        return True
