from __future__ import annotations

import importlib
from types import SimpleNamespace

from src.reporting.report_formatter import format_report


def test_p124_run_health_marks_valid_no_trade_day() -> None:
    generate_report = importlib.import_module("scripts.generate_report")

    health = generate_report._derive_market_run_health(
        {
            "scanner_data_quality": {"data_quality_status": "OK"},
            "signal_generation_status": "PASSED",
            "signals": [
                SimpleNamespace(
                    action="NO_TRADE",
                    data_source="live",
                    score_source="live",
                    thresholds_version="v1",
                    fallback_level="primary",
                )
            ],
        }
    )

    assert health["run_health_status"] == "NO_TRADE_VALID"
    assert health["success_status"] == "SUCCESS"
    assert health["reasons"] == ["no_actionable_signals_with_complete_data"]


def test_p124_run_health_marks_degraded_data() -> None:
    generate_report = importlib.import_module("scripts.generate_report")

    health = generate_report._derive_market_run_health(
        {
            "scanner_data_quality": {"data_quality_status": "DEGRADED"},
            "signal_generation_status": "PASSED",
            "signals": [
                SimpleNamespace(
                    action="NO_TRADE",
                    data_source="live",
                    score_source="live",
                    thresholds_version="v1",
                    fallback_level="primary",
                )
            ],
        }
    )

    assert health["run_health_status"] == "DEGRADED_DATA"
    assert health["success_status"] == "DEGRADED"
    assert "scanner_data_quality_degraded" in health["reasons"]


def test_p124_run_health_marks_demo_or_fallback_data() -> None:
    generate_report = importlib.import_module("scripts.generate_report")

    health = generate_report._derive_market_run_health(
        {
            "scanner_data_quality": {"data_quality_status": "OK"},
            "signal_generation_status": "PASSED",
            "signals": [
                SimpleNamespace(
                    action="BUY_WATCH",
                    data_source="fixture",
                    score_source="live",
                    thresholds_version="v1",
                    fallback_level="secondary",
                )
            ],
        }
    )

    assert health["run_health_status"] == "FALLBACK_ACTIVE"
    assert health["success_status"] == "DEGRADED"
    assert "demo_or_fixture_data_used" in health["reasons"]
    assert "non_primary_fallback_active" in health["reasons"]


def test_p124_empty_market_payload_is_failed() -> None:
    generate_report = importlib.import_module("scripts.generate_report")

    health = generate_report._derive_market_run_health(
        {
            "scanner_data_quality": {"data_quality_status": "OK"},
            "signal_generation_status": "PASSED",
            "signals": [],
        }
    )

    assert health["run_health_status"] == "EMPTY_INPUT"
    assert health["success_status"] == "FAILED"
    assert "signals_empty" in health["reasons"]


def test_p124_failed_signal_generation_is_failed() -> None:
    generate_report = importlib.import_module("scripts.generate_report")

    health = generate_report._derive_market_run_health(
        {
            "scanner_data_quality": {"data_quality_status": "OK"},
            "signal_generation_status": "FAILED",
            "signals": [],
        }
    )

    assert health["run_health_status"] == "FAILED"
    assert health["success_status"] == "FAILED"
    assert "signal_generation_failed" in health["reasons"]


def test_p124_report_contains_health_block() -> None:
    report = format_report(
        {
            "report_type": "premarket",
            "market_regime": {"data_status": "ok", "regime": "Neutral", "market_health_score": 50, "symbols": {}, "focus_areas": [], "notes": []},
            "cross_asset": {"data_status": "ok", "regime": "Neutral", "risk_score": 0, "risk_on_score": 0, "risk_off_score": 0},
            "screener": {"title": "Screener", "watchlist": [], "objectives": [], "warnings": []},
            "decision_report": {
                "market_state": "Neutral",
                "portfolio_heat_limit": 0,
                "approved_count": 0,
                "blocked_count": 1,
                "run_health": {"run_health_status": "NO_TRADE_VALID", "success_status": "SUCCESS", "reasons": ["no_actionable_signals_with_complete_data"]},
                "scanner_data_quality": {"data_quality_status": "OK", "valid_symbols": 1, "total_symbols": 1},
                "signal_generation_status": "PASSED",
                "decisions": [],
                "allowed_setups": [],
                "summary": "No trade.",
            },
        }
    )

    assert "## Run Health / Silent-Failure Gate" in report
    assert "Run Health: NO_TRADE_VALID" in report
    assert "Success Status: SUCCESS" in report
    assert "Scanner Data Quality: OK" in report
