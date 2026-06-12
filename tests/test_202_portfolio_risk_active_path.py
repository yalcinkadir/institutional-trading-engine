from __future__ import annotations

from dataclasses import asdict

from src.signals.signal_generator import build_signals
from src.signals.trade_plan_validator import validate_long_trade_plan


def _decision_report(*, portfolio_required: bool = True) -> dict:
    return {
        "market_state": "low_vol_bull",
        "portfolio_risk_required": portfolio_required,
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


def _scanner_metrics(*, include_returns: bool = True) -> dict:
    metrics = {
        "close": 225.0,
        "high": 226.0,
        "low": 218.0,
        "atr14": 8.0,
        "atr_pct": 3.6,
        "sma20": 220.0,
        "sma50": 210.0,
        "source": "polygon",
        "source_timestamp": "2026-06-12T14:30:00+00:00",
        "fallback_level": "primary",
        "data_status": "OK",
        "sector": "semiconductors",
    }
    if include_returns:
        metrics["returns_20d"] = tuple(float(i) / 100 for i in range(1, 21))
    return {"NVDA": metrics}


def test_202_otherwise_valid_signal_fails_closed_when_portfolio_context_missing() -> None:
    signals = build_signals(
        _decision_report(portfolio_required=True),
        _scanner_metrics(include_returns=False),
        "Bullish",
        portfolio_risk_required=True,
    )

    signal = signals[0]
    assert signal.action == "NO_TRADE"
    assert signal.position_size == 0.0
    assert signal.portfolio_risk_status == "BLOCKED"
    assert signal.portfolio_risk_block_reason == "portfolio_risk_context_missing"
    assert "portfolio_risk_context_missing" in signal.notes


def test_202_otherwise_valid_signal_blocks_due_to_portfolio_risk_limits() -> None:
    signals = build_signals(
        _decision_report(portfolio_required=True),
        _scanner_metrics(include_returns=True),
        "Bullish",
        portfolio_risk_required=True,
        portfolio_risk_limits={"max_portfolio_heat": 0.5, "max_sector_heat": 0.5},
    )

    signal = signals[0]
    assert signal.action == "NO_TRADE"
    assert signal.position_size == 0.0
    assert signal.portfolio_risk_status == "BLOCKED"
    assert signal.portfolio_risk_block_reason is not None
    assert "portfolio_heat_exceeded" in signal.portfolio_risk_block_reason or "sector_heat_exceeded" in signal.portfolio_risk_block_reason
    assert "portfolio_risk" in signal.notes


def test_202_signal_payload_records_portfolio_risk_evidence_fields() -> None:
    signal = build_signals(
        _decision_report(portfolio_required=True),
        _scanner_metrics(include_returns=True),
        "Bullish",
        portfolio_risk_required=True,
        portfolio_risk_limits={"max_portfolio_heat": 3.0, "max_sector_heat": 2.0},
    )[0]

    payload = asdict(signal)

    assert payload["portfolio_risk_status"] == "PASSED"
    assert payload["portfolio_risk_block_reason"] is None
    assert payload["portfolio_risk_multiplier"] == 1.0
    assert payload["action"] == "BUY_WATCH"


def test_202_trade_plan_validator_blocks_missing_portfolio_context() -> None:
    result = validate_long_trade_plan(
        entry_trigger=100.0,
        stop_loss=96.0,
        target_1=108.0,
        atr=4.0,
        symbol="NVDA",
        portfolio_risk_required=True,
        portfolio_risk_result=None,
    )

    assert result.is_valid is False
    assert result.portfolio_risk_status == "BLOCKED"
    assert result.portfolio_risk_block_reason == "portfolio_risk_context_missing"
    assert "portfolio_risk_context_missing" in result.reasons
