from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import UTC, datetime
from typing import Literal

RecommendationAction = Literal["ENTER", "MONITOR", "WAIT", "AVOID"]


@dataclass
class Recommendation:
    ticker: str
    action: RecommendationAction
    score: int
    confidence: float
    market_regime: str
    entry_price: float | None = None
    stop_price: float | None = None
    target_price: float | None = None
    created_at: str = ""

    def to_dict(self) -> dict:
        data = asdict(self)
        if not data["created_at"]:
            data["created_at"] = datetime.now(UTC).isoformat()
        return data


def create_recommendation(
    ticker: str,
    action: RecommendationAction,
    score: int,
    confidence: float,
    market_regime: str,
    entry_price: float | None = None,
    stop_price: float | None = None,
    target_price: float | None = None,
) -> dict:
    return Recommendation(
        ticker=ticker,
        action=action,
        score=score,
        confidence=confidence,
        market_regime=market_regime,
        entry_price=entry_price,
        stop_price=stop_price,
        target_price=target_price,
    ).to_dict()
