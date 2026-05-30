from src.operations.daily_evidence_run_record_schema import (
    RECORD_TYPE,
    RESEARCH_MODE,
    SCHEMA_VERSION,
    validate_daily_evidence_run_record,
)


def _valid_record() -> dict:
    return {
        "schema_version": SCHEMA_VERSION,
        "record_type": RECORD_TYPE,
        "record_id": "2026-05-30-demo-record",
        "commit_sha": "abc123",
        "run_date_utc": "2026-05-30",
        "created_at_utc": "2026-05-30T00:00:00Z",
        "research_mode": RESEARCH_MODE,
        "environment": {
            "provider_mode": "paper",
            "ci_context": "github_actions",
            "local_context": "not_applicable",
            "python_version": "3.11",
            "dependency_snapshot_status": "captured",
        },
        "source_summary": {
            "source_name": "synthetic_fixture",
            "source_status": "complete",
            "source_fingerprint": "source-fp",
            "missing_data_count": 0,
            "provider_warning_count": 0,
        },
        "input_summary": {
            "input_status": "valid",
            "input_fingerprint": "input-fp",
            "validation_status": "passed",
            "validation_error_count": 0,
        },
        "output_summary": {
            "output_status": "generated",
            "output_fingerprint": "output-fp",
            "runtime_report_path": "reports/local/daily.md",
            "generated_artifact_count": 1,
        },
        "reconciliation_summary": {
            "reconciliation_status": "clean",
            "drift_status": "none",
            "unmatched_record_count": 0,
            "reconciliation_note": "ok",
        },
        "notification_summary": {
            "notification_status": "not_applicable",
            "dispatch_record_path": "not_applicable",
            "content_review_status": "passed",
        },
        "exception_summary": {
            "exception_status": "none",
            "exception_record_path": "not_applicable",
        },
        "manual_override_summary": {
            "manual_override_status": "none",
            "manual_override_rationale": "not_applicable",
        },
        "sharing_summary": {
            "repository_status": "reviewed",
            "example_data_status": "synthetic",
            "review_status": "passed",
        },
        "review_summary": {
            "review_status": "reviewed",
            "reviewer": "automation",
            "reviewed_at_utc": "2026-05-30T00:01:00Z",
            "review_note": "ok",
        },
    }


def test_valid_daily_evidence_run_record_passes() -> None:
    result = validate_daily_evidence_run_record(_valid_record())

    assert result.is_valid is True
    assert result.errors == ()


def test_missing_required_top_level_field_fails() -> None:
    record = _valid_record()
    del record["commit_sha"]

    result = validate_daily_evidence_run_record(record)

    assert result.is_valid is False
    assert "missing_top_level_field:commit_sha" in result.errors


def test_invalid_required_schema_values_fail() -> None:
    record = _valid_record()
    record["schema_version"] = "old"
    record["record_type"] = "other"
    record["research_mode"] = "other"

    result = validate_daily_evidence_run_record(record)

    assert "invalid_schema_version" in result.errors
    assert "invalid_record_type" in result.errors
    assert "invalid_research_mode" in result.errors


def test_missing_nested_fingerprint_fails() -> None:
    record = _valid_record()
    record["source_summary"]["source_fingerprint"] = ""

    result = validate_daily_evidence_run_record(record)

    assert result.is_valid is False
    assert "missing_nested_field:source_summary.source_fingerprint" in result.errors


def test_generated_output_requires_output_fingerprint() -> None:
    record = _valid_record()
    record["output_summary"]["output_fingerprint"] = ""

    result = validate_daily_evidence_run_record(record)

    assert result.is_valid is False
    assert "missing_nested_field:output_summary.output_fingerprint" in result.errors
    assert "missing_output_fingerprint_for_generated_output" in result.errors


def test_repository_status_must_be_reviewed() -> None:
    record = _valid_record()
    record["sharing_summary"]["repository_status"] = "unreviewed"

    result = validate_daily_evidence_run_record(record)

    assert result.is_valid is False
    assert "repository_status_not_reviewed" in result.errors


def test_manual_override_requires_rationale() -> None:
    record = _valid_record()
    record["manual_override_summary"]["manual_override_status"] = "present"
    record["manual_override_summary"]["manual_override_rationale"] = ""

    result = validate_daily_evidence_run_record(record)

    assert result.is_valid is False
    assert "manual_override_without_rationale" in result.errors
