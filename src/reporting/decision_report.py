"""
Decision Report Builder.

Builds the institutional decision report from market regime and screener data.

Important integrations:
- Data quality degradation reduces confidence instead of causing a hard override.
- Historical expectancy profiles are fed back into setup scoring before ranking.

The expectancy integration closes the loop:

signals → lifecycle → outcomes → expectancy_r → future scoring
"""

from __future__ import annotations

from pathlib import Path

from src.decision_engine import (
    Decision,
    MarketContext,
    MarketState,
    SetupCandidate,
    SetupType,
    detect_hard_overrides,
    get_allowed_setups,
    rank_candidates,
)
from src.scoring.expectancy_adjuster import (
    DEFAULT_OUTCOME_HISTORY,
    apply_expectancy_to_score,
    default_entry_type_for_setup,
    find_expectancy_adjustment,
)


def _map_regime_to_market_state(
    regime: str,
    market_health_score: int | float | str,
) -> MarketState:
    regime_normalized = (
        str(regime).strip().lower().replace("-", "_").replace(" ", "_")
    )

    # Strip VIX-missing suffix if present (e.g. "Bullish (VIX missing)")
    for suffix in (" (vix_missing)", " (vix missing)"):
        if regime_normalized.endswith(suffix):
            regime_normalized = regime_normalized[: -len(suffix)]

    if regime_normalized in {"strong_bullish", "bullish"}:
        return MarketState.LOW_VOL_BULL
    if regime_normalized in {"defensive", "risk_off"}:
        return MarketState.RISK_OFF
    if regime_normalized in {"neutral"}:
        return MarketState.NEUTRAL

    try:
        score = float(market_health_score)
    except (TypeError, ValueError):
        return MarketState.NEUTRAL

    if score >= 75:
        return MarketState.LOW_VOL_BULL
    if score >= 55:
        return MarketState.NEUTRAL
    return MarketState.RISK_OFF


def _build_market_context(market_regime: dict) -> tuple[MarketContext, bool]:
    """
    Build market context plus a data-quality flag.

    Returns:
        tuple[
            MarketContext,
            bool  # data_quality_ok
        ]
    """
    market_state = _map_regime_to_market_state(
        market_regime.get("regime", "Unknown"),
        market_regime.get("market_health_score", "DATA_UNAVAILABLE"),
    )

    breadth = market_regime.get("breadth", {}) or {}
    symbols = market_regime.get("symbols", {}) or {}
    vix_snapshot = symbols.get("VIX", {}) or {}

    breadth_percent = float(breadth.get("breadth_percent", 50) or 50)
    vix_close = float(vix_snapshot.get("close", 20) or 20)

    breadth_collapse = breadth_percent < 35

    # Corrected liquidity_stress logic.
    #
    # OLD (buggy):
    #   liquidity_stress = market_regime.get("data_status") != "LIVE"
    #
    # This fired on every run because the Free Polygon tier frequently
    # operates in PARTIAL mode (e.g. VIX unavailable), causing permanent
    # hard overrides and blocking all recommendations.
    #
    # NEW:
    # liquidity_stress only reflects genuine market stress.
    liquidity_stress = (vix_close >= 30) or (breadth_percent < 25)

    volatility_stress = vix_close >= 25

    if volatility_stress and market_state == MarketState.LOW_VOL_BULL:
        market_state = MarketState.HIGH_VOL_TRANSITION

    if vix_close >= 35:
        market_state = MarketState.PANIC_DISLOCATION

    # Data quality affects confidence/sizing, not hard overrides.
    data_quality_ok = market_regime.get("data_status") == "LIVE"

    context = MarketContext(
        market_state=market_state,
        breadth_collapse=breadth_collapse,
        liquidity_stress=liquidity_stress,
        failed_breakout_cluster=False,
        max_portfolio_heat=(
            0.5
            if market_state
            in {MarketState.RISK_OFF, MarketState.HIGH_VOL_TRANSITION}
            else 1.0
        ),
    )

    return context, data_quality_ok


def _candidate_for_symbol(
    symbol: str,
    index: int,
    context: MarketContext,
    data_quality_ok: bool,
    outcome_history_path: str | Path = DEFAULT_OUTCOME_HISTORY,
) -> tuple[SetupCandidate, dict]:
    """
    Build report candidate and apply historical expectancy adjustment.

    The candidate remains a normal Decision Engine candidate, but its setup_score
    is adjusted by lifecycle-aware historical evidence where available.
    """
    preferred_setup = {
        MarketState.LOW_VOL_BULL: SetupType.MOMENTUM_BREAKOUT,
        MarketState.HIGH_VOL_TRANSITION: SetupType.PULLBACK_CONTINUATION,
        MarketState.RISK_OFF: SetupType.DEFENSIVE_ROTATION,
        MarketState.PANIC_DISLOCATION: SetupType.REVERSAL_ASYMMETRY,
        MarketState.NEUTRAL: SetupType.PULLBACK_CONTINUATION,
    }[context.market_state]

    base_setup_score = max(55, 82 - index * 3)
    regime_alignment = max(0.50, 0.82 - index * 0.04)
    asymmetry_score = max(0.50, 0.72 - index * 0.03)

    # Full confidence when all feeds live; reduced (but not blocking) when partial
    data_confidence = 0.85 if data_quality_ok else 0.65

    entry_type = default_entry_type_for_setup(preferred_setup.value)
    adjustment = find_expectancy_adjustment(
        setup_type=preferred_setup.value,
        market_state=context.market_state.value,
        entry_type=entry_type,
        outcome_history_path=outcome_history_path,
    )
    adjusted_setup_score = apply_expectancy_to_score(base_setup_score, adjustment)

    # Positive expectancy should not compensate for poor data quality too much.
    # Negative expectancy remains fully effective.
    if not data_quality_ok and adjustment.score_delta > 0:
        adjusted_setup_score = base_setup_score
        adjustment_note = "positive_expectancy_ignored_due_to_partial_data"
    else:
        adjustment_note = adjustment.reason

    candidate = SetupCandidate(
        symbol=symbol,
        setup_type=preferred_setup,
        setup_score=adjusted_setup_score,
        regime_alignment=regime_alignment,
        asymmetry_score=asymmetry_score,
        data_confidence=data_confidence,
    )

    meta = {
        "base_setup_score": base_setup_score,
        "expectancy_adjusted_score": adjusted_setup_score,
        "expectancy_score_delta": round(adjusted_setup_score - base_setup_score, 2),
        "expectancy_size_multiplier": adjustment.size_multiplier,
        "expectancy_profile_key": adjustment.profile_key,
        "expectancy_source": adjustment.source,
        "expectancy_sample_size": adjustment.sample_size,
        "expectancy_win_rate": adjustment.win_rate,
        "expectancy_r": adjustment.expectancy_r,
        "expectancy_recommendation": adjustment.recommendation,
        "expectancy_reason": adjustment_note,
        "entry_type_assumption": entry_type,
    }

    return candidate, meta


