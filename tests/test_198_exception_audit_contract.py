from __future__ import annotations

from pathlib import Path

from src.exception_audit import build_exception_audit_event, safe_call
from src.outcome_tracking import read_decision_records_with_audit


REPO_ROOT = Path(__file__).resolve().parents[1]
ACTIVE_EXCEPTION_PATHS = [
    "src/runtime/runtime_loop.py",
    "src/reporting/market_regime.py",
    "src/outcome_tracking.py",
]


def test_198_exception_audit_event_has_required_metadata() -> None:
    event = build_exception_audit_event(
        stage="unit_test_stage",
        exc=ValueError("bad value"),
        component="unit_test_component",
        trace_id="trace-198",
        severity="DEGRADED",
    )

    assert event["stage"] == "unit_test_stage"
    assert event["component"] == "unit_test_component"
    assert event["trace_id"] == "trace-198"
    assert event["severity"] == "DEGRADED"
    assert event["error_class"] == "ValueError"
    assert event["error_message"] == "bad value"
    assert event["policy"] == "EXPLICIT_EXCEPTION_AUDIT"
    assert "timestamp_utc" in event


def test_198_safe_call_returns_structured_degraded_result() -> None:
    def raises() -> str:
        raise RuntimeError("provider exploded")

    result = safe_call(
        raises,
        stage="scanner.fetch",
        component="scanner",
        trace_id="run-198",
        fallback_value={"status": "BLOCKED"},
    )

    assert result.ok is False
    assert result.value == {"status": "BLOCKED"}
    assert result.audit_event["stage"] == "scanner.fetch"
    assert result.audit_event["error_class"] == "RuntimeError"
    assert result.audit_event["error_message"] == "provider exploded"


def test_198_outcome_reader_exposes_audit_metadata_for_read_errors(tmp_path: Path) -> None:
    input_path = tmp_path / "decision_log.csv"
    input_path.write_text("symbol,decision\nAAPL,approved\n", encoding="utf-8")

    def broken_reader(_path: Path) -> list[dict[str, object]]:
        raise OSError("forced read failure")

    result = read_decision_records_with_audit(
        input_path,
        trace_id="outcome-read-198",
        reader=broken_reader,
    )

    assert result.ok is False
    assert result.records == []
    assert result.audit_event is not None
    assert result.audit_event["stage"] == "outcome_tracking.read_decision_records"
    assert result.audit_event["trace_id"] == "outcome-read-198"
    assert result.audit_event["error_class"] == "OSError"
    assert result.audit_event["error_message"] == "forced read failure"
    assert result.audit_event["policy"] == "EXPLICIT_EXCEPTION_AUDIT"


def test_198_active_broad_exception_handlers_have_policy_marker() -> None:
    for relative_path in ACTIVE_EXCEPTION_PATHS:
        source = (REPO_ROOT / relative_path).read_text(encoding="utf-8")
        lines = source.splitlines()
        for index, line in enumerate(lines):
            if "except Exception" not in line:
                continue
            window = "\n".join(lines[max(0, index - 3): index + 8])
            assert "#198" in window or "EXPLICIT_EXCEPTION_AUDIT" in window or "noqa: BLE001" in line, (
                f"Broad exception handler in {relative_path}:{index + 1} lacks #198 audit marker"
            )
