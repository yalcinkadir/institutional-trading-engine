"""
Decision Report Builder.

Builds the institutional decision report from market regime and screener data.

Important integrations:
- Data quality degradation reduces confidence instead of causing a hard override.
- Historical expectancy profiles are fed back into setup scoring before ranking.
- Runtime governance is evaluated on the scheduled report path before risk is approved.

The expectancy integration closes the loop:

signals → lifecycle → outcomes → expectancy_r → future scoring
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

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
from src.governance.governance_thresholds import DEFAULT_GOVERNANCE_THRESHOLDS
from src.governance.kill_switch import evaluate_kill_switch_for_portfolio_state
from src.runtime.portfolio_state import PortfolioStateStore
from src.scoring.expectancy_adjuster import (
    DEFAULT_OUTCOME_HISTORY,
    apply_expectancy_to_score,
    default_entry_type_for_setup,
    find_expectancy_adjustment,
)

SCANNER_SCORE_FIELDS = (
    "trend_score",
    "volume_score",
    "volatility_score",
    "setup_quality_score",
    "liquidity_score",
)
SCORE_INPUTS = [
    "market_state_base_score",
    "scanner_trend_score",
    "scanner_volume_score",
    "scanner_volatility_score",
    "scanner_setup_quality_score",
    "scanner_liquidity_score",
    "regime_alignment",
    "asymmetry_score",
    "data_confidence",
    "historical_expectancy_adjustment",
]


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

    # Data quality must not be confused with liquidity stress.
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


def _extract_vix_close(market_regime: dict) -> float | None:
    symbols = market_regime.get("symbols", {}) or {}
    vix_snapshot = symbols.get("VIX", {}) or {}
    close = vix_snapshot.get("close")
    if close is None:
        return None
    try:
        return float(close)
    except (TypeError, ValueError):
        return None


def _build_report_governance(market_regime: dict, portfolio_state_store: Any | None = None) -> dict[str, Any]:
    store = portfolio_state_store or PortfolioStateStore()
    portfolio_state = store.load()
    kill_result = evaluate_kill_switch_for_portfolio_state(
        portfolio_state=portfolio_state,
        vix=_extract_vix_close(market_regime),
        severe_anomaly_count=0,
        thresholds=DEFAULT_GOVERNANCE_THRESHOLDS,
    )
    blocked = bool(kill_result.get("kill_switch"))
    reasons = [str(reason) for reason in kill_result.get("reasons", [])]

    if portfolio_state.daily_loss_percent >= DEFAULT_GOVERNANCE_THRESHOLDS.max_daily_loss_percent:
        blocked = True
        if "max_daily_loss_breached" not in reasons:
            reasons.append("max_daily_loss_breached")

    return {
        "status": "BLOCKED" if blocked else "PASSED",
        "blocked": blocked,
        "reasons": reasons,
        "portfolio_state_source": kill_result.get("portfolio_state_source"),
        "portfolio_governance_valid": kill_result.get("portfolio_governance_valid") is True,
        "portfolio_state_warnings": list(kill_result.get("portfolio_state_warnings", [])),
        "vix_available": kill_result.get("vix_available") is True,
        "live_trading_authorized": False,
        "broker_execution_mode": "paper_only",
    }


def _bounded(value: float, lower: float, upper: float) -> float:
    return max(lower, min(upper, value))


def _market_state_base_score(market_state: MarketState) -> float:
    return {
        MarketState.LOW_VOL_BULL: 78.0,
        MarketState.HIGH_VOL_TRANSITION: 69.0,
        MarketState.NEUTRAL: 64.0,
        MarketState.RISK_OFF: 56.0,
        MarketState.PANIC_DISLOCATION: 52.0,
    }[market_state]


def _coerce_score(value: Any) -> float | None:
    if value is None:
        return None
    try:
        score = float(value)
    except (TypeError, ValueError):
        return None
    if score > 1.0:
        score = score / 100.0
    return _bounded(score, 0.0, 1.0)


def _screener_metrics_map(screener: dict) -> dict[str, dict[str, Any]]:
    for key in ("scanner_metrics", "scanner_metrics_map", "symbol_metrics", "metrics"):
        value = screener.get(key)
        if isinstance(value, dict):
            return {
                str(symbol): metrics
                for symbol, metrics in value.items()
                if isinstance(metrics, dict)
            }
    return {}


def _scanner_score_provenance(symbol: str, scanner_metrics: dict[str, Any] | None) -> dict[str, Any]:
    used: dict[str, float] = {}
    for field in SCANNER_SCORE_FIELDS:
        score = _coerce_score((scanner_metrics or {}).get(field))
        if score is not None:
            used[field] = score

    if used:
        weighted_average = sum(used.values()) / len(used)
        scanner_component = round((weighted_average - 0.5) * 16.0, 4)
        source = "scanner_metrics"
    else:
        weighted_average = 0.5
        scanner_component = 0.0
        source = "market_context_neutral_no_placeholder"

    return {
        "symbol": symbol,
        "setup_score_source": source,
        "symbol_component_source": "disabled_no_placeholder",
        "placeholder_score_contribution": 0.0,
        "scanner_metrics_used": used,
        "inputs": list(SCORE_INPUTS),
        "score_components": {
            "scanner_evidence_component": scanner_component,
            "scanner_weighted_average": round(weighted_average, 4),
        },
    }


def _candidate_for_symbol(
    symbol: str,
    index: int,
    context: MarketContext,
    data_quality_ok: bool,
    *,
    scanner_metrics: dict[str, Any] | None = None,
    outcome_history_path: str | Path = DEFAULT_OUTCOME_HISTORY,
) -> tuple[SetupCandidate, dict]:
    """
    Build report candidate and apply historical expectancy adjustment.

    The candidate remains a normal Decision Engine candidate, but its setup_score
    is adjusted by lifecycle-aware historical evidence where available.
    """
    del index  # #180: ranking must not depend on list-position placeholder noise.

    preferred_setup = {
        MarketState.LOW_VOL_BULL: SetupType.MOMENTUM_BREAKOUT,
        MarketState.HIGH_VOL_TRANSITION: SetupType.PULLBACK_CONTINUATION,
        MarketState.RISK_OFF: SetupType.DEFENSIVE_ROTATION,
        MarketState.PANIC_DISLOCATION: SetupType.REVERSAL_ASYMMETRY,
        MarketState.NEUTRAL: SetupType.PULLBACK_CONTINUATION,
    }[context.market_state]

    score_provenance = _scanner_score_provenance(symbol, scanner_metrics)
    scanner_component = float(score_provenance["score_components"]["scanner_evidence_component"])
    scanner_weighted_average = float(score_provenance["score_components"]["scanner_weighted_average"])
    base_market_state_score = _market_state_base_score(context.market_state)
    base_setup_score = round(
        _bounded(
            base_market_state_score
            + scanner_component
            - (4.0 if context.liquidity_stress else 0.0)
            - (6.0 if context.breadth_collapse else 0.0),
            50.0,
            92.0,
        ),
        2,
    )
    scanner_alignment_component = (scanner_weighted_average - 0.5) * 0.08
    regime_alignment = round(
        _bounded(
            0.66
            + (0.14 if context.market_state == MarketState.LOW_VOL_BULL else 0.0)
            - (0.10 if context.liquidity_stress else 0.0)
            - (0.08 if context.breadth_collapse else 0.0)
            + scanner_alignment_component,
            0.45,
            0.92,
        ),
        2,
    )
    scanner_asymmetry_component = (scanner_weighted_average - 0.5) * 0.10
    asymmetry_score = round(
        _bounded(
            0.64
            + (0.06 if context.max_portfolio_heat >= 1.0 else 0.0)
            - (0.05 if context.liquidity_stress else 0.0)
            + scanner_asymmetry_component,
            0.45,
            0.86,
        ),
        2,
    )

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

    score_source = "evidence_adjusted" if adjustment.score_delta != 0 else "scanner_derived"
    data_source = "live" if data_quality_ok else "scanner_metrics"
    score_provenance["score_components"].update(
        {
            "market_state_base_score": base_market_state_score,
            "liquidity_stress_penalty": -4.0 if context.liquidity_stress else 0.0,
            "breadth_collapse_penalty": -6.0 if context.breadth_collapse else 0.0,
            "base_setup_score": base_setup_score,
            "historical_expectancy_delta": adjustment.score_delta,
            "final_setup_score": adjusted_setup_score,
            "regime_alignment": regime_alignment,
            "asymmetry_score": asymmetry_score,
            "data_confidence": data_confidence,
        }
    )
    meta = {
        "base_market_state_score": base_market_state_score,
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
        "score_source": score_source,
        "data_source": data_source,
        "thresholds_version": "report_scoring_v2",
        "score_provenance": score_provenance,
    }

    return candidate, meta


def build_decision_report(
    market_regime: dict,
    screener: dict,
    outcome_history_path: str | Path = DEFAULT_OUTCOME_HISTORY,
    portfolio_state_store: Any | None = None,
) -> dict:
    context, data_quality_ok = _build_market_context(market_regime)
    report_governance = _build_report_governance(market_regime, portfolio_state_store)
    allowed_setups = get_allowed_setups(context.market_state)
    hard_overrides = list(detect_hard_overrides(context))
    if report_governance["blocked"]:
        hard_overrides.extend(report_governance["reasons"])

    scanner_metrics_map = _screener_metrics_map(screener)
    candidate_pairs = [
        _candidate_for_symbol(
            symbol,
            index,
            context,
            data_quality_ok,
            scanner_metrics=scanner_metrics_map.get(str(symbol)),
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

        decision_value = result.decision.value
        blocked_reasons = list(result.blocked_reasons)
        notes = list(result.notes)

        if report_governance["blocked"]:
            decision_value = Decision.BLOCKED.value
            adjusted_size = 0.0
            blocked_reasons = sorted(set(blocked_reasons + report_governance["reasons"]))
            notes.append("report_governance_blocked_before_risk_approval")

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
                "decision": decision_value,
                "risk_tier": "no_trade" if report_governance["blocked"] else result.risk_tier,
                "position_size_multiplier": adjusted_size,
                "base_position_size_multiplier": result.position_size_multiplier,
                "setup_score": candidate.setup_score,
                "base_market_state_score": meta.get("base_market_state_score"),
                "base_setup_score": meta.get("base_setup_score", candidate.setup_score),
                "score_source": meta.get("score_source", "scanner_derived"),
                "score_provenance": meta.get("score_provenance", {}),
                "data_source": meta.get("data_source", "live"),
                "thresholds_version": meta.get("thresholds_version", "report_scoring_v2"),
                "regime_alignment": round(candidate.regime_alignment, 2),
                "asymmetry_score": round(candidate.asymmetry_score, 2),
                "data_confidence": round(candidate.data_confidence, 2),
                "blocked_reasons": blocked_reasons,
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

    if report_governance["blocked"]:
        summary = (
            "Runtime governance blocked report-path risk approval. "
            "The report is defensive only and must not create actionable exposure."
        )
    elif hard_overrides:
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

    score_sources = {item.get("score_source", "scanner_derived") for item in decisions}
    score_source = "evidence_adjusted" if "evidence_adjusted" in score_sources else "scanner_derived"
    data_source = "live" if data_quality_ok else "scanner_metrics"
    return {
        "market_state": context.market_state.value,
        "allowed_setups": [setup.value for setup in allowed_setups],
        "hard_overrides": hard_overrides,
        "report_governance": report_governance,
        "portfolio_heat_limit": 0.0 if report_governance["blocked"] else context.max_portfolio_heat,
        "summary": summary,
        "data_quality_note": data_quality_note,
        "expectancy_adjustments_used": expectancy_adjustments_used,
        "score_source": score_source,
        "score_provenance": {
            "placeholder_scoring_allowed": False,
            "symbol_name_score_enabled": False,
            "score_inputs": SCORE_INPUTS,
            "scanner_metric_fields": list(SCANNER_SCORE_FIELDS),
        },
        "data_source": data_source,
        "thresholds_version": "report_scoring_v2",
        "approved_count": approved_count,
        "blocked_count": blocked_count,
        "decisions": decisions,
    }
