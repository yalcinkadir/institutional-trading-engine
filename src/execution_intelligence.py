"""
Execution Intelligence Engine.

Good analysis is not enough. A strong system must also evaluate whether a setup
can be executed efficiently under current volatility, liquidity and risk
conditions.

This module is deliberately deterministic, explainable and extensible.
It evaluates:
- entry timing quality
- ATR-normalized stop distance
- liquidity-aware sizing
- slippage risk
- partial exit planning
- volatility-adjusted scaling
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ExecutionInput:
    symbol: str
    current_price: float
    sma50: float
    atr14: float
    relative_volume: float
    intraday_range_percent: float
    liquidity_score: float
    volatility_stability_score: float
    failure_risk_score: float
    event_risk_active: bool
    spread_percent: float
    risk_tier: str


@dataclass(frozen=True)
class ExecutionPlan:
    symbol: str
    execution_state: str
    entry_quality_score: int
    stop_distance_atr: float
    stop_price: float
    position_size_multiplier: float
    estimated_slippage_percent: float
    partial_exit_plan: tuple[str, ...]
    warnings: tuple[str, ...]
    confirmations: tuple[str, ...]


RISK_TIER_BASE_SIZE = {
    "tier_1": 1.0,
    "tier_2": 0.5,
    "tier_3": 0.25,
    "no_trade": 0.0,
}


def _clamp(value: float, minimum: float, maximum: float) -> float:
    return max(minimum, min(maximum, value))


def _distance_from_sma50_percent(current_price: float, sma50: float) -> float:
    if current_price == 0:
        return 0.0
    return ((current_price / sma50) - 1) * 100


def calculate_entry_quality(data: ExecutionInput) -> tuple[int, tuple[str, ...], tuple[str, ...]]:
    warnings: list[str] = []
    confirmations: list[str] = []
    score = 50

    distance = _distance_from_sma50_percent(data.current_price, data.sma50)

    if 0 <= distance <= 6:
        score += 15
        confirmations.append("efficient_distance_from_sma50")
    elif distance > 12:
        score -= 20
        warnings.append("extended_from_sma50")
    elif distance < -5:
        score -= 10
        warnings.append("below_sma50_entry_risk")

    if data.relative_volume >= 1.3:
        score += 12
        confirmations.append("volume_confirms_entry")
    elif data.relative_volume < 0.8:
        score -= 10
        warnings.append("weak_volume_confirmation")

    if data.intraday_range_percent <= 2.0:
        score += 8
        confirmations.append("intraday_structure_stable")
    elif data.intraday_range_percent >= 4.5:
        score -= 12
        warnings.append("intraday_range_unstable")

    if data.volatility_stability_score >= 70:
        score += 10
        confirmations.append("volatility_context_supportive")
    elif data.volatility_stability_score <= 40:
        score -= 15
        warnings.append("volatility_context_fragile")

    if data.failure_risk_score >= 60:
        score -= 18
        warnings.append("failure_risk_elevated")

    if data.event_risk_active:
        score -= 10
        warnings.append("event_risk_active")

    score = int(_clamp(score, 0, 100))
    return score, tuple(warnings), tuple(confirmations)


def calculate_stop_distance_atr(data: ExecutionInput) -> float:
    base = 1.6

    if data.volatility_stability_score <= 40:
        base += 0.4
    elif data.volatility_stability_score >= 75:
        base -= 0.2

    if data.failure_risk_score >= 60:
        base += 0.25

    if data.event_risk_active:
        base += 0.25

    if data.liquidity_score <= 40:
        base += 0.25

    return round(_clamp(base, 1.0, 2.8), 2)


def estimate_slippage_percent(data: ExecutionInput) -> float:
    slippage = data.spread_percent

    if data.liquidity_score <= 40:
        slippage += 0.15
    elif data.liquidity_score >= 75:
        slippage -= 0.03

    if data.intraday_range_percent >= 4.5:
        slippage += 0.10

    if data.event_risk_active:
        slippage += 0.08

    return round(_clamp(slippage, 0.0, 1.5), 4)


def calculate_position_size_multiplier(data: ExecutionInput, entry_quality_score: int) -> float:
    size = RISK_TIER_BASE_SIZE.get(data.risk_tier, 0.0)

    if entry_quality_score < 40:
        size *= 0.25
    elif entry_quality_score < 60:
        size *= 0.5

    if data.liquidity_score <= 40:
        size *= 0.5

    if data.volatility_stability_score <= 40:
        size *= 0.5

    if data.failure_risk_score >= 70:
        size *= 0.25
    elif data.failure_risk_score >= 50:
        size *= 0.5

    if data.event_risk_active:
        size *= 0.5

    return round(_clamp(size, 0.0, 1.0), 4)


def build_partial_exit_plan(data: ExecutionInput, stop_distance_atr: float) -> tuple[str, ...]:
    if data.risk_tier == "no_trade":
        return ("no_position",)

    first_target = round(stop_distance_atr * 1.0, 2)
    second_target = round(stop_distance_atr * 2.0, 2)

    plan = [
        f"take_25_percent_at_{first_target}R",
        f"take_25_percent_at_{second_target}R",
        "trail_remaining_with_sma20_or_atr",
    ]

    if data.event_risk_active:
        plan.insert(0, "avoid_new_entry_or_reduce_before_event")

    if data.failure_risk_score >= 60:
        plan.append("tighten_management_due_to_failure_risk")

    return tuple(plan)


def build_execution_plan(data: ExecutionInput) -> ExecutionPlan:
    entry_score, warnings, confirmations = calculate_entry_quality(data)
    stop_distance_atr = calculate_stop_distance_atr(data)
    stop_price = round(data.current_price - (data.atr14 * stop_distance_atr), 4)
    slippage = estimate_slippage_percent(data)
    size = calculate_position_size_multiplier(data, entry_score)
    partial_exit_plan = build_partial_exit_plan(data, stop_distance_atr)

    if data.risk_tier == "no_trade" or size == 0:
        execution_state = "do_not_execute"
    elif entry_score >= 75 and size >= 0.75:
        execution_state = "execution_quality_high"
    elif entry_score >= 55:
        execution_state = "execution_quality_selective"
    elif entry_score >= 40:
        execution_state = "execution_quality_weak"
    else:
        execution_state = "avoid_execution"

    return ExecutionPlan(
        symbol=data.symbol,
        execution_state=execution_state,
        entry_quality_score=entry_score,
        stop_distance_atr=stop_distance_atr,
        stop_price=stop_price,
        position_size_multiplier=size,
        estimated_slippage_percent=slippage,
        partial_exit_plan=partial_exit_plan,
        warnings=warnings,
        confirmations=confirmations,
    )
