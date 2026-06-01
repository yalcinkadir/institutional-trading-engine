from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Optional


class PaperObservationDecision(str, Enum):
    BUY = "BUY"
    WAIT = "WAIT"
    REJECT = "REJECT"
    UNKNOWN = "UNKNOWN"


class PaperObservationReview(str, Enum):
    UNREVIEWED = "UNREVIEWED"
    CORRECT = "CORRECT"
    INCORRECT = "INCORRECT"
    NEEDS_INVESTIGATION = "NEEDS_INVESTIGATION"


@dataclass(frozen=True)
class PaperObservationRecord:
    observation_id: str
    created_at: str

    signal_id: str
    symbol: str

    market_regime: Optional[str]
    setup_classification: Optional[str]
    decision: PaperObservationDecision

    entry_level: Optional[float]
    stop_level: Optional[float]
    target_1: Optional[float]
    target_2: Optional[float]

    runner_state: Optional[str]
    alert_payload: dict[str, Any]

    actual_market_behavior: Optional[str] = None
    review: PaperObservationReview = PaperObservationReview.UNREVIEWED
    review_notes: Optional[str] = None

    @staticmethod
    def utc_now_iso() -> str:
        return datetime.now(timezone.utc).isoformat()

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["decision"] = self.decision.value
        data["review"] = self.review.value
        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "PaperObservationRecord":
        return cls(
            observation_id=data["observation_id"],
            created_at=data["created_at"],
            signal_id=data["signal_id"],
            symbol=data["symbol"],
            market_regime=data.get("market_regime"),
            setup_classification=data.get("setup_classification"),
            decision=PaperObservationDecision(data.get("decision", "UNKNOWN")),
            entry_level=data.get("entry_level"),
            stop_level=data.get("stop_level"),
            target_1=data.get("target_1"),
            target_2=data.get("target_2"),
            runner_state=data.get("runner_state"),
            alert_payload=data.get("alert_payload", {}),
            actual_market_behavior=data.get("actual_market_behavior"),
            review=PaperObservationReview(data.get("review", "UNREVIEWED")),
            review_notes=data.get("review_notes"),
        )