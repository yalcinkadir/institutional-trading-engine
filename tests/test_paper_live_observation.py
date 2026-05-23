from __future__ import annotations

import json
from pathlib import Path

from src.operations.paper_live_observation import (
    observe_paper_live,
    render_paper_live_markdown,
    write_paper_live_report,
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
        {"signal_id": "s1", "event_type": "TARGET_2_HIT"},
        {"signal_id": "s2", "event_type": "EXPIRED"},
    ]
    path.write_text("\n".join(json.dumps(event) for event in events) + "\n", encoding="utf-8")


def _write_alerts(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"alerts": [{"message": "test alert"}]}), encoding="utf-8")


def test_observe_paper_live_passes_with_required_artifacts(tmp_path: Path) -> None:
    signals = tmp_path / "reports/signals/latest-signals.json"
    lifecycle = tmp_path / "data/signal_lifecycle.jsonl"
    alerts = tmp_path / "reports/alerts/latest-alerts.json"
    _write_signals(signals)
    _write_lifecycle(lifecycle)
    _write_alerts(alerts)

    report = observe_paper_live(
        signals_file=signals,
        lifecycle_file=lifecycle,
        alerts_file=alerts,
        min_lifecycle_events=5,
        require_alerts=True,
    )

    assert report.ready_for_review is True
    assert report.signal_count == 2
    assert report.buy_watch_count == 1
    assert report.lifecycle_event_count == 5
    assert report.terminal_event_count == 3
    assert report.alert_count == 1
    assert report.lifecycle_event_types["TARGET_2_HIT"] == 1


def test_observe_paper_live_fails_without_lifecycle_events(tmp_path: Path) -> None:
    signals = tmp_path / "signals.json"
    lifecycle = tmp_path / "missing.jsonl"
    alerts = tmp_path / "alerts.json"
    _write_signals(signals)

    report = observe_paper_live(
        signals_file=signals,
        lifecycle_file=lifecycle,
        alerts_file=alerts,
        min_lifecycle_events=1,
    )

    assert report.ready_for_review is False
    failed_gates = {gate.name for gate in report.gates if not gate.passed}
    assert "lifecycle_file_readable" in failed_gates
    assert "minimum_lifecycle_events" in failed_gates
    assert "terminal_events_observed" in failed_gates


def test_observe_paper_live_alert_gate_is_optional(tmp_path: Path) -> None:
    signals = tmp_path / "signals.json"
    lifecycle = tmp_path / "life.jsonl"
    alerts = tmp_path / "missing-alerts.json"
    _write_signals(signals)
    _write_lifecycle(lifecycle)

    report_without_alert_requirement = observe_paper_live(
        signals_file=signals,
        lifecycle_file=lifecycle,
        alerts_file=alerts,
        min_lifecycle_events=5,
        require_alerts=False,
    )
    report_with_alert_requirement = observe_paper_live(
        signals_file=signals,
        lifecycle_file=lifecycle,
        alerts_file=alerts,
        min_lifecycle_events=5,
        require_alerts=True,
    )

    assert report_without_alert_requirement.ready_for_review is True
    assert report_with_alert_requirement.ready_for_review is False
    assert "alerts_observed" in {gate.name for gate in report_with_alert_requirement.gates if not gate.passed}


def test_write_paper_live_report_outputs_json_and_markdown(tmp_path: Path) -> None:
    signals = tmp_path / "signals.json"
    lifecycle = tmp_path / "life.jsonl"
    alerts = tmp_path / "alerts.json"
    _write_signals(signals)
    _write_lifecycle(lifecycle)
    _write_alerts(alerts)
    report = observe_paper_live(
        signals_file=signals,
        lifecycle_file=lifecycle,
        alerts_file=alerts,
        min_lifecycle_events=5,
        require_alerts=True,
    )

    json_path = tmp_path / "paper-live.json"
    markdown_path = tmp_path / "paper-live.md"
    write_paper_live_report(report, json_path=json_path, markdown_path=markdown_path)

    assert json.loads(json_path.read_text(encoding="utf-8"))["ready_for_review"] is True
    markdown = markdown_path.read_text(encoding="utf-8")
    assert "Paper-Live Observation Report" in markdown
    assert "Ready for review" in markdown
    assert "TARGET_1_HIT" in render_paper_live_markdown(report)
