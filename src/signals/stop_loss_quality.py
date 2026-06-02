"""Stop-loss quality engine for executable signal generation.

The engine derives deterministic long-side stops and explains why a stop is
valid or invalid. TradePlanValidator remains the final executable gate.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


MAX_STRUCTURE_STOP_ATR_DISTANCE = 3.0
MAX_ATR_STOP_DISTANCE = 2.0
STRUCTURE_STOP_BUFFER = 0.998
SUPPORTED_SIDE = "long"


@dataclass(frozen=True)
class StopLossQualityResult:
    is_valid: bool
    stop_loss: float | None
    stop_model: str
    stop_reason: str
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


def _reject(reason: str, *, stop_model: str = "n/a", stop_loss: float | None = None) -> StopLossQualityResult:
    return StopLossQualityResult(
        is_valid=False,
        stop_loss=stop_loss,
        stop_model=stop_model,
        stop_reason=f"invalid_stop: {reason}",
        reasons=[reason],
    )


def _stop_distance_atr(entry_trigger: float, stop: float, atr: float) -> float:
    return (entry_trigger - stop) / atr


def _reject_if_stop_too_far(
    stop: float,
    *,
    entry_trigger: float,
    atr: float,
    stop_model: str,
) -> StopLossQualityResult | None:
    if _stop_distance_atr(entry_trigger, stop, atr) > MAX_ATR_STOP_DISTANCE:
        return _reject(
            "stop_distance_exceeds_max_atr",
            stop_model=stop_model,
            stop_loss=_round_price(stop),
        )
    return None


def _accept_computed_stop(
    stop: float,
    *,
    entry_trigger: float,
    atr: float,
    stop_model: str,
    stop_reason: str,
    enforce_max_atr_distance: bool = True,
) -> StopLossQualityResult:
    if stop <= 0:
        return _reject("computed_stop_non_positive", stop_model=stop_model)
    if enforce_max_atr_distance:
        too_far = _reject_if_stop_too_far(
            stop,
            entry_trigger=entry_trigger,
            atr=atr,
            stop_model=stop_model,
        )
        if too_far is not None:
            return too_far
    return StopLossQualityResult(
        is_valid=True,
        stop_loss=_round_price(stop),
        stop_model=stop_model,
        stop_reason=stop_reason,
    )


def _structure_stop_from_swing_low(
    *,
    swing_low: float | None,
    entry_trigger: float,
    atr: float,
) -> StopLossQualityResult | None:
    if swing_low is None or swing_low <= 0:
        return None
    if swing_low >= entry_trigger:
        return None

    stop = swing_low * STRUCTURE_STOP_BUFFER
    atr_distance = _stop_distance_atr(entry_trigger, stop, atr)
    if atr_distance > MAX_STRUCTURE_STOP_ATR_DISTANCE:
        return None

    return _accept_computed_stop(
        stop,
        entry_trigger=entry_trigger,
        atr=atr,
        stop_model="swing_low_structure_stop",
        stop_reason="swing-low structure stop with 0.2 percent buffer",
        enforce_max_atr_distance=False,
    )


def derive_stop_loss_quality(
    *,
    setup_type: str,
    entry_trigger: float | None,
    close: float | None,
    atr: float | None,
    entry_type: str,
    scanner_metrics: dict[str, Any] | None = None,
    side: str = SUPPORTED_SIDE,
) -> StopLossQualityResult:
    """Derive and validate a long-side stop loss.

    Supported deterministic stop models:
    - scanner_provided_stop
    - swing_low_structure_stop
    - atr_stop
    - pullback_structure_stop
    - retest_structure_stop
    - gap_fill_stop

    Short-side stops are intentionally rejected until explicitly implemented.
    """

    normalized_side = (side or "").lower().strip()
    if normalized_side != SUPPORTED_SIDE:
        return _reject(f"unsupported_side:{normalized_side or 'missing'}", stop_model="unsupported_side")

    if entry_trigger is None:
        return _reject("missing_entry_trigger")
    if entry_trigger <= 0:
        return _reject("invalid_entry_trigger")
    if close is None:
        return _reject("missing_close")
    if close <= 0:
        return _reject("missing_or_invalid_close")
    if atr is None or atr <= 0:
        return _reject("missing_or_invalid_atr")

    scanner = scanner_metrics or {}
    explicit_stop = _safe_float(scanner.get("stop_loss"))
    if explicit_stop is not None:
        if explicit_stop <= 0:
            return _reject("invalid_scanner_stop", stop_model="scanner_provided_stop", stop_loss=explicit_stop)
        if explicit_stop >= entry_trigger:
            return _reject(
                "scanner_stop_not_below_entry",
                stop_model="scanner_provided_stop",
                stop_loss=_round_price(explicit_stop),
            )
        too_far = _reject_if_stop_too_far(
            explicit_stop,
            entry_trigger=entry_trigger,
            atr=atr,
            stop_model="scanner_provided_stop",
        )
        if too_far is not None:
            return too_far
        return StopLossQualityResult(
            is_valid=True,
            stop_loss=_round_price(explicit_stop),
            stop_model="scanner_provided_stop",
            stop_reason="scanner provided stop below entry",
        )

    swing_low_stop = _structure_stop_from_swing_low(
        swing_low=_safe_float(scanner.get("swing_low_3bar")),
        entry_trigger=entry_trigger,
        atr=atr,
    )
    if swing_low_stop is not None:
        return swing_low_stop

    normalized_setup = setup_type.lower().strip()
    normalized_entry_type = entry_type.lower().strip()

    if normalized_entry_type == "pullback" or normalized_setup == "pullback_continuation":
        stop = entry_trigger - 1.5 * atr
        return _accept_computed_stop(
            stop,
            entry_trigger=entry_trigger,
            atr=atr,
            stop_model="pullback_structure_stop",
            stop_reason="pullback structure stop 1.5 ATR below entry",
        )

    if normalized_entry_type == "retest" or normalized_setup == "retest_continuation":
        stop = entry_trigger - 1.25 * atr
        return _accept_computed_stop(
            stop,
            entry_trigger=entry_trigger,
            atr=atr,
            stop_model="retest_structure_stop",
            stop_reason="retest structure stop 1.25 ATR below entry",
        )

    if normalized_entry_type == "gap_fill" or normalized_setup == "gap_fill":
        stop = entry_trigger - 1.5 * atr
        return _accept_computed_stop(
            stop,
            entry_trigger=entry_trigger,
            atr=atr,
            stop_model="gap_fill_stop",
            stop_reason="gap-fill stop 1.5 ATR below entry",
        )

    if normalized_entry_type == "at_market":
        stop = entry_trigger - MAX_ATR_STOP_DISTANCE * atr
        return _accept_computed_stop(
            stop,
            entry_trigger=entry_trigger,
            atr=atr,
            stop_model="atr_stop",
            stop_reason="at-market volatility stop 2 ATR below entry; max 2.0 ATR",
        )

    stop = entry_trigger - MAX_ATR_STOP_DISTANCE * atr
    return _accept_computed_stop(
        stop,
        entry_trigger=entry_trigger,
        atr=atr,
        stop_model="atr_stop",
        stop_reason="ATR stop 2 ATR below entry; max 2.0 ATR",
    )
