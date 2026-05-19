from __future__ import annotations

import json
import time
from typing import Any


class RedisCache:
    """
    Redis cache abstraction layer.

    Current implementation:
    - in-memory fallback cache
    - TTL support
    - serialization support

    Future:
    - real Redis backend
    - distributed caching
    - pub/sub events
    - cache invalidation policies
    """

    def __init__(self) -> None:
        self._cache: dict[str, tuple[float, str]] = {}

    def set(
        self,
        key: str,
        value: Any,
        ttl_seconds: int = 300,
    ) -> None:
        expires_at = time.time() + ttl_seconds
        serialized = json.dumps(value)
        self._cache[key] = (expires_at, serialized)

    def get(self, key: str) -> Any | None:
        item = self._cache.get(key)

        if item is None:
            return None

        expires_at, serialized = item

        if time.time() > expires_at:
            self._cache.pop(key, None)
            return None

        return json.loads(serialized)

    def clear(self) -> None:
        self._cache.clear()
