from __future__ import annotations

import json
from pathlib import Path

from src.validation.paper_observation_health_gate import (
    validate_paper_observation_health,
    validate_paper_observation_health_file,
    write_paper_observation_health_report,
)


def _signal(
    symbol: str,
    *,
    close: float | None,
    action: str = "NO_TRADE",
    notes: str = "regime or quality filter",
    market_regime: str = "Neutral",
) -> dict:
    return {
        "signal_id": f"sig_{symbol}",
        "symbol": symbol,
        "action": action,
        "decision": "approved" if action == "BUY_WATCH" else "blocked",
        "close": close,
        "entry_reason": "n/a" if close is not None else "invalid_entry: missing_close",
        "stop_reason": "n/a" if close is not None else "invalid_stop: missing_entry_trigger",
        "exit_reason": "n/a" if close is not None else "invalid_exit: missing_entry_trigger",
        "market_regime": market_regime,
        "notes": notes,
    }


def test_p122_blind_paper_observation_output_fails_health_gate() -> None:
    payload = {
        "market_regime": "Unknown",
        "total_signals": 4,
        "actionable_count": 0,
        "signals": [
            _signal("SPY", close=None, market_regime="Unknown"),
            _signal("QQQ", close=None, market_regime="Unknown"),
            _signal("MSFT", close=None, market_regime="Unknown"),
            _signal("NVDA", close=None, market_regime="Unknown"),
        ],
    }

    report = validate_paper_observation_health(payload)

    assert report.passed is False
    issue_codes = {issue.code for issue in report.issues}
    assert "all_close_values_missing" in issue_codes
    assert "unknown_regime_and_no_close_data" in issue_codes
    assert "zero_actionable_due_to_missing_data" in issue_codes


def test_p122_valid_no_trade_day_passes_when_market_data_is_healthy() -> None:
    payload = {
        "market_regime": "Neutral",
        "total_signals": 4,
        "actionable_count": 0,
        "data_quality": {"data_quality_status": "OK"},
        "signals": [
            _signal("SPY", close=530.0),
            _signal("QQQ", close=460.0),
            _signal("MSFT", close=420.0),
            _signal("NVDA", close=120.0),
        ],
    }

    report = validate_paper_observation_health(payload)

    assert report.passed is True
    assert report.issues == []
    assert report.valid_close_count == 4
    assert report.valid_core_close_count == 2
    assert report.warnings == [
        "No actionable signals, but market data health is valid; treat as normal no-trade day, not infrastructure failure."
    ]


def test_p122_unknown_regime_with_valid_close_data_fails() -> None:
    payload = {
        "market_regime": "Unknown",
        "total_signals": 2,
        "actionable_count": 0,
        "signals": [
            _signal("SPY", close=530.0, market_regime="Unknown"),
            _signal("QQQ", close=460.0, market_regime="Unknown"),
        ],
    }

    report = validate_paper_observation_health(payload)

    assert report.passed is False
    assert {issue.code for issue in report.issues} == {"unknown_regime_with_market_data"}


def test_p122_health_gate_can_read_and_write_reports(tmp_path: Path) -> None:
    payload_path = tmp_path / "latest-signals.json"
    payload_path.write_text(
        json.dumps(
            {
                "market_regime": "Neutral",
                "total_signals": 2,
                "actionable_count": 0,
                "signals": [
                    _signal("SPY", close=530.0),
                    _signal("QQQ", close=460.0),
                ],
            }
        ),
        encoding="utf-8",
    )

    report = validate_paper_observation_health_file(payload_path)
    json_report = tmp_path / "paper_observation_health.json"
    md_report = tmp_path / "paper_observation_health.md"
    write_paper_observation_health_report(report, json_path=json_report, markdown_path=md_report)

    assert report.passed is True
    assert json_report.exists()
    assert md_report.exists()
    assert "Paper Observation Health Gate" in md_report.read_text(encoding="utf-8")
