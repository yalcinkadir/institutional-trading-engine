from __future__ import annotations

from src.decision_engine import (
    Decision,
    MarketContext,
    MarketState,
    SetupCandidate,
    SetupType,
    detect_hard_overrides,
    evaluate_candidate,
    get_allowed_setups,
    rank_candidates,
)


def _map_regime_to_market_state(regime: str, market_health_score: int | float | str) -> MarketState:
    regime_normalized = str(regime).strip().lower().replace("-", "_").replace(" ", "_")

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


def _build_market_context(market_regime: dict) -> MarketContext:
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
    liquidity_stress = market_regime.get("data_status") != "LIVE"
    volatility_stress = vix_close >= 25

    if volatility_stress and market_state == MarketState.LOW_VOL_BULL:
        market_state = MarketState.HIGH_VOL_TRANSITION

    if vix_close >= 35:
        market_state = MarketState.PANIC_DISLOCATION

    return MarketContext(
        market_state=market_state,
        breadth_collapse=breadth_collapse,
        liquidity_stress=liquidity_stress,
        failed_breakout_cluster=False,
        max_portfolio_heat=0.5 if market_state in {MarketState.RISK_OFF, MarketState.HIGH_VOL_TRANSITION} else 1.0,
    )


def _candidate_for_symbol(symbol: str, index: int, context: MarketContext) -> SetupCandidate:
    """Build deterministic report candidates until richer live setup inputs exist."""
    preferred_setup = {
        MarketState.LOW_VOL_BULL: SetupType.MOMENTUM_BREAKOUT,
        MarketState.HIGH_VOL_TRANSITION: SetupType.PULLBACK_CONTINUATION,
        MarketState.RISK_OFF: SetupType.DEFENSIVE_ROTATION,
        MarketState.PANIC_DISLOCATION: SetupType.REVERSAL_ASYMMETRY,
        MarketState.NEUTRAL: SetupType.PULLBACK_CONTINUATION,
    }[context.market_state]

    # Conservative deterministic defaults. These are not alpha signals; they are
    # report-policy candidates used to show whether the current regime allows
    # risk, blocks risk or reduces size.
    setup_score = max(55, 82 - index * 3)
    regime_alignment = max(0.45, 0.82 - index * 0.04)
    asymmetry_score = max(0.45, 0.72 - index * 0.03)
    data_confidence = 0.85 if not context.liquidity_stress else 0.45

    return SetupCandidate(
        symbol=symbol,
        setup_type=preferred_setup,
        setup_score=setup_score,
        regime_alignment=regime_alignment,
        asymmetry_score=asymmetry_score,
        data_confidence=data_confidence,
    )


def build_decision_report(market_regime: dict, screener: dict) -> dict:
    context = _build_market_context(market_regime)
    allowed_setups = get_allowed_setups(context.market_state)
    hard_overrides = detect_hard_overrides(context)

    candidates = [
        _candidate_for_symbol(symbol, index, context)
        for index, symbol in enumerate(screener.get("watchlist", []))
    ]

    ranked = rank_candidates(context, candidates)

    decisions = []
    for candidate, result in ranked:
        decisions.append(
            {
                "symbol": candidate.symbol,
                "setup_type": candidate.setup_type.value,
                "decision": result.decision.value,
                "risk_tier": result.risk_tier,
                "position_size_multiplier": result.position_size_multiplier,
                "setup_score": candidate.setup_score,
                "regime_alignment": round(candidate.regime_alignment, 2),
                "asymmetry_score": round(candidate.asymmetry_score, 2),
                "data_confidence": round(candidate.data_confidence, 2),
                "blocked_reasons": list(result.blocked_reasons),
                "notes": list(result.notes),
            }
        )

    approved_count = sum(
        1 for item in decisions if item["decision"] in {Decision.APPROVED.value, Decision.REDUCED_SIZE.value}
    )
    blocked_count = sum(
        1 for item in decisions if item["decision"] in {Decision.BLOCKED.value, Decision.NO_TRADE.value}
    )

    if hard_overrides:
        summary = "Hard risk override active. The report should prioritize defense and avoid new aggressive exposure."
    elif approved_count == 0:
        summary = "No high-quality asymmetric opportunity found. No-trade or watch mode is preferred."
    elif context.market_state == MarketState.HIGH_VOL_TRANSITION:
        summary = "Opportunities exist, but high-volatility transition requires reduced position sizing."
    else:
        summary = "Decision context allows selective risk-taking in regime-aligned setups."

    return {
        "market_state": context.market_state.value,
        "allowed_setups": [setup.value for setup in allowed_setups],
        "hard_overrides": list(hard_overrides),
        "portfolio_heat_limit": context.max_portfolio_heat,
        "summary": summary,
        "approved_count": approved_count,
        "blocked_count": blocked_count,
        "decisions": decisions,
    }
