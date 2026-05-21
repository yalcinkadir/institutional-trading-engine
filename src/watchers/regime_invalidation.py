"""Regime invalidation helper for open long-side signals.

No broker execution is performed here. The helper only updates signal state so
watcher/runtime flows can persist and notify regime exits deterministically.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


REGIME_INVALIDATION_EVENT = "REGIME_INVALIDATION_EXIT"
REGIME_INVALIDATION_STATUS = "CANCELLED_BY_REGIME_CHANGE"
ACTIVE_STATUSES = {"TRIGGERED", "TARGET_1_HIT"}
TERMINAL_STATUSES = {
    "STOP_HIT",
    "TARGET_2_HIT",
    "EXPIRED",
    REGIME_INVALIDATION_STATUS,
}
ACTIONABLE_ACTIONS = {"BUY_WATCH"}
RISK_OFF_LABELS = {
    "risk_off",
    "risk-off",
    "risk off",
    "bearish",
    "defensive",
    "capital_protection",
    "capital protection",
    "avoid_longs",
    "avoid longs",
}


@dataclass(frozen=True)
class RegimeInvalidationResult:
    signal: dict[str, Any]
    invalidated: bool
    event_type: str | None = None
    previous_status: str | None = None
    new_status: str | None = None
    reasons: list[str] = field(default_factory=list)


def normalize_regime_label(regime: Any) -> str:
    """Normalize regime input for defensive/risk-off matching."""
    if isinstance(regime, dict):
        for key in ("risk_state", "regime", "market_regime", "state", "label"):
            value = regime.get(key)
            if value:
                return normalize_regime_label(value)
        return "unknown"
    text = str(regime or "unknown").strip().lower().replace("_", " ").replace("-", " ")
    return " ".join(text.split())


def is_risk_off_regime(regime: Any) -> bool:
    normalized = normalize_regime_label(regime)
    compact = normalized.replace(" ", "_")
    dashed = normalized.replace(" ", "-")
    return normalized in RISK_OFF_LABELS or compact in RISK_OFF_LABELS or dashed in RISK_OFF_LABELS


def apply_regime_invalidation(
    signal: dict[str, Any],
    *,
    regime: Any,
    timestamp: str,
) -> RegimeInvalidationResult:
    """Invalidate an active signal when the regime is defensive/risk-off."""
    updated = dict(signal)
    previous_status = str(updated.get("status") or "PENDING")
    action = str(updated.get("action") or "")

    if action not in ACTIONABLE_ACTIONS:
        return RegimeInvalidationResult(
            signal=updated,
            invalidated=False,
            previous_status=previous_status,
            reasons=["non_actionable_signal"],
        )

    if previous_status in TERMINAL_STATUSES:
        return RegimeInvalidationResult(
            signal=updated,
            invalidated=False,
            previous_status=previous_status,
            reasons=["terminal_signal"],
        )

    if previous_status not in ACTIVE_STATUSES:
        return RegimeInvalidationResult(
            signal=updated,
            invalidated=False,
            previous_status=previous_status,
            reasons=["signal_not_active"],
        )

    if not is_risk_off_regime(regime):
        return RegimeInvalidationResult(
            signal=updated,
            invalidated=False,
            previous_status=previous_status,
            reasons=["regime_not_risk_off"],
        )

    updated["status"] = REGIME_INVALIDATION_STATUS
    updated["last_event_at"] = timestamp
    updated["last_event_price"] = updated.get("last_event_price")
    updated["regime_invalidation_at"] = timestamp
    updated["regime_invalidation_reason"] = normalize_regime_label(regime)

    return RegimeInvalidationResult(
        signal=updated,
        invalidated=True,
        event_type=REGIME_INVALIDATION_EVENT,
        previous_status=previous_status,
        new_status=REGIME_INVALIDATION_STATUS,
        reasons=["risk_off_regime_invalidated_active_signal"],
    )
