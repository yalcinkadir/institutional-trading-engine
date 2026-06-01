from __future__ import annotations

import hashlib
from typing import Any, Optional

from .paper_observation_models import (
    PaperObservationDecision,
    PaperObservationRecord,
)
from .paper_observation_store import PaperObservationStore


class PaperObservationService:
    """
    Converts system decisions into paper observation records.

    This service must not place trades.
    This service must not modify decision output.
    This service only observes and records.
    """

    def __init__(self, store: PaperObservationStore) -> None:
        self.store = store

    def record_decision(
        self,
        *,
        signal_id: str,
        symbol: str,
        decision: str,
        market_regime: Optional[str] = None,
        setup_classification: Optional[str] = None,
        entry_level: Optional[float] = None,
        stop_level: Optional[float] = None,
        target_1: Optional[float] = None,
        target_2: Optional[float] = None,
        runner_state: Optional[str] = None,
        alert_payload: Optional[dict[str, Any]] = None,
    ) -> PaperObservationRecord:
        normalized_decision = self._normalize_decision(decision)

        record = PaperObservationRecord(
            observation_id=self._build_observation_id(
                signal_id=signal_id,
                symbol=symbol,
                decision=normalized_decision.value,
            ),
            created_at=PaperObservationRecord.utc_now_iso(),
            signal_id=signal_id,
            symbol=symbol.upper(),
            market_regime=market_regime,
            setup_classification=setup_classification,
            decision=normalized_decision,
            entry_level=entry_level,
            stop_level=stop_level,
            target_1=target_1,
            target_2=target_2,
            runner_state=runner_state,
            alert_payload=alert_payload or {},
        )

        self.store.append(record)
        return record

    @staticmethod
    def _normalize_decision(decision: str) -> PaperObservationDecision:
        try:
            return PaperObservationDecision(decision.upper())
        except ValueError:
            return PaperObservationDecision.UNKNOWN

    @staticmethod
    def _build_observation_id(
        *,
        signal_id: str,
        symbol: str,
        decision: str,
    ) -> str:
        raw = f"{signal_id}|{symbol.upper()}|{decision}"
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:24]