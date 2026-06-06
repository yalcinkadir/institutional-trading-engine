"""Paper-live observation before trading.

P26 is an operational readiness layer. It reads local artifacts and produces a
report. It never places orders and never contacts a broker.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
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

DATA_QUALITY_ORDER = {"OK": 0, "DEGRADED": 1, "UNKNOWN": 2, "BLOCKED": 3}


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
    timestamp_utc: str
    universe: list[str]
    signal_ids: list[str]
    decision_status: dict[str, int]
    data_quality_status: str
    provenance: list[dict[str, Any]]
    gates: list[PaperLiveGate] = field(default_factory=list)
    lifecycle_event_types: dict[str, int] = field(default_factory=dict)
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "timestamp_utc": self.timestamp_utc,
            "ready_for_review": self.ready_for_review,
            "signal_count": self.signal_count,
            "buy_watch_count": self.buy_watch_count,
            "lifecycle_event_count": self.lifecycle_event_count,
            "terminal_event_count": self.terminal_event_count,
            "alert_count": self.alert_count,
            "universe": self.universe,
            "signal_ids": self.signal_ids,
            "decision_status": self.decision_status,
            "data_quality_status": self.data_quality_status,
            "provenance": self.provenance,
            "gates": [gate.to_dict() for gate in self.gates],
            "lifecycle_event_types": self.lifecycle_event_types,
            "notes": self.notes,
        }


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _read_signal_payload(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    payload = _read_json(path)
    if isinstance(payload, dict):
        return payload
    if isinstance(payload, list):
        return {"signals": [item for item in payload if isinstance(item, dict)]}
    return {}


def _read_signals(path: Path) -> list[dict[str, Any]]:
    payload = _read_signal_payload(path)
    if isinstance(payload.get("signals"), list):
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


def _signal_id(signal: dict[str, Any]) -> str:
    return str(signal.get("signal_id") or signal.get("id") or signal.get("symbol") or "UNKNOWN")


def _decision_status(signal: dict[str, Any]) -> str:
    return str(signal.get("decision") or signal.get("status") or signal.get("action") or "UNKNOWN")


def _data_quality_status(signals: list[dict[str, Any]]) -> str:
    if not signals:
        return "BLOCKED"
    worst = "OK"
    for signal in signals:
        status = str(signal.get("data_status") or signal.get("data_quality_status") or "UNKNOWN")
        status = status if status in DATA_QUALITY_ORDER else "UNKNOWN"
        if DATA_QUALITY_ORDER[status] > DATA_QUALITY_ORDER[worst]:
            worst = status
    return worst


def _build_provenance(signals: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "signal_id": _signal_id(signal),
            "symbol": str(signal.get("symbol") or "UNKNOWN"),
            "source": str(signal.get("source") or "UNKNOWN"),
            "source_timestamp": str(signal.get("source_timestamp") or signal.get("generated_at") or "UNKNOWN"),
            "fallback_level": str(signal.get("fallback_level") or "UNKNOWN"),
            "data_status": str(signal.get("data_status") or signal.get("data_quality_status") or "UNKNOWN"),
        }
        for signal in signals
    ]


def _paper_observation_health_gate(payload: dict[str, Any], signals: list[dict[str, Any]]) -> PaperLiveGate:
    reasons: list[str] = []
    total = len(signals)
    if total == 0:
        return PaperLiveGate("paper_observation_health", False, "no_signals_loaded")

    close_missing = sum(1 for signal in signals if signal.get("close") is None)
    atr_missing = sum(1 for signal in signals if signal.get("atr14") is None)
    if close_missing == total or close_missing / total >= 0.8:
        reasons.append("all_or_most_close_missing")
    if atr_missing == total or atr_missing / total >= 0.8:
        reasons.append("all_or_most_atr_missing")

    market_regime = str(payload.get("market_regime") or "Unknown")
    has_available_data = close_missing < total and atr_missing < total
    if market_regime == "Unknown" and has_available_data:
        reasons.append("unknown_market_regime_with_available_data")

    data_quality = payload.get("data_quality") if isinstance(payload.get("data_quality"), dict) else {}
    missing_symbols = data_quality.get("missing_symbols") or []
    missing_required_fields = data_quality.get("missing_required_fields") or {}
    if missing_symbols:
        reasons.append("scanner_metrics_missing_for_core_symbols")
    if missing_required_fields:
        reasons.append("scanner_metrics_missing_required_fields")

    actionable_count = int(payload.get("actionable_count") or 0)
    if actionable_count == 0 and (missing_required_fields or close_missing > 0 or atr_missing > 0):
        reasons.append("zero_actionable_due_to_missing_required_data")

    if reasons:
        return PaperLiveGate("paper_observation_health", False, ",".join(sorted(set(reasons))))
    return PaperLiveGate("paper_observation_health", True, "paper observation sees complete market data or valid no-trade conditions")


def observe_paper_live(
    *,
    signals_file: Path = Path("reports/signals/latest-signals.json"),
    lifecycle_file: Path = Path("data/signal_lifecycle.jsonl"),
    alerts_file: Path = Path("reports/alerts/latest-alerts.json"),
    min_lifecycle_events: int = 5,
    require_alerts: bool = False,
) -> PaperLiveObservationReport:
    signal_payload = _read_signal_payload(signals_file)
    signals = _read_signals(signals_file)
    lifecycle_events = _read_lifecycle_events(lifecycle_file)
    alerts = _read_alerts(alerts_file)

    event_counts: dict[str, int] = {}
    for event in lifecycle_events:
        event_name = _event_type(event)
        event_counts[event_name] = event_counts.get(event_name, 0) + 1

    terminal_count = sum(count for event, count in event_counts.items() if event in TERMINAL_EVENTS)
    buy_watch_count = sum(1 for signal in signals if signal.get("action") == "BUY_WATCH")
    universe = sorted({str(signal.get("symbol")) for signal in signals if signal.get("symbol")})
    signal_ids = sorted(_signal_id(signal) for signal in signals)
    decision_status: dict[str, int] = {}
    for signal in signals:
        decision = _decision_status(signal)
        decision_status[decision] = decision_status.get(decision, 0) + 1
    provenance = _build_provenance(signals)

    gates = [
        PaperLiveGate("signals_file_present", signals_file.exists(), f"signals file: {signals_file}"),
        PaperLiveGate("signals_loaded", len(signals) > 0, f"signals loaded: {len(signals)}"),
        PaperLiveGate(
            "observation_evidence_schema",
            bool(universe and signal_ids and decision_status and provenance),
            "observation artifact includes universe, signal ids, decision status and provenance",
        ),
        _paper_observation_health_gate(signal_payload, signals),
        PaperLiveGate("lifecycle_file_readable", lifecycle_file.exists(), f"lifecycle file: {lifecycle_file}"),
        PaperLiveGate(
            "minimum_lifecycle_events",
            len(lifecycle_events) >= min_lifecycle_events,
            f"lifecycle events: {len(lifecycle_events)} / required: {min_lifecycle_events}",
        ),
        PaperLiveGate("terminal_events_observed", terminal_count > 0, f"terminal events observed: {terminal_count}"),
    ]

    if require_alerts:
        gates.append(PaperLiveGate("alerts_observed", len(alerts) > 0, f"alerts observed: {len(alerts)}"))

    notes = [
        "Paper-live observation is decision-support evidence only.",
        "This report does not authorize trading or broker execution.",
    ]
    return PaperLiveObservationReport(
        ready_for_review=all(gate.passed for gate in gates),
        signal_count=len(signals),
        buy_watch_count=buy_watch_count,
        lifecycle_event_count=len(lifecycle_events),
        terminal_event_count=terminal_count,
        alert_count=len(alerts),
        timestamp_utc=datetime.now(UTC).isoformat(),
        universe=universe,
        signal_ids=signal_ids,
        decision_status=dict(sorted(decision_status.items())),
        data_quality_status=_data_quality_status(signals),
        provenance=provenance,
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
        f"- Data quality status: {report.data_quality_status}",
        "",
        "## Gates",
        "",
        "| Gate | Status | Message |",
        "|---|---:|---|",
    ]
    for gate in report.gates:
        status = "PASS" if gate.passed else "FAIL"
        lines.append(f"| {gate.name} | {status} | {gate.message} |")
    lines.extend(["", "## Lifecycle Event Types", "", "| Event | Count |", "|---|---:"])
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
