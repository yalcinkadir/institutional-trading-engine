from __future__ import annotations

from src.reporting.decision_report import build_decision_report
from src.runtime.portfolio_state import PortfolioState


class _PortfolioStateStore:
    def load(self) -> PortfolioState:
        return PortfolioState(
            equity_start=100000.0,
            equity_current=100000.0,
            drawdown_percent=0.0,
            daily_loss_percent=0.0,
            open_positions=[],
            source="test_portfolio_state_store",
            governance_valid=True,
        )


def _market_regime() -> dict:
    return {
        "regime": "Bullish",
        "market_health_score": 82,
        "data_status": "LIVE",
        "breadth": {"breadth_percent": 71, "above_sma50": 11, "universe_size": 16},
        "symbols": {"VIX": {"close": 14}},
    }


def test_180_placeholder_symbol_component_does_not_contribute_to_report_score() -> None:
    report = build_decision_report(
        _market_regime(),
        {"watchlist": ["AAA", "ZZZ"]},
        portfolio_state_store=_PortfolioStateStore(),
    )

    assert report["score_source"] in {"scanner_derived", "evidence_adjusted"}
    for decision in report["decisions"]:
        assert decision["score_source"] != "placeholder"
        assert decision["score_provenance"]["placeholder_score_contribution"] == 0.0
        assert decision["score_provenance"]["symbol_component_source"] == "disabled_no_placeholder"
        assert "symbol_name" not in decision["score_provenance"]["inputs"]


def test_180_scanner_metrics_contribute_to_setup_score_with_provenance() -> None:
    report = build_decision_report(
        _market_regime(),
        {
            "watchlist": ["NVDA"],
            "scanner_metrics": {
                "NVDA": {
                    "trend_score": 0.92,
                    "volume_score": 0.84,
                    "volatility_score": 0.68,
                    "setup_quality_score": 0.88,
                    "liquidity_score": 0.91,
                }
            },
        },
        portfolio_state_store=_PortfolioStateStore(),
    )

    decision = report["decisions"][0]
    provenance = decision["score_provenance"]

    assert decision["setup_score"] > decision["base_market_state_score"]
    assert provenance["setup_score_source"] == "scanner_metrics"
    assert provenance["placeholder_score_contribution"] == 0.0
    assert provenance["scanner_metrics_used"] == {
        "trend_score": 0.92,
        "volume_score": 0.84,
        "volatility_score": 0.68,
        "setup_quality_score": 0.88,
        "liquidity_score": 0.91,
    }
    assert provenance["score_components"]["scanner_evidence_component"] > 0


def test_180_missing_scanner_metrics_are_neutral_not_placeholder_confidence() -> None:
    report = build_decision_report(
        _market_regime(),
        {"watchlist": ["NVDA"]},
        portfolio_state_store=_PortfolioStateStore(),
    )

    decision = report["decisions"][0]
    provenance = decision["score_provenance"]

    assert provenance["setup_score_source"] == "market_context_neutral_no_placeholder"
    assert provenance["score_components"]["scanner_evidence_component"] == 0.0
    assert provenance["placeholder_score_contribution"] == 0.0
    assert decision["score_source"] == "scanner_derived"
    assert decision["data_confidence"] == 0.85


def test_180_report_level_score_provenance_is_exported() -> None:
    report = build_decision_report(
        _market_regime(),
        {"watchlist": ["MSFT"]},
        portfolio_state_store=_PortfolioStateStore(),
    )

    assert report["score_provenance"]["placeholder_scoring_allowed"] is False
    assert report["score_provenance"]["symbol_name_score_enabled"] is False
    assert report["score_provenance"]["score_inputs"] == [
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
