"""Paper-live observation before trading.

P26 is an operational readiness layer. It reads local artifacts and produces a
report. It never places orders and never contacts a broker.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any


TERMINAL_EVENTS = {
    "STOP_HIT",
    "TARGET_1_HIT",
    "TARGET_2_HIT",
    "EXPIRED",
    "CANCELLED_BY_REGIME_CHANGE",
    "REGIME_INVALIDATION_EXIT",
}


@dataclass(frozen=True)
class PaperLiveGate:
    name: str
    passed: bool
    message: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class PaperLiveObservationReport:
    ready_for_review: bool
    signal_count: int
    buy_watch_count: int
    lifecycle_event_count: int
    terminal_event_count: int
    alert_count: int
    gates: list[PaperLiveGate] = field(default_factory=list)
    lifecycle_event_types: dict[str, int] = field(default_factory=dict)
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "ready_for_review": self.ready_for_review,
            "signal_count": self.signal_count,
            "buy_watch_count": self.buy_watch_count,
            "lifecycle_event_count": self.lifecycle_event_count,
            "terminal_event_count": self.terminal_event_count,
            "alert_count": self.alert_count,
            "gates": [gate.to_dict() for gate in self.gates],
            "lifecycle_event_types": self.lifecycle_event_types,
            "notes": self.notes,
        }


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _read_signals(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    payload = _read_json(path)
    if isinstance(payload, list):
        return [item for item in payload if isinstance(item, dict)]
    if isinstance(payload, dict) and isinstance(payload.get("signals"), list):
        return [item for item in payload["signals"] if isinstance(item, dict)]
    return []


def _read_lifecycle_events(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    events: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            payload = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(payload, dict):
            events.append(payload)
    return events


def _read_alerts(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    payload = _read_json(path)
    if isinstance(payload, list):
        return [item for item in payload if isinstance(item, dict)]
    if isinstance(payload, dict) and isinstance(payload.get("alerts"), list):
        return [item for item in payload["alerts"] if isinstance(item, dict)]
    return []


def _event_type(event: dict[str, Any]) -> str:
    return str(event.get("event_type") or event.get("type") or event.get("status") or "UNKNOWN")


def observe_paper_live(
    *,
    signals_file: Path = Path("reports/signals/latest-signals.json"),
    lifecycle_file: Path = Path("data/signal_lifecycle.jsonl"),
    alerts_file: Path = Path("reports/alerts/latest-alerts.json"),
    min_lifecycle_events: int = 5,
    require_alerts: bool = False,
) -> PaperLiveObservationReport:
    signals = _read_signals(signals_file)
    lifecycle_events = _read_lifecycle_events(lifecycle_file)
    alerts = _read_alerts(alerts_file)

    event_counts: dict[str, int] = {}
    for event in lifecycle_events:
        event_name = _event_type(event)
        event_counts[event_name] = event_counts.get(event_name, 0) + 1

    terminal_count = sum(count for event, count in event_counts.items() if event in TERMINAL_EVENTS)
    buy_watch_count = sum(1 for signal in signals if signal.get("action") == "BUY_WATCH")

    gates = [
        PaperLiveGate(
            name="signals_file_present",
            passed=signals_file.exists(),
            message=f"signals file: {signals_file}",
        ),
        PaperLiveGate(
            name="signals_loaded",
            passed=len(signals) > 0,
            message=f"signals loaded: {len(signals)}",
        ),
        PaperLiveGate(
            name="lifecycle_file_readable",
            passed=lifecycle_file.exists(),
            message=f"lifecycle file: {lifecycle_file}",
        ),
        PaperLiveGate(
            name="minimum_lifecycle_events",
            passed=len(lifecycle_events) >= min_lifecycle_events,
            message=f"lifecycle events: {len(lifecycle_events)} / required: {min_lifecycle_events}",
        ),
        PaperLiveGate(
            name="terminal_events_observed",
            passed=terminal_count > 0,
            message=f"terminal events observed: {terminal_count}",
        ),
    ]

    if require_alerts:
        gates.append(
            PaperLiveGate(
                name="alerts_observed",
                passed=len(alerts) > 0,
                message=f"alerts observed: {len(alerts)}",
            )
        )

    ready = all(gate.passed for gate in gates)
    notes = [
        "Paper-live observation is decision-support evidence only.",
        "This report does not authorize trading or broker execution.",
    ]
    return PaperLiveObservationReport(
        ready_for_review=ready,
        signal_count=len(signals),
        buy_watch_count=buy_watch_count,
        lifecycle_event_count=len(lifecycle_events),
        terminal_event_count=terminal_count,
        alert_count=len(alerts),
        gates=gates,
        lifecycle_event_types=dict(sorted(event_counts.items())),
        notes=notes,
    )


def render_paper_live_markdown(report: PaperLiveObservationReport) -> str:
    lines = [
        "# Paper-Live Observation Report",
        "",
        f"Ready for review: `{report.ready_for_review}`",
        "",
        "## Summary",
        "",
        f"- Signals: {report.signal_count}",
        f"- BUY_WATCH signals: {report.buy_watch_count}",
        f"- Lifecycle events: {report.lifecycle_event_count}",
        f"- Terminal events: {report.terminal_event_count}",
        f"- Alerts: {report.alert_count}",
        "",
        "## Gates",
        "",
        "| Gate | Status | Message |",
        "|---|---:|---|",
    ]
    for gate in report.gates:
        status = "PASS" if gate.passed else "FAIL"
        lines.append(f"| {gate.name} | {status} | {gate.message} |")
    lines.extend(["", "## Lifecycle Event Types", "", "| Event | Count |", "|---|---:|"])
    for event, count in report.lifecycle_event_types.items():
        lines.append(f"| {event} | {count} |")
    lines.extend(["", "## Guardrail", ""])
    for note in report.notes:
        lines.append(f"- {note}")
    return "\n".join(lines) + "\n"


def write_paper_live_report(report: PaperLiveObservationReport, *, json_path: Path, markdown_path: Path) -> None:
    json_path.parent.mkdir(parents=True, exist_ok=True)
    markdown_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(report.to_dict(), indent=2), encoding="utf-8")
    markdown_path.write_text(render_paper_live_markdown(report), encoding="utf-8")
