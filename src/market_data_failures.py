"""Canonical market-data failure taxonomy.

The scanner must not collapse provider errors, empty payloads, rate limits, and
network failures into an undifferentiated `None`. This module gives downstream
quality gates one shared vocabulary for blocking, degrading, reporting, and
alerting.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any


class MarketDataFailureKind(str, Enum):
    MISSING_API_KEY = "MISSING_API_KEY"
    AUTH_FORBIDDEN = "AUTH_FORBIDDEN"
    RATE_LIMIT = "RATE_LIMIT"
    EMPTY_BARS = "EMPTY_BARS"
    HTTP_ERROR = "HTTP_ERROR"
    NETWORK_ERROR = "NETWORK_ERROR"
    PARSE_ERROR = "PARSE_ERROR"


@dataclass(frozen=True)
class MarketDataFailure:
    symbol: str
    kind: MarketDataFailureKind
    message: str
    provider: str = "polygon"
    status_code: int | None = None
    attempts: int = 1

    def as_metrics_fields(self) -> dict[str, Any]:
        return {
            "source": self.provider,
            "fallback_level": "primary",
            "data_status": "BLOCKED",
            "data_failure_kind": self.kind.value,
            "data_failure_message": self.message,
            "provider_status_code": self.status_code,
        }
