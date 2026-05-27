"""Exit / target quality engine for executable signal generation.

The engine derives deterministic long-side targets and explains why exit levels
are valid or invalid. TradePlanValidator remains the final executable gate.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class ExitTargetQualityResult:
    is_valid: bool
    target_1: float | None
    target_2: float | None
    exit_model: str
    exit_reason: str
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


def _reject(
    reason: str,
    *,
    exit_model: str = "n/a",
    target_1: float | None = None,
    target_2: float | None = None,
) -> ExitTargetQualityResult:
    return ExitTargetQualityResult(
        is_valid=False,
        target_1=target_1,
        target_2=target_2,
        exit_model=exit_model,
        exit_reason=f"invalid_exit: {reason}",
        reasons=[reason],
    )


def _validate_targets(
    *,
    entry_trigger: float,
    target_1: float,
    target_2: float | None,
    exit_model: str,
    exit_reason: str,
) -> ExitTargetQualityResult:
    reasons: list[str] = []

    if target_1 <= entry_trigger:
        reasons.append("target_1_not_above_entry")
    if target_2 is not None and target_2 <= target_1:
        reasons.append("target_2_not_above_target_1")

    if reasons:
        return ExitTargetQualityResult(
            is_valid=False,
            target_1=_round_price(target_1),
            target_2=_round_price(target_2) if target_2 is not None else None,
            exit_model=exit_model,
            exit_reason=f"invalid_exit: {', '.join(reasons)}",
            reasons=reasons,
        )

    return ExitTargetQualityResult(
        is_valid=True,
        target_1=_round_price(target_1),
        target_2=_round_price(target_2) if target_2 is not None else None,
        exit_model=exit_model,
        exit_reason=exit_reason,
    )


def derive_exit_target_quality(
    *,
    setup_type: str,
    entry_trigger: float | None,
    stop_loss: float | None,
    atr: float | None,
    scanner_metrics: dict[str, Any] | None = None,
) -> ExitTargetQualityResult:
    """Derive and validate long-side target levels.

    Supported deterministic exit models:
    - scanner_provided_targets
    - momentum_targets
    - pullback_targets
    - retest_targets
    - gap_fill_targets
    - mean_reversion_targets
    - defensive_rotation_targets
    - default_risk_targets
    """

    if entry_trigger is None:
        return _reject("missing_entry_trigger")
    if stop_loss is None:
        return _reject("missing_stop_loss")
    if stop_loss >= entry_trigger:
        return _reject("stop_loss_not_below_entry")

    risk = entry_trigger - stop_loss
    if risk <= 0:
        return _reject("invalid_risk_per_share")

    scanner = scanner_metrics or {}
    explicit_t1 = _safe_float(scanner.get("exit_1"))
    explicit_t2 = _safe_float(scanner.get("exit_2"))
    if explicit_t1 is not None:
        return _validate_targets(
            entry_trigger=entry_trigger,
            target_1=explicit_t1,
            target_2=explicit_t2,
            exit_model="scanner_provided_targets",
            exit_reason="scanner provided target levels validated above entry",
        )

    normalized_setup = setup_type.lower().strip()

    if normalized_setup == "momentum_breakout":
        target_1 = entry_trigger + 1.5 * risk
        target_2 = entry_trigger + 2.5 * risk
        return _validate_targets(
            entry_trigger=entry_trigger,
            target_1=target_1,
            target_2=target_2,
            exit_model="momentum_targets",
            exit_reason="momentum targets at 1.5R and 2.5R",
        )

    if normalized_setup == "pullback_continuation":
        target_1 = entry_trigger + 1.35 * risk
        target_2 = entry_trigger + 2.25 * risk
        return _validate_targets(
            entry_trigger=entry_trigger,
            target_1=target_1,
            target_2=target_2,
            exit_model="pullback_targets",
            exit_reason="pullback continuation targets at 1.35R and 2.25R",
        )

    if normalized_setup == "retest_continuation":
        target_1 = entry_trigger + 1.4 * risk
        target_2 = entry_trigger + 2.3 * risk
        return _validate_targets(
            entry_trigger=entry_trigger,
            target_1=target_1,
            target_2=target_2,
            exit_model="retest_targets",
            exit_reason="retest continuation targets at 1.4R and 2.3R",
        )

    if normalized_setup == "gap_fill":
        target_1 = entry_trigger + 1.35 * risk
        target_2 = entry_trigger + 2.0 * risk
        return _validate_targets(
            entry_trigger=entry_trigger,
            target_1=target_1,
            target_2=target_2,
            exit_model="gap_fill_targets",
            exit_reason="gap-fill targets at 1.35R and 2.0R",
        )

    if normalized_setup == "mean_reversion":
        target_1 = entry_trigger + 1.0 * risk
        target_2 = entry_trigger + 1.5 * risk
        if atr is not None and atr > 0:
            target_1 = min(target_1, entry_trigger + 1.0 * atr)
            target_2 = min(target_2, entry_trigger + 1.5 * atr)
        return _validate_targets(
            entry_trigger=entry_trigger,
            target_1=target_1,
            target_2=target_2,
            exit_model="mean_reversion_targets",
            exit_reason="mean-reversion targets use quicker 1.0R/1.5R exits capped by 1.0/1.5 ATR when available",
        )

    if normalized_setup == "defensive_rotation":
        target_1 = entry_trigger + 1.2 * risk
        target_2 = entry_trigger + 1.8 * risk
        if atr is not None and atr > 0:
            target_1 = max(target_1, entry_trigger + 1.0 * atr)
            target_2 = max(target_2, entry_trigger + 1.5 * atr)
        return _validate_targets(
            entry_trigger=entry_trigger,
            target_1=target_1,
            target_2=target_2,
            exit_model="defensive_rotation_targets",
            exit_reason="defensive rotation targets use moderated 1.2R/1.8R exits with ATR floor when available",
        )

    target_1 = entry_trigger + 1.5 * risk
    target_2 = None
    if atr is not None and atr > 0:
        target_1 = max(target_1, entry_trigger + 2.0 * atr)

    return _validate_targets(
        entry_trigger=entry_trigger,
        target_1=target_1,
        target_2=target_2,
        exit_model="default_risk_targets",
        exit_reason="default target using at least 1.5R or 2 ATR when available",
    )
