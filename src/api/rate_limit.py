from __future__ import annotations

import time
from collections import defaultdict

from fastapi import HTTPException


class SimpleRateLimiter:
    def __init__(self, limit: int = 60, window_seconds: int = 60) -> None:
        self.limit = limit
        self.window_seconds = window_seconds
        self.requests: dict[str, list[float]] = defaultdict(list)

    def check(self, key: str) -> None:
        now = time.time()
        window_start = now - self.window_seconds

        self.requests[key] = [
            timestamp
            for timestamp in self.requests[key]
            if timestamp >= window_start
        ]

        if len(self.requests[key]) >= self.limit:
            raise HTTPException(status_code=429, detail="Rate limit exceeded")

        self.requests[key].append(now)


rate_limiter = SimpleRateLimiter()
