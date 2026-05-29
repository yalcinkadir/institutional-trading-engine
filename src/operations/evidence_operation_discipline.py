from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Mapping, Sequence

from src.notifications.telegram_report_dispatcher import RESEARCH_ONLY_FOOTER
from src.reporting.tg2_tg3_report_templates import ReportTemplateType, RenderedReportTemplate


class EvidenceOperationStatus(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"


@dataclass(frozen=True)
class EvidenceOperationConfig:
    require_daily_evidence_passed: bool = True
    require_reconciliation_passed: bool = True
    require_all_tg3_templates: bool = True
    require_telegram_dispatch_records: bool = False
    allowed_modes: tuple[str, ...] = ("observation_only", "paper_observation", "paper_only", "research_only")


@dataclass(frozen=True)
class EvidenceOperationGate:
    name: str
    passed: bool
    value: str | int | bool
    threshold: str | int | bool
    message: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class EvidenceOperationRecord:
    status: EvidenceOperationStatus
    observation_date: str
    observation_mode: str
    gates: list[EvidenceOperationGate] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return self.status == EvidenceOperationStatus.PASS

    def to_dict(self) -> dict[str, Any]:
        return {
            "status": self.status.value,
            "passed": self.passed,
            "observation_date": self.observation_date,
            "observation_mode": self.observation_mode,
            "gates": [gate.to_dict() for gate in self.gates],
            "notes": list(self.notes),
        }


def build_evidence_operation_record(
    *,
    observation_date: str,
    daily_evidence_report: Mapping[str, Any] | Any | None,
    report_templates: Sequence[RenderedReportTemplate | Mapping[str, Any]] = (),
    telegram_dispatch_results: Sequence[Mapping[str, Any] | Any] = (),
    observation_mode: str = "observation_only",
    config: EvidenceOperationConfig = EvidenceOperationConfig(),
) -> EvidenceOperationRecord:
    daily_payload = _to_payload(daily_evidence_report)
    gates = [
        _mode_gate(observation_mode, config),
        _daily_present_gate(daily_payload),
        _daily_pass_gate(daily_payload, config),
        _reconciliation_gate(daily_payload, config),
        _templates_gate(report_templates, config),
        _telegram_dispatch_gate(telegram_dispatch_results, config),
    ]
    status = EvidenceOperationStatus.PASS if all(gate.passed for gate in gates) else EvidenceOperationStatus.FAIL
    return EvidenceOperationRecord(
        status=status,
        observation_date=observation_date,
        observation_mode=observation_mode,
        gates=gates,
        notes=[
            "b1_1_observation_only_evidence_operation",
            "tg2_tg3_report_delivery_integration_only",
            "no_broker_execution",
            "no_live_trading_authorization",
            "no_private_edge_parameters",
        ],
    )


def render_evidence_operation_markdown(record: EvidenceOperationRecord) -> str:
    lines = [
        "# B1.1 Evidence Operation Discipline",
        "",
        f"Date: **{record.observation_date}**",
        f"Mode: **{record.observation_mode}**",
        f"Status: **{record.status.value}**",
        "",
        "## Gates",
        "",
        "| Gate | Status | Value | Threshold |",
        "|---|---:|---:|---:|",
    ]
    for gate in record.gates:
        lines.append(f"| {gate.name} | {'PASS' if gate.passed else 'FAIL'} | {gate.value} | {gate.threshold} |")
    lines.extend(["", "## Notes", ""])
    lines.extend(f"- {note}" for note in record.notes)
    lines.extend(["", RESEARCH_ONLY_FOOTER])
    return "\n".join(lines).rstrip() + "\n"


def write_evidence_operation_record(record: EvidenceOperationRecord, *, json_path: Path, markdown_path: Path) -> None:
    json_path.parent.mkdir(parents=True, exist_ok=True)
    markdown_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(record.to_dict(), indent=2), encoding="utf-8")
    markdown_path.write_text(render_evidence_operation_markdown(record), encoding="utf-8")


