from __future__ import annotations

import json
import os
import time
from typing import Any


class RedisCache:
    """
    Redis cache abstraction layer.

    Behavior:
    - Uses real Redis when REDIS_ENABLED=true and redis package is available.
    - Falls back to deterministic in-memory cache when Redis is unavailable.

    This keeps local tests stable while allowing production deployments to use Redis.
    """

    def __init__(self) -> None:
        self._cache: dict[str, tuple[float, str]] = {}
        self._redis = self._connect_redis()

    def _connect_redis(self):
        if os.getenv("REDIS_ENABLED", "false").lower() != "true":
            return None

        try:
            import redis

            host = os.getenv("REDIS_HOST", "localhost")
            port = int(os.getenv("REDIS_PORT", "6379"))
            db = int(os.getenv("REDIS_DB", "0"))

            client = redis.Redis(
                host=host,
                port=port,
                db=db,
                decode_responses=True,
                socket_connect_timeout=2,
                socket_timeout=2,
            )
            client.ping()
            return client
        except Exception:
            return None

    @property
    def backend(self) -> str:
        return "redis" if self._redis is not None else "memory"

    def set(
        self,
        key: str,
        value: Any,
        ttl_seconds: int = 300,
    ) -> None:
        serialized = json.dumps(value)

        if self._redis is not None:
            self._redis.setex(key, ttl_seconds, serialized)
            return

        expires_at = time.time() + ttl_seconds
        self._cache[key] = (expires_at, serialized)

    def get(self, key: str) -> Any | None:
        if self._redis is not None:
            value = self._redis.get(key)
            return json.loads(value) if value is not None else None

        item = self._cache.get(key)

        if item is None:
            return None

        expires_at, serialized = item

        if time.time() > expires_at:
            self._cache.pop(key, None)
            return None

        return json.loads(serialized)

    def clear(self) -> None:
        if self._redis is not None:
            self._redis.flushdb()
            return

        self._cache.clear()
