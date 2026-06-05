#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

REQUIRED_ARTIFACT_FIELDS = [
    "timestamp_utc",
    "universe",
    "signal_ids",
    "decision_status",
    "data_quality_status",
    "provenance",
    "ready_for_review",
]

REQUIRED_PROVENANCE_FIELDS = [
    "signal_id",
    "symbol",
    "source",
    "source_timestamp",
    "fallback_level",
    "data_status",
]

VALID_DATA_QUALITY_STATUSES = {"OK", "DEGRADED", "BLOCKED", "UNKNOWN"}


@dataclass(frozen=True)
class PaperObservationEvidenceGateReport:
    passed: bool
    artifact_path: str
    missing_fields: list[str] = field(default_factory=list)
    invalid_fields: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _load_payload(path: Path) -> tuple[dict[str, Any] | None, list[str]]:
    if not path.exists():
        return None, ["artifact_missing"]
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return None, [f"invalid_json: {exc}"]
    if not isinstance(payload, dict):
        return None, ["artifact_not_object"]
    return payload, []


def _is_non_empty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _validate_provenance(provenance: Any) -> bool:
    if not isinstance(provenance, list) or not provenance:
        return False
    for record in provenance:
        if not isinstance(record, dict):
            return False
        for field_name in REQUIRED_PROVENANCE_FIELDS:
            if field_name not in record:
                return False
        if not _is_non_empty_string(record.get("signal_id")):
            return False
        if not _is_non_empty_string(record.get("symbol")):
            return False
        if not _is_non_empty_string(record.get("source")):
            return False
        if not _is_non_empty_string(record.get("source_timestamp")):
            return False
        if not _is_non_empty_string(record.get("fallback_level")):
            return False
        if record.get("data_status") not in VALID_DATA_QUALITY_STATUSES:
            return False
    return True


def validate_paper_observation_evidence_artifact(path: Path) -> PaperObservationEvidenceGateReport:
    payload, errors = _load_payload(path)
    if payload is None:
        return PaperObservationEvidenceGateReport(
            passed=False,
            artifact_path=path.as_posix(),
            errors=errors,
        )

    missing_fields = [field_name for field_name in REQUIRED_ARTIFACT_FIELDS if field_name not in payload]
    invalid_fields: list[str] = []

    if "timestamp_utc" in payload and not _is_non_empty_string(payload.get("timestamp_utc")):
        invalid_fields.append("timestamp_utc")
    if "universe" in payload and not (
        isinstance(payload.get("universe"), list)
        and payload["universe"]
        and all(_is_non_empty_string(symbol) for symbol in payload["universe"])
    ):
        invalid_fields.append("universe")
    if "signal_ids" in payload and not (
        isinstance(payload.get("signal_ids"), list)
        and payload["signal_ids"]
        and all(_is_non_empty_string(signal_id) for signal_id in payload["signal_ids"])
    ):
        invalid_fields.append("signal_ids")
    if "decision_status" in payload and not isinstance(payload.get("decision_status"), dict):
        invalid_fields.append("decision_status")
    if "data_quality_status" in payload and payload.get("data_quality_status") not in VALID_DATA_QUALITY_STATUSES:
        invalid_fields.append("data_quality_status")
    if "ready_for_review" in payload and not isinstance(payload.get("ready_for_review"), bool):
        invalid_fields.append("ready_for_review")
    if "provenance" in payload and not _validate_provenance(payload.get("provenance")):
        invalid_fields.append("provenance")

    return PaperObservationEvidenceGateReport(
        passed=not missing_fields and not invalid_fields and not errors,
        artifact_path=path.as_posix(),
        missing_fields=missing_fields,
        invalid_fields=invalid_fields,
        errors=errors,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate paper observation evidence artifact schema.")
    parser.add_argument("--artifact", default="reports/paper-live/paper-live-observation.json")
    parser.add_argument("--report-output", default="reports/paper-live/paper-observation-evidence-gate.json")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    report = validate_paper_observation_evidence_artifact(Path(args.artifact))
    output = Path(args.report_output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report.to_dict(), indent=2), encoding="utf-8")

    status = "PASS" if report.passed else "FAIL"
    print(f"Paper observation evidence gate status: {status}")
    print(f"Artifact: {report.artifact_path}")
    if report.missing_fields:
        print(f"Missing fields: {', '.join(report.missing_fields)}")
    if report.invalid_fields:
        print(f"Invalid fields: {', '.join(report.invalid_fields)}")
    if report.errors:
        print(f"Errors: {', '.join(report.errors)}")
    print(f"Gate report: {args.report_output}")
    return 0 if report.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
