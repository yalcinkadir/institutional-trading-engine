"""
Cross-Asset Regime Layer for Decision Engine v3.

This module adds a macro/systemic risk view without making the model opaque.
It converts cross-asset evidence into a deterministic risk score and regime.

Primary inputs are deliberately accessible through ETF/proxy tickers:

- DXY / UUP proxy for USD pressure
- TLT proxy for long-duration bond stress
- HYG vs LQD proxy for credit appetite
- IWM vs QQQ proxy for participation / risk appetite
- GLD vs SPY proxy for defensive demand

The layer should not replace setup scoring. It acts as a higher-level context
filter that can reduce risk, activate defensive setups or block aggressive risk.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CrossAssetInput:
    symbol: str
    return_20d: float
    above_sma50: bool
    above_sma200: bool


@dataclass(frozen=True)
class CrossAssetRegime:
    regime: str
    risk_score: int
    risk_on_score: int
    risk_off_score: int
    warnings: tuple[str, ...]
    confirmations: tuple[str, ...]


def _spread(a: CrossAssetInput, b: CrossAssetInput) -> float:
    return round(a.return_20d - b.return_20d, 4)


def evaluate_cross_asset_regime(
    *,
    dollar: CrossAssetInput,
    long_bonds: CrossAssetInput,
    high_yield: CrossAssetInput,
    investment_grade: CrossAssetInput,
    small_caps: CrossAssetInput,
    growth: CrossAssetInput,
    gold: CrossAssetInput,
    equities: CrossAssetInput,
) -> CrossAssetRegime:
    warnings: list[str] = []
    confirmations: list[str] = []
    risk_off_score = 0
    risk_on_score = 0

    credit_spread_proxy = _spread(high_yield, investment_grade)
    small_vs_growth = _spread(small_caps, growth)
    gold_vs_equities = _spread(gold, equities)

    if dollar.return_20d > 0.03 and dollar.above_sma50:
        risk_off_score += 20
        warnings.append("strong_usd_pressure")
    else:
        risk_on_score += 8
        confirmations.append("usd_pressure_contained")

    if long_bonds.return_20d < -0.04 and not long_bonds.above_sma50:
        risk_off_score += 20
        warnings.append("duration_rate_stress")
    else:
        risk_on_score += 8
        confirmations.append("duration_stress_contained")

    if credit_spread_proxy < -0.02:
        risk_off_score += 25
        warnings.append("credit_risk_appetite_deteriorating")
    elif credit_spread_proxy > 0.01:
        risk_on_score += 20
        confirmations.append("credit_risk_appetite_supportive")

    if small_vs_growth < -0.03:
        risk_off_score += 15
        warnings.append("small_caps_underperform_growth")
    elif small_vs_growth > 0.01:
        risk_on_score += 15
        confirmations.append("small_caps_confirm_risk_appetite")

    if gold_vs_equities > 0.03:
        risk_off_score += 15
        warnings.append("defensive_gold_outperformance")
    elif gold_vs_equities < -0.02:
        risk_on_score += 10
        confirmations.append("equities_outperform_defensive_gold")

    if equities.above_sma50 and equities.above_sma200:
        risk_on_score += 20
        confirmations.append("equity_trend_supportive")
    elif not equities.above_sma50 and not equities.above_sma200:
        risk_off_score += 20
        warnings.append("equity_trend_broken")

    risk_score = max(0, min(100, 50 + risk_on_score - risk_off_score))

    if risk_off_score >= 55:
        regime = "cross_asset_risk_off"
    elif risk_on_score >= 55 and risk_off_score <= 25:
        regime = "cross_asset_risk_on"
    elif risk_off_score > risk_on_score:
        regime = "cross_asset_defensive"
    else:
        regime = "cross_asset_neutral"

    return CrossAssetRegime(
        regime=regime,
        risk_score=risk_score,
        risk_on_score=risk_on_score,
        risk_off_score=risk_off_score,
        warnings=tuple(warnings),
        confirmations=tuple(confirmations),
    )