def _mode_gate(observation_mode: str, config: EvidenceOperationConfig) -> EvidenceOperationGate:
    normalized = observation_mode.strip().lower()
    blocked_terms = ("live", "real_money", "production_execution")
    passed = normalized in config.allowed_modes and not any(term in normalized for term in blocked_terms)
    return EvidenceOperationGate("observation_only_mode", passed, normalized, "allowed non-live mode", "B1.1 must stay observation-only / paper-only.")


def _daily_present_gate(payload: Mapping[str, Any] | None) -> EvidenceOperationGate:
    return EvidenceOperationGate("daily_evidence_report_present", payload is not None, payload is not None, True, "Daily evidence report must exist.")


def _daily_pass_gate(payload: Mapping[str, Any] | None, config: EvidenceOperationConfig) -> EvidenceOperationGate:
    if not config.require_daily_evidence_passed:
        return EvidenceOperationGate("daily_evidence_passed", True, "not_required", "not_required", "Daily evidence pass gate disabled by config.")
    passed = bool(payload and payload.get("passed", False))
    return EvidenceOperationGate("daily_evidence_passed", passed, passed, True, "Daily evidence report must pass.")


def _reconciliation_gate(payload: Mapping[str, Any] | None, config: EvidenceOperationConfig) -> EvidenceOperationGate:
    if not config.require_reconciliation_passed:
        return EvidenceOperationGate("reconciliation_component_passed", True, "not_required", "not_required", "Reconciliation pass gate disabled by config.")
    component = _find_component(payload, "reconciliation") if payload else None
    passed = bool(component and component.get("status") == "PASS" and component.get("passed", False))
    value = str(component.get("status")) if component else "missing"
    return EvidenceOperationGate("reconciliation_component_passed", passed, value, "PASS", "Daily reconciliation must pass before the observation day is clean.")


def _templates_gate(templates: Sequence[RenderedReportTemplate | Mapping[str, Any]], config: EvidenceOperationConfig) -> EvidenceOperationGate:
    required = {item.value for item in ReportTemplateType}
    present = {_template_type(template) for template in templates}
    missing = sorted(required - present)
    passed = not config.require_all_tg3_templates or not missing
    return EvidenceOperationGate("tg3_report_templates_rendered", passed, len(present), len(required), "TG3 Daily Evidence, Fill Quality, Kill Switch and Backtest Summary templates must be rendered.")


def _telegram_dispatch_gate(results: Sequence[Mapping[str, Any] | Any], config: EvidenceOperationConfig) -> EvidenceOperationGate:
    if not results:
        passed = not config.require_telegram_dispatch_records
        return EvidenceOperationGate("tg2_telegram_dispatch_safe", passed, 0, "optional" if passed else ">=1", "TG2 dispatch records are optional unless required by config.")
    safe_statuses = {"DRY_RUN", "SENT"}
    normalized = [_to_payload(result) or {} for result in results]
    passed = all(str(result.get("status", "")).upper() in safe_statuses and RESEARCH_ONLY_FOOTER in str(result.get("message", "")) for result in normalized)
    return EvidenceOperationGate("tg2_telegram_dispatch_safe", passed, len(normalized), len(normalized), "Telegram dispatches must be safe TG1 research-only dispatches.")


def _find_component(payload: Mapping[str, Any] | None, name: str) -> Mapping[str, Any] | None:
    if not payload:
        return None
    components = payload.get("components", [])
    if not isinstance(components, Sequence):
        return None
    for component in components:
        if isinstance(component, Mapping) and component.get("name") == name:
            return component
    return None


def _template_type(template: RenderedReportTemplate | Mapping[str, Any]) -> str:
    if isinstance(template, RenderedReportTemplate):
        return template.report_type.value
    value = template.get("report_type", "")
    return str(getattr(value, "value", value))


def _to_payload(value: Mapping[str, Any] | Any | None) -> dict[str, Any] | None:
    if value is None:
        return None
    if isinstance(value, Mapping):
        return dict(value)
    if hasattr(value, "to_dict"):
        return value.to_dict()
    return None
