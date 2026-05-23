from __future__ import annotations

import json
from pathlib import Path

from src.operations.entry_exit_watcher_health import (
    render_watcher_health_markdown,
    run_entry_exit_watcher_health_check,
    write_watcher_health_report,
)


def _write_signals(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            {
                "signals": [
                    {"signal_id": "s1", "symbol": "SPY", "action": "BUY_WATCH"},
                    {"signal_id": "s2", "symbol": "QQQ", "action": "NO_TRADE"},
                ]
            }
        ),
        encoding="utf-8",
    )


def _write_lifecycle(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    events = [
        {"signal_id": "s1", "event_type": "PENDING"},
        {"signal_id": "s1", "event_type": "TRIGGERED"},
        {"signal_id": "s1", "event_type": "TARGET_1_HIT"},
    ]
    path.write_text("\n".join(json.dumps(event) for event in events) + "\n", encoding="utf-8")


def test_watcher_health_passes_with_valid_artifacts(tmp_path: Path) -> None:
    signals = tmp_path / "reports/signals/latest-signals.json"
    lifecycle = tmp_path / "data/signal_lifecycle.jsonl"
    _write_signals(signals)
    _write_lifecycle(lifecycle)

    report = run_entry_exit_watcher_health_check(
        signals_file=signals,
        lifecycle_file=lifecycle,
        min_signals=1,
        min_lifecycle_events=2,
        require_terminal_event=True,
    )

    assert report.healthy is True
    assert report.signal_count == 2
    assert report.buy_watch_count == 1
    assert report.lifecycle_event_count == 3
    assert report.terminal_event_count == 1
    assert report.malformed_lifecycle_lines == 0


def test_watcher_health_fails_when_files_are_missing(tmp_path: Path) -> None:
    report = run_entry_exit_watcher_health_check(
        signals_file=tmp_path / "missing-signals.json",
        lifecycle_file=tmp_path / "missing-lifecycle.jsonl",
    )

    assert report.healthy is False
    failed = {gate.name for gate in report.gates if not gate.passed}
    assert "signals_file_present_and_parseable" in failed
    assert "lifecycle_file_present_and_parseable" in failed
    assert "minimum_signals_loaded" in failed
    assert "minimum_lifecycle_events_loaded" in failed


def test_watcher_health_detects_malformed_lifecycle_lines(tmp_path: Path) -> None:
    signals = tmp_path / "signals.json"
    lifecycle = tmp_path / "life.jsonl"
    _write_signals(signals)
    lifecycle.write_text('{"event_type": "PENDING"}\nnot-json\n[]\n', encoding="utf-8")

    report = run_entry_exit_watcher_health_check(
        signals_file=signals,
        lifecycle_file=lifecycle,
        min_signals=1,
        min_lifecycle_events=1,
    )

    assert report.healthy is False
    assert report.lifecycle_event_count == 1
    assert report.malformed_lifecycle_lines == 2
    failed = {gate.name for gate in report.gates if not gate.passed}
    assert "no_malformed_lifecycle_lines" in failed


def test_write_watcher_health_report_outputs_json_and_markdown(tmp_path: Path) -> None:
    signals = tmp_path / "signals.json"
    lifecycle = tmp_path / "life.jsonl"
    _write_signals(signals)
    _write_lifecycle(lifecycle)
    report = run_entry_exit_watcher_health_check(signals_file=signals, lifecycle_file=lifecycle)

    json_path = tmp_path / "reports/watcher/health.json"
    markdown_path = tmp_path / "reports/watcher/health.md"
    write_watcher_health_report(report, json_path=json_path, markdown_path=markdown_path)

    payload = json.loads(json_path.read_text(encoding="utf-8"))
    assert payload["healthy"] is True
    markdown = markdown_path.read_text(encoding="utf-8")
    assert "Entry/Exit Watcher Health Report" in markdown
    assert "TARGET_1_HIT" in render_watcher_health_markdown(report)
