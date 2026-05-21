"""Entry quality engine for executable signal generation.

The engine derives deterministic entry triggers and explains why an entry is
valid or invalid. It is intentionally lightweight and testable.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class EntryQualityResult:
    is_valid: bool
    entry_trigger: float | None
    entry_type: str
    entry_reason: str
    reasons: list[str] = field(default_factory=list)


def _safe_float(value: Any) -> float | None:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _round_price(value: float) -> float:
    return round(value, 2)


def _reject(reason: str, *, entry_type: str = "n/a") -> EntryQualityResult:
    return EntryQualityResult(
        is_valid=False,
        entry_trigger=None,
        entry_type=entry_type,
        entry_reason=f"invalid_entry: {reason}",
        reasons=[reason],
    )


def derive_entry_quality(
    *,
    setup_type: str,
    close: float | None,
    atr: float | None,
    scanner_metrics: dict[str, Any] | None = None,
    allow_at_market: bool = False,
    max_breakout_extension_atr: float = 1.5,
) -> EntryQualityResult:
    """Derive and validate an entry trigger.

    Supported deterministic entry types:
    - breakout for momentum_breakout and default trend setups
    - pullback for pullback_continuation
    - retest for retest_continuation
    - gap_fill for gap_fill
    - at_market only when explicitly allowed
    """

    if close is None:
        return _reject("missing_close")
    if atr is None or atr <= 0:
        return _reject("missing_or_invalid_atr")

    scanner = scanner_metrics or {}
    explicit_entry = _safe_float(scanner.get("entry"))
    explicit_entry_type = str(scanner.get("entry_type") or "").strip()

    if explicit_entry is not None:
        entry_type = explicit_entry_type or "scanner_provided"
        if explicit_entry <= 0:
            return _reject("invalid_scanner_entry", entry_type=entry_type)
        extension_atr = (close - explicit_entry) / atr
        if entry_type in {"breakout", "break_above", "scanner_provided"} and extension_atr > max_breakout_extension_atr:
            return EntryQualityResult(
                is_valid=False,
                entry_trigger=_round_price(explicit_entry),
                entry_type=entry_type,
                entry_reason="invalid_entry: late_entry_price_extended_beyond_trigger",
                reasons=["late_entry_price_extended_beyond_trigger"],
            )
        return EntryQualityResult(
            is_valid=True,
            entry_trigger=_round_price(explicit_entry),
            entry_type=entry_type,
            entry_reason="scanner provided executable entry level",
        )

    normalized_setup = setup_type.lower().strip()

    if normalized_setup == "momentum_breakout":
        entry = close + 0.5 * atr
        return EntryQualityResult(
            is_valid=True,
            entry_trigger=_round_price(entry),
            entry_type="breakout",
            entry_reason="breakout entry above current close using 0.5 ATR buffer",
        )

    if normalized_setup == "pullback_continuation":
        entry = close - 1.0 * atr
        return EntryQualityResult(
            is_valid=True,
            entry_trigger=_round_price(entry),
            entry_type="pullback",
            entry_reason="pullback entry near 1 ATR below current close",
        )

    if normalized_setup == "retest_continuation":
        entry = close - 0.5 * atr
        return EntryQualityResult(
            is_valid=True,
            entry_trigger=_round_price(entry),
            entry_type="retest",
            entry_reason="retest entry near 0.5 ATR below current close",
        )

    if normalized_setup == "gap_fill":
        entry = close - 0.75 * atr
        return EntryQualityResult(
            is_valid=True,
            entry_trigger=_round_price(entry),
            entry_type="gap_fill",
            entry_reason="gap-fill entry near 0.75 ATR below current close",
        )

    if normalized_setup in {"defensive_rotation", "mean_reversion"}:
        if not allow_at_market:
            return _reject("at_market_entry_not_allowed", entry_type="at_market")
        return EntryQualityResult(
            is_valid=True,
            entry_trigger=_round_price(close),
            entry_type="at_market",
            entry_reason="at-market entry explicitly allowed for defensive/mean-reversion setup",
        )

    entry = close + 0.3 * atr
    return EntryQualityResult(
        is_valid=True,
        entry_trigger=_round_price(entry),
        entry_type="breakout",
        entry_reason="default breakout entry using 0.3 ATR buffer",
    )
