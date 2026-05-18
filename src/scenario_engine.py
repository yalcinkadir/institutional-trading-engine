"""
Scenario Engine.

The Scenario Engine evaluates how fragile the current decision environment is
under plausible macro and market shocks.

It does not forecast events. It stress-tests the current market context.

Supported scenario families:
- hot CPI / inflation shock
- bond selloff / rate shock
- VIX spike / volatility shock
- dollar shock
- growth crash
- credit stress
- liquidity shock
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class ScenarioType(str, Enum):
    HOT_CPI = "hot_cpi"
    BOND_SELLOFF = "bond_selloff"
    VIX_SPIKE = "vix_spike"
    DOLLAR_SHOCK = "dollar_shock"
    GROWTH_CRASH = "growth_crash"
    CREDIT_STRESS = "credit_stress"
    LIQUIDITY_SHOCK = "liquidity_shock"


@dataclass(frozen=True)
class ScenarioContext:
    current_macro_risk_score: float
    liquidity_stability_score: float
    breadth_score: float
    sector_rotation_offensive_score: float
    failure_risk_score: float
    portfolio_beta: float
    portfolio_correlation_score: float
    event_risk_score: float


@dataclass(frozen=True)
class ScenarioShock:
    scenario_type: ScenarioType
    severity: float
    description: str = ""


@dataclass(frozen=True)
class ScenarioImpact:
    scenario_type: str
    impact_score: int
    expected_pressure: str
    affected_layers: tuple[str, ...]
    recommended_action: str


@dataclass(frozen=True)
class ScenarioAssessment:
    scenario_risk_state: str
    aggregate_impact_score: int
    impacts: tuple[ScenarioImpact, ...]
    warnings: tuple[str, ...]
    recommended_actions: tuple[str, ...]


def _clamp(value: float, minimum: float = 0.0, maximum: float = 100.0) -> float:
    return max(minimum, min(maximum, value))


def _impact_for_scenario(context: ScenarioContext, shock: ScenarioShock) -> ScenarioImpact:
    severity = _clamp(shock.severity, 0.0, 1.0)
    affected_layers: list[str] = []
    score = 0.0

    if shock.scenario_type == ScenarioType.HOT_CPI:
        score = severity * (
            (100 - context.current_macro_risk_score) * 0.25
            + (100 - context.liquidity_stability_score) * 0.15
            + context.portfolio_beta * 18
            + context.event_risk_score * 0.25
        )
        affected_layers = ["rates", "real_yields", "growth", "volatility"]

    elif shock.scenario_type == ScenarioType.BOND_SELLOFF:
        score = severity * (
            (100 - context.current_macro_risk_score) * 0.25
            + context.portfolio_beta * 20
            + context.portfolio_correlation_score * 0.25
        )
        affected_layers = ["rates", "duration_assets", "growth", "portfolio_beta"]

    elif shock.scenario_type == ScenarioType.VIX_SPIKE:
        score = severity * (
            (100 - context.liquidity_stability_score) * 0.35
            + context.failure_risk_score * 0.30
            + context.portfolio_correlation_score * 0.20
        )
        affected_layers = ["volatility", "liquidity", "execution", "failure_patterns"]

    elif shock.scenario_type == ScenarioType.DOLLAR_SHOCK:
        score = severity * (
            (100 - context.current_macro_risk_score) * 0.20
            + context.portfolio_beta * 14
            + context.failure_risk_score * 0.20
        )
        affected_layers = ["fx", "commodities", "risk_assets", "macro"]

    elif shock.scenario_type == ScenarioType.GROWTH_CRASH:
        score = severity * (
            context.portfolio_beta * 24
            + context.portfolio_correlation_score * 0.35
            + (100 - context.breadth_score) * 0.25
            + context.failure_risk_score * 0.20
        )
        affected_layers = ["growth", "momentum", "portfolio_correlation", "breadth"]

    elif shock.scenario_type == ScenarioType.CREDIT_STRESS:
        score = severity * (
            (100 - context.current_macro_risk_score) * 0.30
            + (100 - context.liquidity_stability_score) * 0.25
            + context.failure_risk_score * 0.25
        )
        affected_layers = ["credit", "liquidity", "risk_appetite", "cyclicals"]

    elif shock.scenario_type == ScenarioType.LIQUIDITY_SHOCK:
        score = severity * (
            (100 - context.liquidity_stability_score) * 0.45
            + context.portfolio_correlation_score * 0.25
            + context.failure_risk_score * 0.25
        )
        affected_layers = ["liquidity", "execution", "slippage", "portfolio_heat"]

    impact = int(_clamp(score))

    if impact >= 70:
        pressure = "severe_pressure"
        action = "reduce_risk_or_hedge_before_scenario"
    elif impact >= 50:
        pressure = "high_pressure"
        action = "reduce_position_size_and_raise_thresholds"
    elif impact >= 30:
        pressure = "moderate_pressure"
        action = "avoid_marginal_setups"
    else:
        pressure = "contained_pressure"
        action = "normal_risk_protocol"

    return ScenarioImpact(
        scenario_type=shock.scenario_type.value,
        impact_score=impact,
        expected_pressure=pressure,
        affected_layers=tuple(affected_layers),
        recommended_action=action,
    )


def evaluate_scenarios(
    context: ScenarioContext,
    shocks: tuple[ScenarioShock, ...],
) -> ScenarioAssessment:
    impacts = tuple(_impact_for_scenario(context, shock) for shock in shocks)

    if not impacts:
        return ScenarioAssessment(
            scenario_risk_state="no_scenarios_defined",
            aggregate_impact_score=0,
            impacts=(),
            warnings=("no_scenario_shocks_provided",),
            recommended_actions=("define_relevant_macro_or_market_scenarios",),
        )

    aggregate = int(round(sum(item.impact_score for item in impacts) / len(impacts)))
    warnings: list[str] = []
    actions: list[str] = []

    for impact in impacts:
        if impact.impact_score >= 50:
            warnings.append(f"scenario_pressure:{impact.scenario_type}:{impact.impact_score}")
        actions.append(impact.recommended_action)

    if aggregate >= 70:
        state = "scenario_risk_extreme"
        actions.append("block_new_aggressive_risk")
    elif aggregate >= 50:
        state = "scenario_risk_high"
        actions.append("reduce_portfolio_heat")
    elif aggregate >= 30:
        state = "scenario_risk_moderate"
        actions.append("increase_selectivity")
    else:
        state = "scenario_risk_contained"

    return ScenarioAssessment(
        scenario_risk_state=state,
        aggregate_impact_score=aggregate,
        impacts=impacts,
        warnings=tuple(dict.fromkeys(warnings)),
        recommended_actions=tuple(dict.fromkeys(actions)),
    )
