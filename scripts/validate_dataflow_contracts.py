#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(frozen=True)
class ContractReport:
    stage: str
    passed: bool
    missing_fields: list[str] = field(default_factory=list)
    invalid_fields: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class ContractViolation(ValueError):
    def __init__(self, report: ContractReport) -> None:
        super().__init__(f"contract failed for {report.stage}")
        self.report = report


def _get(payload: Any, field: str) -> Any:
    if isinstance(payload, dict):
        return payload.get(field)
    return getattr(payload, field, None)


def _has(payload: Any, field: str) -> bool:
    return field in payload if isinstance(payload, dict) else hasattr(payload, field)


def _present(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, (list, dict)):
        return bool(value)
    return True


def _validate(stage: str, payload: Any, required: list[str]) -> ContractReport:
    missing = [field for field in required if not _has(payload, field)]
    invalid = [field for field in required if field not in missing and not _present(_get(payload, field))]
    report = ContractReport(stage, not missing and not invalid, missing, invalid)
    if not report.passed:
        raise ContractViolation(report)
    return report


def validate_signal_contract(signal: Any) -> ContractReport:
    required = [
        "signal_id",
        "symbol",
        "action",
        "setup_type",
        "decision",
        "market_regime",
        "generated_at",
        "data_status",
        "source",
        "source_timestamp",
        "fallback_level",
    ]
    report = _validate("signal", signal, required)
    if str(_get(signal, "action") or "") == "BUY_WATCH":
        invalid = [field for field in ["entry_trigger", "stop_loss", "target_1"] if not _present(_get(signal, field))]
        if invalid:
            raise ContractViolation(ContractReport("signal", False, [], invalid))
    return report


def validate_decision_report_contract(payload: dict[str, Any]) -> ContractReport:
    return _validate(
        "decision_report",
        payload,
        ["market_state", "summary", "run_health", "scanner_data_quality", "signal_generation_status", "decisions"],
    )


def validate_paper_observation_contract(payload: dict[str, Any]) -> ContractReport:
    report = _validate(
        "paper_observation",
        payload,
        ["timestamp_utc", "ready_for_review", "universe", "signal_ids", "decision_status", "data_quality_status", "provenance"],
    )
    if not _has(payload, "gates"):
        raise ContractViolation(ContractReport("paper_observation", False, ["gates"], []))
    gates = payload.get("gates") or []
    if not any(isinstance(gate, dict) and gate.get("name") == "paper_observation_health" for gate in gates):
        raise ContractViolation(ContractReport("paper_observation", False, [], ["paper_observation_health_gate"]))
    return report


def validate_backtest_evidence_contract(payload: dict[str, Any]) -> ContractReport:
    return _validate(
        "backtest_evidence",
        payload,
        ["run_id", "data_source", "symbol_universe", "date_range", "strategy_version", "input_pack_gate_status", "input_completeness_status", "run_health_status", "input_plan_count", "accepted_plan_count", "rejected_plan_count", "metrics", "results"],
    )
