"""Entry/Exit Watcher health diagnostics.

P30 improves observability around watcher artifacts. It does not place orders,
call a broker, or change watcher execution behavior.
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
class WatcherHealthGate:
    name: str
    passed: bool
    message: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class WatcherHealthReport:
    healthy: bool
    signal_count: int
    buy_watch_count: int
    lifecycle_event_count: int
    terminal_event_count: int
    malformed_lifecycle_lines: int
    lifecycle_event_types: dict[str, int] = field(default_factory=dict)
    gates: list[WatcherHealthGate] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "healthy": self.healthy,
            "signal_count": self.signal_count,
            "buy_watch_count": self.buy_watch_count,
            "lifecycle_event_count": self.lifecycle_event_count,
            "terminal_event_count": self.terminal_event_count,
            "malformed_lifecycle_lines": self.malformed_lifecycle_lines,
            "lifecycle_event_types": self.lifecycle_event_types,
            "gates": [gate.to_dict() for gate in self.gates],
            "notes": self.notes,
        }


def _load_signals(path: Path) -> tuple[list[dict[str, Any]], str | None]:
    if not path.exists():
        return [], "signals file is missing"
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [], f"signals file is malformed JSON: {exc}"
    if isinstance(payload, list):
        return [item for item in payload if isinstance(item, dict)], None
    if isinstance(payload, dict) and isinstance(payload.get("signals"), list):
        return [item for item in payload["signals"] if isinstance(item, dict)], None
    return [], "signals payload must be a list or contain a signals list"


def _load_lifecycle(path: Path) -> tuple[list[dict[str, Any]], int, str | None]:
    if not path.exists():
        return [], 0, "lifecycle file is missing"
    events: list[dict[str, Any]] = []
    malformed = 0
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            payload = json.loads(line)
        except json.JSONDecodeError:
            malformed += 1
            continue
        if isinstance(payload, dict):
            events.append(payload)
        else:
            malformed += 1
    return events, malformed, None


def _event_type(event: dict[str, Any]) -> str:
    return str(event.get("event_type") or event.get("type") or event.get("status") or "UNKNOWN")


def run_entry_exit_watcher_health_check(
    *,
    signals_file: Path = Path("reports/signals/latest-signals.json"),
    lifecycle_file: Path = Path("data/signal_lifecycle.jsonl"),
    min_signals: int = 1,
    min_lifecycle_events: int = 1,
    require_terminal_event: bool = False,
) -> WatcherHealthReport:
    signals, signal_error = _load_signals(signals_file)
    lifecycle_events, malformed_lifecycle_lines, lifecycle_error = _load_lifecycle(lifecycle_file)

    event_counts: dict[str, int] = {}
    for event in lifecycle_events:
        name = _event_type(event)
        event_counts[name] = event_counts.get(name, 0) + 1

    terminal_event_count = sum(count for name, count in event_counts.items() if name in TERMINAL_EVENTS)
    buy_watch_count = sum(1 for signal in signals if signal.get("action") == "BUY_WATCH")

    gates = [
        WatcherHealthGate(
            name="signals_file_present_and_parseable",
            passed=signal_error is None,
            message=signal_error or f"signals loaded: {len(signals)}",
        ),
        WatcherHealthGate(
            name="minimum_signals_loaded",
            passed=len(signals) >= min_signals,
            message=f"signals: {len(signals)} / required: {min_signals}",
        ),
        WatcherHealthGate(
            name="lifecycle_file_present_and_parseable",
            passed=lifecycle_error is None,
            message=lifecycle_error or f"lifecycle events loaded: {len(lifecycle_events)}",
        ),
        WatcherHealthGate(
            name="minimum_lifecycle_events_loaded",
            passed=len(lifecycle_events) >= min_lifecycle_events,
            message=f"lifecycle events: {len(lifecycle_events)} / required: {min_lifecycle_events}",
        ),
        WatcherHealthGate(
            name="no_malformed_lifecycle_lines",
            passed=malformed_lifecycle_lines == 0,
            message=f"malformed lifecycle lines: {malformed_lifecycle_lines}",
        ),
    ]
    if require_terminal_event:
        gates.append(
            WatcherHealthGate(
                name="terminal_event_observed",
                passed=terminal_event_count > 0,
                message=f"terminal events: {terminal_event_count}",
            )
        )

    healthy = all(gate.passed for gate in gates)
    return WatcherHealthReport(
        healthy=healthy,
        signal_count=len(signals),
        buy_watch_count=buy_watch_count,
        lifecycle_event_count=len(lifecycle_events),
        terminal_event_count=terminal_event_count,
        malformed_lifecycle_lines=malformed_lifecycle_lines,
        lifecycle_event_types=dict(sorted(event_counts.items())),
        gates=gates,
        notes=[
            "Watcher health check is diagnostics only.",
            "No broker call or order execution is performed.",
        ],
    )


def render_watcher_health_markdown(report: WatcherHealthReport) -> str:
    lines = [
        "# Entry/Exit Watcher Health Report",
        "",
        f"Healthy: `{report.healthy}`",
        "",
        "## Summary",
        "",
        f"- Signals: {report.signal_count}",
        f"- BUY_WATCH signals: {report.buy_watch_count}",
        f"- Lifecycle events: {report.lifecycle_event_count}",
        f"- Terminal events: {report.terminal_event_count}",
        f"- Malformed lifecycle lines: {report.malformed_lifecycle_lines}",
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
    for name, count in report.lifecycle_event_types.items():
        lines.append(f"| {name} | {count} |")
    lines.extend(["", "## Notes", ""])
    for note in report.notes:
        lines.append(f"- {note}")
    return "\n".join(lines) + "\n"


def write_watcher_health_report(report: WatcherHealthReport, *, json_path: Path, markdown_path: Path) -> None:
    json_path.parent.mkdir(parents=True, exist_ok=True)
    markdown_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(report.to_dict(), indent=2), encoding="utf-8")
    markdown_path.write_text(render_watcher_health_markdown(report), encoding="utf-8")