def build_decision_report(
    market_regime: dict,
    screener: dict,
    outcome_history_path: str | Path = DEFAULT_OUTCOME_HISTORY,
) -> dict:
    context, data_quality_ok = _build_market_context(market_regime)
    allowed_setups = get_allowed_setups(context.market_state)
    hard_overrides = detect_hard_overrides(context)

    candidate_pairs = [
        _candidate_for_symbol(
            symbol,
            index,
            context,
            data_quality_ok,
            outcome_history_path=outcome_history_path,
        )
        for index, symbol in enumerate(screener.get("watchlist", []))
    ]
    candidates = [candidate for candidate, _meta in candidate_pairs]
    meta_by_symbol = {candidate.symbol: meta for candidate, meta in candidate_pairs}

    ranked = rank_candidates(context, candidates)

    decisions = []
    for candidate, result in ranked:
        meta = meta_by_symbol.get(candidate.symbol, {})
        adjusted_size = round(
            result.position_size_multiplier
            * float(meta.get("expectancy_size_multiplier", 1.0)),
            4,
        )

        notes = list(result.notes)
        expectancy_delta = float(meta.get("expectancy_score_delta", 0.0))
        if expectancy_delta != 0:
            notes.append(
                "expectancy_adjustment: "
                f"{expectancy_delta:+.1f} score, "
                f"size×{meta.get('expectancy_size_multiplier')} "
                f"({meta.get('expectancy_reason')})"
            )

        decisions.append(
            {
                "symbol": candidate.symbol,
                "setup_type": candidate.setup_type.value,
                "decision": result.decision.value,
                "risk_tier": result.risk_tier,
                "position_size_multiplier": adjusted_size,
                "base_position_size_multiplier": result.position_size_multiplier,
                "setup_score": candidate.setup_score,
                "base_setup_score": meta.get("base_setup_score", candidate.setup_score),
                "regime_alignment": round(candidate.regime_alignment, 2),
                "asymmetry_score": round(candidate.asymmetry_score, 2),
                "data_confidence": round(candidate.data_confidence, 2),
                "blocked_reasons": list(result.blocked_reasons),
                "notes": notes,
                "expectancy": {
                    "profile_key": meta.get("expectancy_profile_key"),
                    "source": meta.get("expectancy_source"),
                    "sample_size": meta.get("expectancy_sample_size"),
                    "win_rate": meta.get("expectancy_win_rate"),
                    "expectancy_r": meta.get("expectancy_r"),
                    "score_delta": meta.get("expectancy_score_delta"),
                    "size_multiplier": meta.get("expectancy_size_multiplier"),
                    "recommendation": meta.get("expectancy_recommendation"),
                    "reason": meta.get("expectancy_reason"),
                    "entry_type_assumption": meta.get("entry_type_assumption"),
                },
            }
        )

    approved_count = sum(
        1
        for item in decisions
        if item["decision"] in {Decision.APPROVED.value, Decision.REDUCED_SIZE.value}
    )
    blocked_count = sum(
        1
        for item in decisions
        if item["decision"] in {Decision.BLOCKED.value, Decision.NO_TRADE.value}
    )

    if hard_overrides:
        summary = (
            "Hard risk override active. "
            "The report should prioritize defense and avoid new aggressive exposure."
        )
    elif approved_count == 0:
        summary = (
            "No high-quality asymmetric opportunity found. "
            "No-trade or watch mode is preferred."
        )
    elif context.market_state == MarketState.HIGH_VOL_TRANSITION:
        summary = (
            "Opportunities exist, but high-volatility transition "
            "requires reduced position sizing."
        )
    else:
        summary = (
            "Decision context allows selective risk-taking "
            "in regime-aligned setups."
        )

    data_quality_note = (
        "" if data_quality_ok
        else "Data feeds partial (Free Polygon tier — VIX unavailable). "
             "Data confidence reduced; sizing conservative."
    )

    expectancy_adjustments_used = [
        item["expectancy"]
        for item in decisions
        if item["expectancy"].get("score_delta") not in {None, 0, 0.0}
    ]

    return {
        "market_state": context.market_state.value,
        "allowed_setups": [setup.value for setup in allowed_setups],
        "hard_overrides": list(hard_overrides),
        "portfolio_heat_limit": context.max_portfolio_heat,
        "summary": summary,
        "data_quality_note": data_quality_note,
        "expectancy_adjustments_used": expectancy_adjustments_used,
        "approved_count": approved_count,
        "blocked_count": blocked_count,
        "decisions": decisions,
    }
