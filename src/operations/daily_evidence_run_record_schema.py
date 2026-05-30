"""Validation helpers for B1.1 daily evidence run records."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

SCHEMA_VERSION = "b11_daily_evidence_run_record_v1"
RECORD_TYPE = "daily_evidence_run_record"
RESEARCH_MODE = "paper_observation_only"

REQUIRED_TOP_LEVEL_FIELDS = frozenset(
    {
        "schema_version",
        "record_type",
        "record_id",
        "commit_sha",
        "run_date_utc",
        "created_at_utc",
        "research_mode",
        "environment",
        "source_summary",
        "input_summary",
        "output_summary",
        "reconciliation_summary",
        "notification_summary",
        "exception_summary",
        "manual_override_summary",
        "sharing_summary",
        "review_summary",
    }
)

REQUIRED_NESTED_FIELDS: Mapping[str, frozenset[str]] = {
    "environment": frozenset(
        {
            "provider_mode",
            "ci_context",
            "local_context",
            "python_version",
            "dependency_snapshot_status",
        }
    ),
    "source_summary": frozenset(
        {
            "source_name",
            "source_status",
            "source_fingerprint",
            "missing_data_count",
            "provider_warning_count",
        }
    ),
    "input_summary": frozenset(
        {
            "input_status",
            "input_fingerprint",
            "validation_status",
            "validation_error_count",
        }
    ),
    "output_summary": frozenset(
        {
            "output_status",
            "output_fingerprint",
            "runtime_report_path",
            "generated_artifact_count",
        }
    ),
    "reconciliation_summary": frozenset(
        {
            "reconciliation_status",
            "drift_status",
            "unmatched_record_count",
            "reconciliation_note",
        }
    ),
    "notification_summary": frozenset(
        {
            "notification_status",
            "dispatch_record_path",
            "content_review_status",
        }
    ),
    "exception_summary": frozenset({"exception_status", "exception_record_path"}),
    "manual_override_summary": frozenset(
        {"manual_override_status", "manual_override_rationale"}
    ),
    "sharing_summary": frozenset(
        {"repository_status", "example_data_status", "review_status"}
    ),
    "review_summary": frozenset(
        {"review_status", "reviewer", "reviewed_at_utc", "review_note"}
    ),
}


@dataclass(frozen=True)
class RunRecordValidationResult:
    """Result for B1.1 daily evidence run record validation."""

    is_valid: bool
    errors: tuple[str, ...]


def _is_non_empty(value: Any) -> bool:
    return value is not None and value != ""


def _missing_fields(record: Mapping[str, Any], fields: frozenset[str]) -> tuple[str, ...]:
    return tuple(sorted(field for field in fields if not _is_non_empty(record.get(field))))


def validate_daily_evidence_run_record(
    record: Mapping[str, Any],
) -> RunRecordValidationResult:
    """Validate the canonical B1.1 daily evidence run record structure."""

    errors: list[str] = []

    for field in _missing_fields(record, REQUIRED_TOP_LEVEL_FIELDS):
        errors.append(f"missing_top_level_field:{field}")

    if record.get("schema_version") != SCHEMA_VERSION:
        errors.append("invalid_schema_version")
    if record.get("record_type") != RECORD_TYPE:
        errors.append("invalid_record_type")
    if record.get("research_mode") != RESEARCH_MODE:
        errors.append("invalid_research_mode")

    for block_name, required_fields in REQUIRED_NESTED_FIELDS.items():
        block = record.get(block_name)
        if not isinstance(block, Mapping):
            errors.append(f"missing_or_invalid_block:{block_name}")
            continue
        for field in _missing_fields(block, required_fields):
            errors.append(f"missing_nested_field:{block_name}.{field}")

    output_summary = record.get("output_summary")
    if isinstance(output_summary, Mapping):
        output_status = output_summary.get("output_status")
        output_fingerprint = output_summary.get("output_fingerprint")
        if output_status == "generated" and not _is_non_empty(output_fingerprint):
            errors.append("missing_output_fingerprint_for_generated_output")

    sharing_summary = record.get("sharing_summary")
    if isinstance(sharing_summary, Mapping):
        if sharing_summary.get("repository_status") != "reviewed":
            errors.append("repository_status_not_reviewed")

    manual_override_summary = record.get("manual_override_summary")
    if isinstance(manual_override_summary, Mapping):
        override_status = manual_override_summary.get("manual_override_status")
        rationale = manual_override_summary.get("manual_override_rationale")
        if override_status not in (None, "none", "not_applicable") and not _is_non_empty(rationale):
            errors.append("manual_override_without_rationale")

    return RunRecordValidationResult(is_valid=not errors, errors=tuple(errors))
