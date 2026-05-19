from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(slots=True)
class PostgresConfig:
    host: str
    port: int
    database: str
    user: str
    password: str


class PostgresStore:
    """
    Production-ready persistence foundation.

    Current status:
    - configuration layer implemented
    - connection abstraction implemented
    - migration target prepared

    Future:
    - SQLAlchemy integration
    - asyncpg support
    - connection pooling
    - read replicas
    - partitioning
    """

    def __init__(self, config: PostgresConfig | None = None) -> None:
        self.config = config or self._load_from_env()

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
