from __future__ import annotations

from src.portfolio_risk import PortfolioCandidate, evaluate_portfolio_risk
from src.signals.signal_generator import build_signals
from src.signals.trade_plan_validator import validate_long_trade_plan


def _decision_report() -> dict:
    return {
        "market_state": "low_vol_bull",
        "portfolio_risk_required": True,
        "decisions": [
            {
                "symbol": "NVDA",
                "decision": "approved",
                "setup_type": "momentum_breakout",
                "risk_tier": "tier_1",
                "position_size_multiplier": 1.0,
                "setup_score": 82,
                "regime_alignment": 0.84,
                "asymmetry_score": 0.74,
                "data_confidence": 0.86,
                "score_source": "scanner_derived",
                "data_source": "live",
                "thresholds_version": "report_scoring_v2",
                "blocked_reasons": [],
                "notes": [],
                "sector": "semiconductors",
            }
        ],
    }


def _scanner_metrics() -> dict:
    returns = tuple(float(i) / 100 for i in range(1, 21))
    return {
        "NVDA": {
            "close": 225.0,
            "atr14": 8.0,
            "atr_pct": 3.6,
            "source": "polygon",
            "source_timestamp": "2026-06-03T14:30:00+00:00",
            "fallback_level": "primary",
            "data_status": "OK",
            "sector": "semiconductors",
            "returns_20d": returns,
        }
    }


def test_182_valid_trade_plan_blocks_when_portfolio_context_missing() -> None:
    result = validate_long_trade_plan(
        entry_trigger=100.0,
        stop_loss=96.0,
        target_1=108.0,
        atr=4.0,
        portfolio_risk_required=True,
        portfolio_risk_result=None,
    )

    assert result.is_valid is False
    assert "portfolio_risk_context_missing" in result.reasons
    assert result.portfolio_risk_status == "BLOCKED"
    assert result.portfolio_risk_block_reason == "portfolio_risk_context_missing"


def test_182_valid_trade_plan_blocks_when_portfolio_heat_exceeded() -> None:
    candidates = [
        PortfolioCandidate("NVDA", "semiconductors", "tier_1", 1.0, tuple(float(i) for i in range(20))),
        PortfolioCandidate("AMD", "semiconductors", "tier_1", 1.0, tuple(float(i) for i in range(20))),
    ]
    portfolio_risk = evaluate_portfolio_risk(candidates, max_portfolio_heat=1.0)

    result = validate_long_trade_plan(
        entry_trigger=100.0,
        stop_loss=96.0,
        target_1=108.0,
        atr=4.0,
        symbol="NVDA",
        portfolio_risk_required=True,
        portfolio_risk_result=portfolio_risk,
    )

    assert result.is_valid is False
    assert "portfolio_risk_blocked" in result.reasons
    assert result.portfolio_risk_status == "BLOCKED"
    assert "portfolio_heat_exceeded" in result.portfolio_risk_block_reason


def test_182_signal_generation_blocks_otherwise_valid_signal_on_portfolio_risk() -> None:
    signals = build_signals(
        _decision_report(),
        _scanner_metrics(),
        "Bullish",
        portfolio_risk_required=True,
        portfolio_risk_limits={"max_portfolio_heat": 0.5, "max_sector_heat": 0.5},
    )

    assert len(signals) == 1
    signal = signals[0]
    assert signal.action == "NO_TRADE"
    assert signal.position_size == 0.0
    assert signal.portfolio_risk_status == "BLOCKED"
    assert "portfolio_risk" in signal.notes
    assert "portfolio_heat_exceeded" in signal.notes or "sector_heat_exceeded" in signal.notes


def test_182_signal_generation_records_passed_portfolio_risk_evidence() -> None:
    signals = build_signals(
        _decision_report(),
        _scanner_metrics(),
        "Bullish",
        portfolio_risk_required=True,
        portfolio_risk_limits={"max_portfolio_heat": 3.0, "max_sector_heat": 2.0},
    )

    signal = signals[0]
    assert signal.action == "BUY_WATCH"
    assert signal.portfolio_risk_status == "PASSED"
    assert signal.portfolio_risk_block_reason is None
    assert signal.portfolio_risk_multiplier == 1.0
