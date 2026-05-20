from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from typing import Any


@dataclass(frozen=True)
class RuntimeMarketSnapshot:
    spy_metrics: dict[str, Any]
    qqq_metrics: dict[str, Any]
    market_metrics: dict[str, Any]
    sector_metrics: dict[str, Any]
    volatility_metrics: dict[str, Any]
    timestamp: str

    @classmethod
    def create(
        cls,
        spy_metrics: dict[str, Any],
        qqq_metrics: dict[str, Any],
        market_metrics: dict[str, Any],
        sector_metrics: dict[str, Any],
        volatility_metrics: dict[str, Any],
    ) -> "RuntimeMarketSnapshot":
        return cls(
            spy_metrics=spy_metrics,
            qqq_metrics=qqq_metrics,
            market_metrics=market_metrics,
            sector_metrics=sector_metrics,
            volatility_metrics=volatility_metrics,
            timestamp=datetime.now(UTC).isoformat(),
        )

    def to_persistence_payload(self) -> dict[str, Any]:
        return asdict(self)
