from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import patch

import pytest

from scripts.run_entry_exit_watcher import (
    WatcherRuntimeConfigurationError,
    _build_cycle_id,
    _validate_runtime,
    main,
)


def test_build_cycle_id_uses_github_context(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("GITHUB_RUN_ID", "12345")
    monkeypatch.setenv("GITHUB_RUN_ATTEMPT", "2")

    assert _build_cycle_id() == "entry-exit-watcher-12345-2"


def test_validate_runtime_requires_positive_days(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("POLYGON_API_KEY", "test-key")
    signals_file = tmp_path / "signals.json"
    signals_file.write_text("[]", encoding="utf-8")

    with pytest.raises(WatcherRuntimeConfigurationError, match="positive integer"):
        _validate_runtime(signals_file=signals_file, days=0)


def test_validate_runtime_requires_polygon_api_key(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("POLYGON_API_KEY", raising=False)
    signals_file = tmp_path / "signals.json"
    signals_file.write_text("[]", encoding="utf-8")

    with pytest.raises(WatcherRuntimeConfigurationError, match="POLYGON_API_KEY"):
        _validate_runtime(signals_file=signals_file, days=5)


def test_validate_runtime_requires_existing_signals_file(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("POLYGON_API_KEY", "test-key")

    with pytest.raises(WatcherRuntimeConfigurationError, match="Signals file not found"):
        _validate_runtime(signals_file=tmp_path / "missing.json", days=5)


def test_validate_runtime_rejects_invalid_json(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("POLYGON_API_KEY", "test-key")
    signals_file = tmp_path / "signals.json"
    signals_file.write_text("not-json", encoding="utf-8")

    with pytest.raises(WatcherRuntimeConfigurationError, match="invalid JSON"):
        _validate_runtime(signals_file=signals_file, days=5)


def test_validate_runtime_requires_signal_list(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("POLYGON_API_KEY", "test-key")
    signals_file = tmp_path / "signals.json"
    signals_file.write_text(json.dumps({"symbol": "AAPL"}), encoding="utf-8")

    with pytest.raises(WatcherRuntimeConfigurationError, match="JSON list"):
        _validate_runtime(signals_file=signals_file, days=5)


def test_validate_runtime_accepts_valid_empty_signal_list(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("POLYGON_API_KEY", "test-key")
    signals_file = tmp_path / "signals.json"
    signals_file.write_text("[]", encoding="utf-8")

    _validate_runtime(signals_file=signals_file, days=5)


def test_main_emits_structured_logs_for_validation_failure(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    missing_file = tmp_path / "missing.json"
    monkeypatch.setenv("POLYGON_API_KEY", "test-key")
    monkeypatch.setenv("GITHUB_RUN_ID", "111")
    monkeypatch.setenv("GITHUB_RUN_ATTEMPT", "1")
    monkeypatch.setattr(
        "sys.argv",
        ["run_entry_exit_watcher.py", "--signals-file", str(missing_file)],
    )

    events: list[dict] = []

    def fake_log(**kwargs):
        events.append(kwargs)

    with patch("scripts.run_entry_exit_watcher.emit_structured_log", side_effect=fake_log):
        exit_code = main()

    assert exit_code == 2
    assert [event["event_type"] for event in events] == [
        "watcher_runner_started",
        "watcher_runtime_validation_failed",
    ]
    assert all(event["cycle_id"] == "entry-exit-watcher-111-1" for event in events)
    assert events[-1]["level"] == "ERROR"


def test_main_emits_structured_logs_for_no_actionable_signals(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    signals_file = tmp_path / "signals.json"
    signals_file.write_text("[]", encoding="utf-8")
    monkeypatch.setenv("POLYGON_API_KEY", "test-key")
    monkeypatch.setattr(
        "sys.argv",
        ["run_entry_exit_watcher.py", "--signals-file", str(signals_file)],
    )

    events: list[dict] = []

    def fake_log(**kwargs):
        events.append(kwargs)

    with patch("scripts.run_entry_exit_watcher.emit_structured_log", side_effect=fake_log):
        exit_code = main()

    assert exit_code == 0
    event_types = [event["event_type"] for event in events]
    assert "watcher_runner_started" in event_types
    assert "watcher_runtime_validation_succeeded" in event_types
    assert "watcher_signals_loaded" in event_types
    assert "watcher_no_actionable_signals" in event_types
