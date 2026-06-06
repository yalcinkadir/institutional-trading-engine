from __future__ import annotations

import importlib
from types import SimpleNamespace


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
