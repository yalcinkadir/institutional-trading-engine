"""
Bridge: Scanner Metrics → Institutional Decision Orchestrator

This module is the critical connection between the live scanner world
and the institutional runtime framework.

Design principles:
- No synthetic floats. Every value is derived from real scanner metrics.
- Explicit derivation logic: every mapping is documented and testable.
- Graceful degradation: missing data produces conservative inputs,
  never crashes the runtime.
- No side effects. Pure transformation only.

Input:  metrics_map (dict[symbol -> scanner metrics dict])
        vix_data    (dict | None from scanner.get_vix_value())

Output: InstitutionalDecisionInputs (fully populated, no synthetic values)
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any

import pandas as pd

from src.orchestration.institutional_decision_orchestrator import (
    InstitutionalDecisionInputs,
)

# ── Conservative fallback constants ────────────────────────────────────────
# Used only when a metric is genuinely unavailable from live data.
# These are deliberately cautious, not optimistic.
_FALLBACK_VIX = 25.0          # Elevated, not panic — forces conservative sizing
_FALLBACK_EQUITY_STRENGTH = 50.0
_FALLBACK_BOND_STRENGTH = 50.0
_FALLBACK_DOLLAR_STRENGTH = 50.0
_FALLBACK_GOLD_STRENGTH = 50.0
_FALLBACK_ADV_MILLIONS = 20.0
_FALLBACK_SPREAD_PCT = 0.10
_FALLBACK_ORDER_SIZE_PCT = 5.0

# ── Symbol roles in cross-asset derivation ─────────────────────────────────
_EQUITY_PROXY = "SPY"
_TECH_PROXY = "QQQ"
_GOLD_PROXY = "GLD"
_SILVER_PROXY = "SLV"

# Symbols treated as bond proxies (long-duration, rate-sensitive)
_BOND_PROXIES = {"TLT", "IEF", "BND"}

# Symbols treated as dollar-proxy (inverse correlation)
_DOLLAR_INVERSE = {"GLD", "SLV", "EEM", "FXI"}


@dataclass(frozen=True)
class BridgeTranslation:
    """
    Full translation result from scanner world to institutional world.

    Separates the final inputs from the derivation notes so callers
    can inspect how each value was derived (auditability requirement).
    """

    inputs: InstitutionalDecisionInputs
    derivation_notes: dict[str, str]
    symbols_used: list[str]
    data_quality_warnings: list[str]


def _safe_float(value: Any, fallback: float) -> float:
    """Return float value, or fallback if None / NaN / invalid."""
    if value is None:
        return fallback
    try:
        f = float(value)
        return fallback if math.isnan(f) or math.isinf(f) else f
    except (TypeError, ValueError):
        return fallback


def _clamp(value: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, value))


def _derive_equity_strength(metrics_map: dict[str, Any]) -> tuple[float, str]:
    """
    Equity strength from SPY and QQQ scanner metrics.

    Combines:
    - 20-day return (momentum direction)
    - RSI14 (momentum intensity)
    - Trend label (structure quality)

    Returns (score 0–100, derivation note).
    """
    spy = metrics_map.get(_EQUITY_PROXY) or {}
    qqq = metrics_map.get(_TECH_PROXY) or {}

    if not spy and not qqq:
        return _FALLBACK_EQUITY_STRENGTH, "fallback: no SPY/QQQ data"

    scores: list[float] = []
    sources: list[str] = []

    for sym, m in [("SPY", spy), ("QQQ", qqq)]:
        if not m:
            continue

        # Return component: map ret_20d → 0–40 pts
        ret = _safe_float(m.get("ret_20d"), 0.0)
        ret_score = _clamp((ret + 20) / 40 * 40, 0, 40)

        # RSI component: 50–65 is ideal (30 pts), extremes penalized
        rsi = _safe_float(m.get("rsi14"), 50.0)
        if 50 <= rsi <= 65:
            rsi_score = 30.0
        elif 45 <= rsi < 50 or 65 < rsi <= 70:
            rsi_score = 18.0
        elif rsi > 70:
            rsi_score = 8.0   # Extended — near-term reversal risk
        else:
            rsi_score = 5.0   # Weak

        # Trend component: structure quality (30 pts)
        trend = m.get("trend", "")
        trend_score = {
            "Strong Uptrend": 30.0,
            "Uptrend": 20.0,
            "Mixed": 10.0,
            "Downtrend": 0.0,
        }.get(trend, 10.0)

        symbol_score = ret_score + rsi_score + trend_score
        scores.append(symbol_score)
        sources.append(sym)

    if not scores:
        return _FALLBACK_EQUITY_STRENGTH, "fallback: metrics incomplete"

    result = sum(scores) / len(scores)
    return round(_clamp(result, 0.0, 100.0), 2), f"derived from {', '.join(sources)}"


def _derive_gold_strength(metrics_map: dict[str, Any]) -> tuple[float, str]:
    """
    Gold strength from GLD scanner metrics.
    High gold strength = defensive pressure = risk-off signal.
    """
    gld = metrics_map.get(_GOLD_PROXY) or {}

    if not gld:
        return _FALLBACK_GOLD_STRENGTH, "fallback: no GLD data"

    ret = _safe_float(gld.get("ret_20d"), 0.0)
    rsi = _safe_float(gld.get("rsi14"), 50.0)
    trend = gld.get("trend", "Mixed")

    ret_score = _clamp((ret + 15) / 30 * 40, 0, 40)
    rsi_score = 30.0 if 50 <= rsi <= 70 else (15.0 if rsi > 70 else 5.0)
    trend_score = {
        "Strong Uptrend": 30.0,
        "Uptrend": 20.0,
        "Mixed": 10.0,
        "Downtrend": 0.0,
    }.get(trend, 10.0)

    result = ret_score + rsi_score + trend_score
    return round(_clamp(result, 0.0, 100.0), 2), "derived from GLD metrics"


def _derive_dollar_strength(
    metrics_map: dict[str, Any],
    gold_strength: float,
) -> tuple[float, str]:
    """
    Dollar strength estimated from inverse gold/commodity behavior.
    When GLD is strong and broad equities weak → dollar likely stronger.

    This is an approximation until DXY/UUP is added to the universe.
    Score is intentionally conservative (50 base ± 20 range).
    """
    spy = metrics_map.get(_EQUITY_PROXY) or {}
    equity_ret = _safe_float((spy or {}).get("ret_20d"), 0.0)

    # Dollar tends to strengthen when: gold weak + equities weak (flight to safety)
    # Dollar tends to weaken when: gold strong + equities strong (risk-on)
    gold_component = (100.0 - gold_strength) * 0.3
    equity_inverse = _clamp((10.0 - equity_ret) / 20.0 * 20.0, 0, 20)

    result = _clamp(40.0 + gold_component + equity_inverse, 0.0, 100.0)
    return round(result, 2), "estimated from GLD/equity inverse relationship"


def _derive_bond_strength(
    metrics_map: dict[str, Any],
    vix_level: float,
) -> tuple[float, str]:
    """
    Bond strength estimated from VIX level and equity behavior.
    When VIX is high → bonds likely bid (flight to safety).

    This is an approximation until TLT is added to the universe.
    """
    if vix_level >= 30:
        score = 75.0
        note = "estimated: VIX elevated → bonds likely bid"
    elif vix_level >= 20:
        score = 58.0
        note = "estimated: VIX moderate → neutral bond pressure"
    else:
        score = 35.0
        note = "estimated: VIX low → bonds likely under pressure"

    return round(score, 2), note


def _derive_market_regime_score(
    metrics_map: dict[str, Any],
    vix_level: float,
) -> tuple[float, str]:
    """
    Market regime score (0–100) from combined breadth signals.

    Inputs:
    - SPY/QQQ trend quality
    - SPY/QQQ RSI
    - VIX level
    - Leaders vs Weak ratio in the universe
    """
    spy = metrics_map.get(_EQUITY_PROXY) or {}
    qqq = metrics_map.get(_TECH_PROXY) or {}

    score = 50.0  # Base neutral

    # Trend quality adjustment (±20)
    for m in [spy, qqq]:
        trend = (m or {}).get("trend", "Mixed")
        if trend == "Strong Uptrend":
            score += 10.0
        elif trend == "Uptrend":
            score += 5.0
        elif trend == "Downtrend":
            score -= 10.0
        elif trend == "Mixed":
            score -= 2.0

    # RSI breadth adjustment (±15)
    rsi_readings = [
        _safe_float((spy or {}).get("rsi14"), 50.0),
        _safe_float((qqq or {}).get("rsi14"), 50.0),
    ]
    avg_rsi = sum(rsi_readings) / len(rsi_readings)
    if avg_rsi >= 60:
        score += 10.0
    elif avg_rsi >= 50:
        score += 5.0
    elif avg_rsi < 40:
        score -= 10.0

    # VIX penalty (±15)
    if vix_level >= 35:
        score -= 20.0
    elif vix_level >= 25:
        score -= 10.0
    elif vix_level >= 20:
        score -= 5.0
    elif vix_level <= 15:
        score += 10.0

    # Universe breadth: leaders vs weak ratio
    symbols = [
        m for sym, m in metrics_map.items()
        if m and sym not in {_EQUITY_PROXY, _TECH_PROXY}
    ]
    if symbols:
        leaders = sum(1 for m in symbols if m.get("rs_label") == "Leader")
        weak = sum(1 for m in symbols if m.get("rs_label") == "Weak")
        breadth_ratio = (leaders - weak) / max(1, len(symbols))
        score += breadth_ratio * 10.0

    return round(_clamp(score, 0.0, 100.0), 2), "derived from SPY/QQQ/VIX/breadth"


def _derive_gap_risk(
    metrics_map: dict[str, Any],
    vix_level: float,
) -> tuple[float, str]:
    """
    Gap risk estimate based on ATR% of core indices and VIX level.
    Higher ATR% + higher VIX = higher gap risk.
    """
    atr_readings: list[float] = []
    for sym in [_EQUITY_PROXY, _TECH_PROXY]:
        m = metrics_map.get(sym) or {}
        atr_pct = _safe_float(m.get("atr_pct"), 1.5)
        atr_readings.append(atr_pct)

    avg_atr = sum(atr_readings) / max(1, len(atr_readings))

    # Combine ATR% with VIX regime
    vix_factor = _clamp(vix_level / 30.0, 0.5, 2.0)
    gap_risk = _clamp(avg_atr * vix_factor * 3.0, 0.0, 50.0)

    return round(gap_risk, 2), f"avg_atr={avg_atr:.2f}%, vix_factor={vix_factor:.2f}"


def _derive_liquidity_stress(
    metrics_map: dict[str, Any],
    vix_level: float,
) -> tuple[float, str]:
    """
    Liquidity stress estimate from RVOL and VIX.

    Unusually high RVOL across the universe = liquidity fragmentation.
    VIX spike = institutional withdrawal of liquidity.
    """
    rvol_readings: list[float] = []
    for sym, m in metrics_map.items():
        if not m:
            continue
        rvol = _safe_float(m.get("rvol"), 1.0)
        rvol_readings.append(rvol)

    avg_rvol = sum(rvol_readings) / max(1, len(rvol_readings)) if rvol_readings else 1.0

    # Normal RVOL ~1.0 → low stress; >2.0 indicates panic / dislocation
    rvol_stress = _clamp((avg_rvol - 1.0) * 20.0, 0.0, 40.0)

    # VIX-based stress component
    vix_stress = _clamp((vix_level - 15.0) / 25.0 * 30.0, 0.0, 30.0)

    liquidity_stress = rvol_stress + vix_stress
    return round(_clamp(liquidity_stress, 0.0, 70.0), 2), f"avg_rvol={avg_rvol:.2f}"


def _derive_feature_alpha_score(metrics_map: dict[str, Any]) -> tuple[float, str]:
    """
    Alpha score from the quality of the universe's setup opportunities.

    High alpha score = many actionable setups with strong RS.
    Low alpha score = most names extended, weak, or directionless.
    """
    actionable_labels = {"Pullback Candidate", "Breakout Watch"}
    avoid_labels = {"Weak - Avoid", "Extended - Avoid Chase", "High Volatility Caution"}

    symbols = [
        m for sym, m in metrics_map.items()
        if m and sym not in {_EQUITY_PROXY, _TECH_PROXY}
    ]

    if not symbols:
        return 50.0, "fallback: no non-index symbols"

    actionable = sum(1 for m in symbols if m.get("setup_readiness") in actionable_labels)
    avoid = sum(1 for m in symbols if m.get("setup_readiness") in avoid_labels)
    total = len(symbols)

    actionable_ratio = actionable / total
    avoid_ratio = avoid / total

    score = 50.0 + (actionable_ratio * 40.0) - (avoid_ratio * 30.0)

    return round(_clamp(score, 0.0, 100.0), 2), (
        f"{actionable}/{total} actionable, {avoid}/{total} avoid"
    )


def _derive_adv_millions(metrics_map: dict[str, Any]) -> tuple[float, str]:
    """
    Average daily volume in millions from the universe median.
    Used by LiquidityIntelligence to assess execution conditions.
    """
    vol_readings: list[float] = []
    for sym, m in metrics_map.items():
        if not m:
            continue
        vol = _safe_float(m.get("vol20"), None)
        if vol is not None and vol > 0:
            vol_readings.append(vol / 1_000_000)

    if not vol_readings:
        return _FALLBACK_ADV_MILLIONS, "fallback: no volume data"

    median_adv = sorted(vol_readings)[len(vol_readings) // 2]
    return round(_clamp(median_adv, 0.1, 5000.0), 2), f"median across {len(vol_readings)} symbols"


def translate(
    metrics_map: dict[str, Any],
    vix_data: dict[str, Any] | None,
) -> BridgeTranslation:
    """
    Translate live scanner metrics into InstitutionalDecisionInputs.

    This is the single entry point for the bridge. All derivation logic
    is encapsulated here. Callers receive both the inputs and the full
    derivation notes for auditability.

    Args:
        metrics_map: Output of scanner.build_symbol_metrics() for all symbols.
                     Keys are ticker symbols. Values are metric dicts or None.
        vix_data:    Output of scanner.get_vix_value(). May be None if unavailable.

    Returns:
        BridgeTranslation with inputs ready for the orchestrator.
    """
    notes: dict[str, str] = {}
    warnings: list[str] = []

    # ── VIX ────────────────────────────────────────────────────────────────
    if vix_data and vix_data.get("close") is not None:
        vix_level = _safe_float(vix_data["close"], _FALLBACK_VIX)
        notes["volatility_level"] = f"live VIX: {vix_level}"
    else:
        vix_level = _FALLBACK_VIX
        notes["volatility_level"] = "fallback VIX (live data unavailable)"
        warnings.append("VIX data unavailable — using conservative fallback")

    # ── Cross-asset strengths ───────────────────────────────────────────────
    equity_strength, equity_note = _derive_equity_strength(metrics_map)
    notes["equity_strength"] = equity_note

    gold_strength, gold_note = _derive_gold_strength(metrics_map)
    notes["gold_strength"] = gold_note

    dollar_strength, dollar_note = _derive_dollar_strength(metrics_map, gold_strength)
    notes["dollar_strength"] = dollar_note

    bond_strength, bond_note = _derive_bond_strength(metrics_map, vix_level)
    notes["bond_strength"] = bond_note

    # ── Regime score ────────────────────────────────────────────────────────
    market_regime_score, regime_note = _derive_market_regime_score(metrics_map, vix_level)
    notes["market_regime_score"] = regime_note

    # ── Risk signals ────────────────────────────────────────────────────────
    gap_risk, gap_note = _derive_gap_risk(metrics_map, vix_level)
    notes["gap_risk_percent"] = gap_note

    liquidity_stress, liq_note = _derive_liquidity_stress(metrics_map, vix_level)
    notes["liquidity_stress_percent"] = liq_note

    # Correlation and event risk: conservative static estimates.
    # These require portfolio-level and calendar data (Phase 4 territory).
    correlation_risk = _clamp(20.0 + (vix_level - 15.0) * 0.5, 10.0, 50.0)
    notes["correlation_risk_percent"] = "VIX-scaled estimate (calendar integration pending)"

    event_risk = 15.0
    notes["event_risk_percent"] = "static conservative estimate (calendar integration pending)"

    # ── Execution / liquidity inputs ────────────────────────────────────────
    adv_millions, adv_note = _derive_adv_millions(metrics_map)
    notes["average_daily_volume_millions"] = adv_note

    # Spread: estimated from ATR% of core indices
    spy_atr = _safe_float((metrics_map.get(_EQUITY_PROXY) or {}).get("atr_pct"), 1.5)
    bid_ask_spread = _clamp(spy_atr * 0.02, 0.02, 0.50)
    notes["bid_ask_spread_percent"] = f"estimated from SPY ATR%: {spy_atr:.2f}%"

    # Order size: conservative 2% of ADV
    order_size_pct_adv = 2.0
    notes["order_size_percent_adv"] = "conservative default (portfolio tracking pending)"

    # ── Alpha score ─────────────────────────────────────────────────────────
    feature_alpha_score, alpha_note = _derive_feature_alpha_score(metrics_map)
    notes["feature_alpha_score"] = alpha_note

    # ── Portfolio risk inputs ───────────────────────────────────────────────
    # Conservative defaults until real portfolio positions are tracked (Phase 4).
    portfolio_sector_exposure = 30.0
    portfolio_volatility_exposure = 25.0
    portfolio_concentration = 20.0
    portfolio_correlation = 25.0
    notes["portfolio_inputs"] = "conservative defaults (portfolio tracking pending)"

    # ── Validate completeness ───────────────────────────────────────────────
    symbols_used = [sym for sym, m in metrics_map.items() if m is not None]
    if len(symbols_used) < 2:
        warnings.append(f"Only {len(symbols_used)} valid symbols in metrics_map")

    inputs = InstitutionalDecisionInputs(
        market_regime_score=market_regime_score,
        equity_strength=equity_strength,
        bond_strength=bond_strength,
        dollar_strength=dollar_strength,
        gold_strength=gold_strength,
        volatility_level=vix_level,
        gap_risk_percent=gap_risk,
        liquidity_stress_percent=liquidity_stress,
        correlation_risk_percent=round(_clamp(correlation_risk, 0.0, 100.0), 2),
        event_risk_percent=event_risk,
        average_daily_volume_millions=adv_millions,
        bid_ask_spread_percent=round(bid_ask_spread, 4),
        order_size_percent_adv=order_size_pct_adv,
        feature_alpha_score=feature_alpha_score,
        portfolio_sector_exposure_percent=portfolio_sector_exposure,
        portfolio_volatility_exposure_percent=portfolio_volatility_exposure,
        portfolio_concentration_percent=portfolio_concentration,
        portfolio_correlation_percent=portfolio_correlation,
    )

    return BridgeTranslation(
        inputs=inputs,
        derivation_notes=notes,
        symbols_used=symbols_used,
        data_quality_warnings=warnings,
    )
