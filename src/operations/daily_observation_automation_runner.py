from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any, Iterable, Mapping

from src.operations.daily_observation_record_artifact_contract import build_daily_observation_record_path
from src.operations.daily_observation_record_index import build_daily_observation_record_index
from src.operations.daily_observation_record_writer import build_daily_observation_record
from src.operations.daily_observation_review_summary import build_daily_observation_review_summary
from src.operations.paper_observation_review_gate import evaluate_paper_observation_review_gate

AUTOMATION_ARTIFACT_ROOT = Path("reports/daily_observation_automation")
AUTOMATION_STATUS_PASSED = "PASSED"
AUTOMATION_STATUS_BLOCKED = "BLOCKED"


@dataclass(frozen=True)
class DailyObservationAutomationRunnerResult:
    valid: bool
    errors: tuple[str, ...]
    artifact_path: str
    artifact: dict[str, Any]


def build_daily_observation_automation_artifact_path(observation_date: str | date) -> Path:
    if isinstance(observation_date, date):
        date_value = observation_date.isoformat()
    else:
        date_value = observation_date
    return AUTOMATION_ARTIFACT_ROOT / f"{date_value}.json"


def build_daily_observation_automation_artifact(
    *,
    observation_date: str | date,
    existing_records: Iterable[Mapping[str, Any]] | None = None,
    missing_evidence: Iterable[str] | None = None,
    incidents: Iterable[str] | None = None,
    artifact_paths: Iterable[str] | None = None,
    review_notes: str = "",
    minimum_records: int = 1,
    created_at: str | None = None,
    require_artifact_paths_exist: bool = False,
    artifact_root: str | Path | None = None,
) -> DailyObservationAutomationRunnerResult:
    """Build the deterministic PO10 daily observation automation artifact.

    PO10 connects the already validated Paper Observation chain:

    PO5 Daily Observation Record Writer
    PO7 Daily Observation Record Index
    PO8 Daily Observation Review Summary
    PO9 Paper Observation Review Gate

    The runner never authorizes live trading or broker execution.
    """

    errors: list[str] = []

    record = build_daily_observation_record(
        observation_date=observation_date,
        missing_evidence=missing_evidence,
        incidents=incidents,
        artifact_paths=artifact_paths,
        review_notes=review_notes,
        created_at=created_at,
        require_artifact_paths_exist=require_artifact_paths_exist,
        artifact_root=artifact_root,
    )

    records = [dict(record) for record in existing_records or []]
    records.append(record)

    index_result = build_daily_observation_record_index(records)
    errors.extend(f"index:{error}" for error in index_result.errors)

    summary_result = build_daily_observation_review_summary(index_result.index)
    errors.extend(f"summary:{error}" for error in summary_result.errors)

    gate_result = evaluate_paper_observation_review_gate(
        summary_result.summary,
        minimum_records=minimum_records,
    )

    artifact_path = build_daily_observation_automation_artifact_path(str(record["date"]))
    record_path = build_daily_observation_record_path(str(record["date"]))

    automation_status = AUTOMATION_STATUS_PASSED if gate_result.approved_for_review else AUTOMATION_STATUS_BLOCKED

    artifact = {
        "observation_date": record["date"],
        "automation_status": automation_status,
        "record_path": str(record_path),
        "index_path": index_result.index.get("index_path"),
        "summary": summary_result.summary,
        "gate": gate_result.gate,
        "errors": tuple(errors),
        "live_trading_authorized": False,
        "broker_execution_mode": "paper_only",
    }

    valid = not errors and gate_result.valid and automation_status == AUTOMATION_STATUS_PASSED

    return DailyObservationAutomationRunnerResult(
        valid=valid,
        errors=tuple(errors),
        artifact_path=str(artifact_path),
        artifact=artifact,
    )


def write_daily_observation_automation_artifact(
    *,
    result: DailyObservationAutomationRunnerResult,
    output_path: str | Path | None = None,
    indent: int = 2,
) -> DailyObservationAutomationRunnerResult:
    path = Path(output_path) if output_path is not None else Path(result.artifact_path)
    expected_path = Path(result.artifact_path)

    if path != expected_path:
        artifact = dict(result.artifact)
        errors = tuple(result.errors) + ("automation_artifact_path_must_be_canonical",)
        artifact["errors"] = errors
        return DailyObservationAutomationRunnerResult(
            valid=False,
            errors=errors,
            artifact_path=result.artifact_path,
            artifact=artifact,
        )

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result.artifact, indent=indent, sort_keys=True) + "\n", encoding="utf-8")
    return result
