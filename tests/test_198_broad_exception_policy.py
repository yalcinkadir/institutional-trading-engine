from __future__ import annotations

import asyncio
from pathlib import Path

import pytest

from scripts.check_broad_exception_policy import (
    ACTIVE_PATHS,
    allowlist_entries,
    discover_broad_exception_handlers,
    validate_active_broad_exception_handlers,
    validate_allowlist_contract,
)
from src.exception_audit import build_exception_audit_event, safe_call
from src.outcome_tracking import read_decision_records
from src.runtime.runtime_loop import RuntimeLoop, RuntimeLoopError


def test_198_exception_audit_event_has_required_metadata() -> None:
    event = build_exception_audit_event(
        RuntimeError("boom"),
        stage="scanner.example",
        behavior="structured_degraded_result",
        component="scanner",
        rationale="test rationale",
        trace_id="trace-123",
    )

    assert event["stage"] == "scanner.example"
    assert event["error_class"] == "RuntimeError"
    assert event["error_message"] == "boom"
    assert event["behavior"] == "structured_degraded_result"
    assert event["component"] == "scanner"
    assert event["rationale"] == "test rationale"
    assert event["trace_id"] == "trace-123"
    assert event["policy"] == "EXPLICIT_EXCEPTION_AUDIT"
    assert event["severity"] == "DEGRADED"
    assert event["timestamp_utc"]


def test_198_safe_call_converts_exception_to_structured_audit_metadata() -> None:
    result = safe_call(
        lambda: (_ for _ in ()).throw(ValueError("bad input")),
        stage="reporting.market_regime",
        component="reporting",
        fallback_value={"status": "BLOCKED"},
        trace_id="trace-safe-call",
        behavior="blocked_result",
        rationale="reporting must return explicit blocked evidence",
    )

    assert result.ok is False
    assert result.value == {"status": "BLOCKED"}
    assert result.audit_event["error_class"] == "ValueError"
    assert result.audit_event["behavior"] == "blocked_result"
    assert result.audit_event["trace_id"] == "trace-safe-call"


def test_198_outcome_read_degrades_only_with_audit_metadata(tmp_path: Path) -> None:
    path = tmp_path / "decision_log.csv"
    path.write_text("not-used", encoding="utf-8")
    audit_errors: list[dict[str, str | None]] = []

    records = read_decision_records(
        path,
        audit_errors=audit_errors,
        reader=lambda _path: (_ for _ in ()).throw(OSError("csv unavailable")),
    )

    assert records == []
    assert len(audit_errors) == 1
    assert audit_errors[0]["stage"] == "outcome_tracking.read_decision_records"
    assert audit_errors[0]["error_class"] == "OSError"
    assert audit_errors[0]["behavior"] == "degraded_empty_records"
    assert audit_errors[0]["trace_id"]


def test_198_runtime_loop_logs_then_fails_closed_after_threshold(monkeypatch: pytest.MonkeyPatch) -> None:
    emitted: list[dict] = []

    async def failing_provider() -> dict:
        raise RuntimeError("cycle failed")

    async def no_sleep(_seconds: int) -> None:
        return None

    monkeypatch.setattr("src.runtime.runtime_loop.emit_structured_log", lambda **kwargs: emitted.append(kwargs))
    monkeypatch.setattr("src.runtime.runtime_loop.asyncio.sleep", no_sleep)

    with pytest.raises(RuntimeLoopError):
        asyncio.run(
            RuntimeLoop().start(
                failing_provider,
                cycle_interval_seconds=0,
                max_consecutive_errors=2,
            )
        )

    assert len(emitted) == 2
    assert emitted[0]["event_type"] == "runtime_loop_cycle_provider_error"
    assert emitted[0]["context"]["error_type"] == "RuntimeError"
    assert emitted[1]["context"]["consecutive_errors"] == 2


def test_198_broad_exception_allowlist_contract_is_complete() -> None:
    assert validate_allowlist_contract() == []
    entries = allowlist_entries()
    assert any(
        entry["path"] == "src/outcome_tracking.py"
        and entry["function"] == "read_decision_records"
        and entry["behavior"] == "degraded_empty_records_with_audit_metadata"
        for entry in entries
    )


def test_198_active_broad_exception_handlers_are_allowlisted() -> None:
    handlers = discover_broad_exception_handlers(ACTIVE_PATHS)
    assert handlers
    assert validate_active_broad_exception_handlers() == []
