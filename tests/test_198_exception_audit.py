from __future__ import annotations

from pathlib import Path

import pytest

from src.exception_audit import build_exception_audit_event, format_exception_audit_summary
from src.outcome_tracking import read_decision_records
from src.reporting import market_regime


def test_198_exception_audit_event_has_required_metadata() -> None:
    event = build_exception_audit_event(
        RuntimeError("provider failed"),
        stage="scanner.fetch",
        behavior="degraded_continue",
        component="scanner",
        rationale="safe degraded output contains explicit error metadata",
        trace_id="trace-123",
    )

    assert event["stage"] == "scanner.fetch"
    assert event["error_class"] == "RuntimeError"
    assert event["error_message"] == "provider failed"
    assert event["behavior"] == "degraded_continue"
    assert event["component"] == "scanner"
    assert event["rationale"] == "safe degraded output contains explicit error metadata"
    assert event["trace_id"] == "trace-123"
    assert event["timestamp_utc"]
    assert "trace-123" in format_exception_audit_summary(event)


def test_198_outcome_read_failure_is_not_silent(tmp_path: Path) -> None:
    broken_path = tmp_path / "broken.csv"
    broken_path.write_text("symbol,result_5d\nAAPL,1\n", encoding="utf-8")
    broken_path.chmod(0o000)
    audit_errors: list[dict[str, str | None]] = []

    try:
        # Force a parser-level failure independent of platform permission semantics.
        records = read_decision_records(broken_path, audit_errors=audit_errors, reader=lambda _path: (_ for _ in ()).throw(ValueError("csv parse failed")))
    finally:
        broken_path.chmod(0o644)

    assert records == []
    assert len(audit_errors) == 1
    assert audit_errors[0]["stage"] == "outcome_tracking.read_decision_records"
    assert audit_errors[0]["error_class"] == "ValueError"
    assert audit_errors[0]["error_message"] == "csv parse failed"
    assert audit_errors[0]["behavior"] == "degraded_empty_records"
    assert audit_errors[0]["trace_id"]


def test_198_market_regime_client_failure_contains_structured_audit(monkeypatch: pytest.MonkeyPatch) -> None:
    class BrokenClient:
        def __init__(self) -> None:
            raise RuntimeError("client init failed")

    monkeypatch.setattr(market_regime, "PolygonClient", BrokenClient)

    summary = market_regime.build_market_regime_summary("premarket")

    assert summary["regime_validation_status"] == market_regime.REGIME_STATUS_BLOCKED
    assert summary["exception_audit"]
    audit = summary["exception_audit"][0]
    assert audit["stage"] == "reporting.market_regime.PolygonClient"
    assert audit["error_class"] == "RuntimeError"
    assert audit["error_message"] == "client init failed"
    assert audit["behavior"] == "fail_closed_blocked_regime"
    assert audit["trace_id"]


def test_198_market_regime_breadth_failure_contains_structured_audit(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(market_regime, "_try_symbol_snapshot", lambda _client, ticker: ({"ticker": ticker, "close": 100, "above_sma50": True, "above_sma200": True}, None))

    def broken_breadth(_client):
        raise RuntimeError("breadth failed")

    monkeypatch.setattr(market_regime, "_calculate_breadth", broken_breadth)

    summary = market_regime.build_market_regime_summary("premarket")

    assert summary["exception_audit"]
    audit = summary["exception_audit"][0]
    assert audit["stage"] == "reporting.market_regime.breadth"
    assert audit["error_class"] == "RuntimeError"
    assert audit["error_message"] == "breadth failed"
    assert audit["behavior"] == "degraded_continue"
    assert audit["trace_id"]
