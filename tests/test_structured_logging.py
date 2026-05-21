from __future__ import annotations

import io
import json

import pytest

from src.structured_logging import build_structured_log_event, emit_structured_log


def test_build_structured_log_event_has_required_shape(monkeypatch) -> None:
    monkeypatch.setenv("GITHUB_RUN_ID", "run-1")
    monkeypatch.setenv("GITHUB_RUN_ATTEMPT", "2")

    event = build_structured_log_event(
        level="info",
        event_type="notification_send_started",
        component="notification_cli",
        message="started",
        cycle_id="cycle-1",
        context={"channel": "telegram"},
        timestamp="2026-05-21T07:30:00+00:00",
    )

    payload = event.to_dict()
    assert payload["timestamp"] == "2026-05-21T07:30:00+00:00"
    assert payload["level"] == "INFO"
    assert payload["event_type"] == "notification_send_started"
    assert payload["component"] == "notification_cli"
    assert payload["message"] == "started"
    assert payload["cycle_id"] == "cycle-1"
    assert payload["workflow_run_id"] == "run-1"
    assert payload["workflow_run_attempt"] == "2"
    assert payload["context"] == {"channel": "telegram"}


def test_structured_log_event_is_json_serializable() -> None:
    event = build_structured_log_event(
        level="WARNING",
        event_type="watcher_runtime_warning",
        component="entry_exit_watcher",
        message="warning",
        context={"count": 3},
        timestamp="2026-05-21T07:30:00+00:00",
    )

    payload = json.loads(event.to_json())

    assert payload["level"] == "WARNING"
    assert payload["context"] == {"count": 3}


def test_invalid_log_level_raises() -> None:
    with pytest.raises(ValueError, match="Invalid log level"):
        build_structured_log_event(
            level="NOTICE",
            event_type="bad_level",
            component="test",
            message="bad",
        )


def test_emit_structured_log_writes_json_line() -> None:
    stream = io.StringIO()

    event = emit_structured_log(
        level="INFO",
        event_type="notification_send_completed",
        component="notification_cli",
        message="completed",
        cycle_id="cycle-2",
        context={"failed": False},
        stream=stream,
    )

    line = stream.getvalue().strip()
    payload = json.loads(line)

    assert payload["event_type"] == "notification_send_completed"
    assert payload["component"] == "notification_cli"
    assert payload["cycle_id"] == "cycle-2"
    assert payload["context"] == {"failed": False}
    assert event.event_type == "notification_send_completed"
