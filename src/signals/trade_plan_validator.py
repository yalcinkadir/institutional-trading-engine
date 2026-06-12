"""Trade plan validation for executable signal quality.

A high setup score is not enough. A BUY_WATCH signal needs a complete,
ordered and risk-valid trade plan.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class TradePlanValidationResult:
    is_valid: bool
    reasons: list[str] = field(default_factory=list)
    risk_reward: float | None = None
    risk_per_share: float | None = None
    reward_per_share: float | None = None
    stop_distance_atr: float | None = None
    portfolio_risk_status: str = "NOT_EVALUATED"
    portfolio_risk_block_reason: str | None = None
    portfolio_risk_multiplier: float | None = None


def _is_missing(value: float | None) -> bool:
    return value is None


def _round_or_none(value: float | None, digits: int = 4) -> float | None:
    if value is None:
        return None
    return round(value, digits)


def _portfolio_multiplier_for_symbol(portfolio_risk_result: Any, symbol: str | None) -> float | None:
    if portfolio_risk_result is None or symbol is None:
        return None
    for item in getattr(portfolio_risk_result, "symbol_risk_multipliers", ()):
        if len(item) != 2:
            continue
        item_symbol, multiplier = item
        if item_symbol == symbol:
            return float(multiplier)
    return None


def _portfolio_risk_reasons(portfolio_risk_result: Any, symbol: str | None) -> list[str]:
    if portfolio_risk_result is None:
        return ["portfolio_risk_context_missing"]

    reasons: list[str] = []
    concentration_warnings = tuple(getattr(portfolio_risk_result, "concentration_warnings", ()))
    correlation_warnings = tuple(getattr(portfolio_risk_result, "correlation_warnings", ()))
    reduced_symbols = tuple(getattr(portfolio_risk_result, "reduced_symbols", ()))

    if concentration_warnings:
        reasons.extend(str(reason) for reason in concentration_warnings)
    if correlation_warnings:
        reasons.extend(str(reason) for reason in correlation_warnings)
    if symbol is not None and symbol in reduced_symbols and not reasons:
        reasons.append(f"portfolio_symbol_reduced:{symbol}")

    return reasons


def validate_long_trade_plan(
    *,
    entry_trigger: float | None,
    stop_loss: float | None,
    target_1: float | None,
    target_2: float | None = None,
    atr: float | None = None,
    min_risk_reward: float = 1.2,
    min_stop_atr: float = 0.25,
    max_stop_atr: float = 4.0,
    symbol: str | None = None,
    portfolio_risk_required: bool = False,
    portfolio_risk_result: Any | None = None,
) -> TradePlanValidationResult:
    """Validate a long trade plan.

    Required:
    - entry, stop and target_1 must exist
    - stop must be below entry
    - target_1 must be above entry
    - target_2, when present, must be above target_1
    - risk/reward must meet minimum threshold
    - stop distance must be within ATR thresholds when ATR is available
    - portfolio-risk context must pass when required
    """

    reasons: list[str] = []
    portfolio_risk_status = "NOT_REQUIRED"
    portfolio_risk_block_reason: str | None = None
    portfolio_risk_multiplier: float | None = None

    if portfolio_risk_required:
        portfolio_risk_reasons = _portfolio_risk_reasons(portfolio_risk_result, symbol)
        portfolio_risk_multiplier = _portfolio_multiplier_for_symbol(portfolio_risk_result, symbol)
        if portfolio_risk_reasons:
            portfolio_risk_status = "BLOCKED"
            portfolio_risk_block_reason = ",".join(portfolio_risk_reasons)
            if portfolio_risk_result is None:
                reasons.append("portfolio_risk_context_missing")
            else:
                reasons.append("portfolio_risk_blocked")
        else:
            portfolio_risk_status = "PASSED"
            if portfolio_risk_multiplier is None:
                portfolio_risk_multiplier = 1.0

    missing = []
    if _is_missing(entry_trigger):
        missing.append("entry_trigger")
    if _is_missing(stop_loss):
        missing.append("stop_loss")
    if _is_missing(target_1):
        missing.append("target_1")

    if missing:
        reasons.extend(f"missing_{name}" for name in missing)
        return TradePlanValidationResult(
            is_valid=False,
            reasons=reasons,
            portfolio_risk_status=portfolio_risk_status,
            portfolio_risk_block_reason=portfolio_risk_block_reason,
            portfolio_risk_multiplier=portfolio_risk_multiplier,
        )

    assert entry_trigger is not None
    assert stop_loss is not None
    assert target_1 is not None

    risk_per_share = entry_trigger - stop_loss
    reward_per_share = target_1 - entry_trigger

    if stop_loss >= entry_trigger:
        reasons.append("stop_loss_not_below_entry")
    if target_1 <= entry_trigger:
        reasons.append("target_1_not_above_entry")
    if target_2 is not None and target_2 <= target_1:
        reasons.append("target_2_not_above_target_1")

    risk_reward: float | None = None
    if risk_per_share <= 0:
        reasons.append("invalid_risk_per_share")
    elif reward_per_share <= 0:
        reasons.append("invalid_reward_per_share")
    else:
        risk_reward = reward_per_share / risk_per_share
        if risk_reward < min_risk_reward:
            reasons.append("risk_reward_below_minimum")

    stop_distance_atr: float | None = None
    if atr is not None and atr > 0 and risk_per_share > 0:
        stop_distance_atr = risk_per_share / atr
        if stop_distance_atr < min_stop_atr:
            reasons.append("stop_distance_too_tight")
        if stop_distance_atr > max_stop_atr:
            reasons.append("stop_distance_too_wide")

    return TradePlanValidationResult(
        is_valid=not reasons,
        reasons=reasons,
        risk_reward=_round_or_none(risk_reward, 4),
        risk_per_share=_round_or_none(risk_per_share, 4),
        reward_per_share=_round_or_none(reward_per_share, 4),
        stop_distance_atr=_round_or_none(stop_distance_atr, 4),
        portfolio_risk_status=portfolio_risk_status,
        portfolio_risk_block_reason=portfolio_risk_block_reason,
        portfolio_risk_multiplier=portfolio_risk_multiplier,
    )
