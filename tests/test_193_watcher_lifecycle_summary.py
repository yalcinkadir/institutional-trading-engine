from __future__ import annotations

import json
from pathlib import Path

from scripts.watcher_lifecycle_summary import (
    NO_ACTIONABLE_SIGNALS,
    build_watcher_lifecycle_summary,
    write_watcher_lifecycle_summary,
)
from src.watchers.entry_exit_watcher import build_watcher_market_data_health


def _signal(**overrides):
    payload = {
        "signal_id": "stable-no-trade-id",
        "symbol": "NVDA",
        "action": "NO_TRADE",
        "decision": "rejected",
        "status": "PENDING",
        "generated_at": "2026-06-11T18:00:00Z",
    }
    payload.update(overrides)
    return payload


def test_193_watcher_lifecycle_summary_marks_zero_actionable_runs_explicitly(tmp_path: Path) -> None:
    signals_file = tmp_path / "reports/signals/latest-signals.json"
    signals_file.parent.mkdir(parents=True, exist_ok=True)
    signals_file.write_text(json.dumps({"signals": [_signal()]}, indent=2), encoding="utf-8")
    signals = [_signal()]
    health = build_watcher_market_data_health(
        signals,
        evaluated_symbols=set(),
        generated_at="2026-06-11T18:10:00+00:00",
        cycle_id="entry-exit-watcher-test-1",
        artifact_path="reports/runtime/entry_exit_watcher_market_data_health.json",
    )

    summary = build_watcher_lifecycle_summary(
        signals=signals,
        updates=[],
        health=health,
        cycle_id="entry-exit-watcher-test-1",
        signals_file=signals_file,
        generated_at="2026-06-11T18:10:00+00:00",
    )

    assert summary["schema_version"] == "watcher_lifecycle_summary.v1"
    assert summary["summary_date"] == "2026-06-11"
    assert summary["status"] == NO_ACTIONABLE_SIGNALS
    assert summary["signal_count"] == 1
    assert summary["actionable_open_count"] == 0
    assert summary["lifecycle_event_count"] == 0
    assert summary["signal_file_path"].endswith("reports/signals/latest-signals.json")
    assert summary["signal_file_sha256"]
    assert summary["records"][0]["watcher_status"] == NO_ACTIONABLE_SIGNALS
    assert summary["records"][0]["trigger_expiry_block_reason"] == "not_actionable_or_terminal_signal"
    assert summary["records"][0]["data_completeness_status"] == "PASSED"


def test_193_watcher_lifecycle_summary_writer_creates_dated_and_latest_files(tmp_path: Path) -> None:
    signals_file = tmp_path / "reports/signals/latest-signals.json"
    signals_file.parent.mkdir(parents=True, exist_ok=True)
    signals = [_signal(signal_id="stable-no-actionable-id", symbol="MSFT")]
    signals_file.write_text(json.dumps({"signals": signals}, indent=2), encoding="utf-8")
    health = build_watcher_market_data_health(
        signals,
        evaluated_symbols=set(),
        generated_at="2026-06-11T19:00:00+00:00",
        cycle_id="entry-exit-watcher-test-2",
        artifact_path="reports/runtime/entry_exit_watcher_market_data_health.json",
    )

    dated, latest = write_watcher_lifecycle_summary(
        signals=signals,
        updates=[],
        health=health,
        cycle_id="entry-exit-watcher-test-2",
        signals_file=signals_file,
        output_dir=tmp_path / "reports/watchers/lifecycle",
        generated_at="2026-06-11T19:00:00+00:00",
    )

    assert dated == tmp_path / "reports/watchers/lifecycle/2026-06-11.json"
    assert latest == tmp_path / "reports/watchers/lifecycle/latest.json"
    assert dated.exists()
    assert latest.exists()
    dated_payload = json.loads(dated.read_text(encoding="utf-8"))
    latest_payload = json.loads(latest.read_text(encoding="utf-8"))
    assert dated_payload == latest_payload
    assert dated_payload["status"] == NO_ACTIONABLE_SIGNALS
    assert dated_payload["records"][0]["symbol"] == "MSFT"


def test_193_runner_imports_and_writes_lifecycle_summary_for_no_actionable_path() -> None:
    runner = Path("scripts/run_entry_exit_watcher.py").read_text(encoding="utf-8")

    assert "from scripts.watcher_lifecycle_summary import write_watcher_lifecycle_summary" in runner
    assert "_persist_lifecycle_summary(" in runner
    assert "updates=[]" in runner
    assert "watcher_no_actionable_signals" in runner
    assert "reports/watchers/lifecycle/YYYY-MM-DD.json" in runner
    assert "reports/watchers/lifecycle/latest.json" in runner
