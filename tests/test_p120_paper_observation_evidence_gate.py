from __future__ import annotations

import json
from pathlib import Path

from src.operations.paper_live_observation import observe_paper_live, write_paper_live_report
from src.operations.paper_observation_evidence_gate import validate_paper_observation_evidence_artifact


def _write_signals(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            {
                "signals": [
                    {
                        "signal_id": "sig_NVDA_001",
                        "symbol": "NVDA",
                        "action": "BUY_WATCH",
                        "decision": "approved",
                        "data_status": "OK",
                        "source": "polygon",
                        "source_timestamp": "2026-06-05T13:30:00+00:00",
                        "fallback_level": "primary",
                    },
                    {
                        "signal_id": "sig_QQQ_001",
                        "symbol": "QQQ",
                        "action": "NO_TRADE",
                        "decision": "blocked",
                        "data_status": "DEGRADED",
                        "source": "polygon",
                        "source_timestamp": "2026-06-05T13:30:00+00:00",
                        "fallback_level": "degraded",
                    },
                ]
            }
        ),
        encoding="utf-8",
    )


def _write_lifecycle(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    events = [
        {"signal_id": "sig_NVDA_001", "event_type": "PENDING"},
        {"signal_id": "sig_NVDA_001", "event_type": "TRIGGERED"},
        {"signal_id": "sig_NVDA_001", "event_type": "TARGET_1_HIT"},
        {"signal_id": "sig_QQQ_001", "event_type": "EXPIRED"},
    ]
    path.write_text("\n".join(json.dumps(event) for event in events) + "\n", encoding="utf-8")


def _write_alerts(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"alerts": [{"message": "observation alert"}]}), encoding="utf-8")


def test_p120_observation_report_contains_durable_evidence_schema(tmp_path: Path) -> None:
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
        min_lifecycle_events=2,
        require_alerts=True,
    )
    payload = report.to_dict()

    assert payload["timestamp_utc"]
    assert payload["universe"] == ["NVDA", "QQQ"]
    assert payload["signal_ids"] == ["sig_NVDA_001", "sig_QQQ_001"]
    assert payload["decision_status"] == {"approved": 1, "blocked": 1}
    assert payload["data_quality_status"] == "DEGRADED"
    assert len(payload["provenance"]) == 2


def test_p120_evidence_gate_validates_written_observation_artifact(tmp_path: Path) -> None:
    signals = tmp_path / "signals.json"
    lifecycle = tmp_path / "life.jsonl"
    alerts = tmp_path / "alerts.json"
    json_output = tmp_path / "paper-live-observation.json"
    markdown_output = tmp_path / "paper-live-observation.md"
    _write_signals(signals)
    _write_lifecycle(lifecycle)
    _write_alerts(alerts)

    report = observe_paper_live(
        signals_file=signals,
        lifecycle_file=lifecycle,
        alerts_file=alerts,
        min_lifecycle_events=2,
        require_alerts=True,
    )
    write_paper_live_report(report, json_path=json_output, markdown_path=markdown_output)

    gate = validate_paper_observation_evidence_artifact(json_output)

    assert gate.passed is True
    assert gate.missing_fields == []
    assert gate.invalid_fields == []


def test_p120_evidence_gate_rejects_missing_provenance(tmp_path: Path) -> None:
    artifact = tmp_path / "paper-live-observation.json"
    artifact.write_text(
        json.dumps(
            {
                "timestamp_utc": "2026-06-05T13:30:00+00:00",
                "universe": ["NVDA"],
                "signal_ids": ["sig_NVDA_001"],
                "decision_status": {"approved": 1},
                "data_quality_status": "OK",
                "ready_for_review": True,
                "provenance": [],
            }
        ),
        encoding="utf-8",
    )

    gate = validate_paper_observation_evidence_artifact(artifact)

    assert gate.passed is False
    assert "provenance" in gate.invalid_fields
