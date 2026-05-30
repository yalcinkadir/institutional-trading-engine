from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "docs" / "operations" / "b11_daily_evidence_run_record_schema.md"
CI_WORKFLOW = ROOT / ".github" / "workflows" / "ci.yml"


REQUIRED_TOP_LEVEL_FIELDS = [
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
]


REQUIRED_SCHEMA_VALUES = [
    "schema_version: b11_daily_evidence_run_record_v1",
    "record_type: daily_evidence_run_record",
    "research_mode: paper_observation_only",
]


REQUIRED_INVALID_CONDITIONS = [
    "schema_version is missing",
    "record_id is missing",
    "commit_sha is missing",
    "research_mode is not paper_observation_only",
    "source_fingerprint is missing",
    "input_fingerprint is missing",
    "reconciliation_status is missing",
    "repository_status is not reviewed",
    "manual_override_status is present without rationale",
]


def test_daily_evidence_run_record_schema_lists_top_level_fields() -> None:
    text = SCHEMA.read_text(encoding="utf-8")

    for field in REQUIRED_TOP_LEVEL_FIELDS:
        assert field in text


def test_daily_evidence_run_record_schema_lists_required_values() -> None:
    text = SCHEMA.read_text(encoding="utf-8")

    for value in REQUIRED_SCHEMA_VALUES:
        assert value in text


def test_daily_evidence_run_record_schema_lists_invalid_conditions() -> None:
    text = SCHEMA.read_text(encoding="utf-8")

    for condition in REQUIRED_INVALID_CONDITIONS:
        assert condition in text


def test_daily_evidence_run_record_schema_ci_guard_is_wired() -> None:
    workflow = CI_WORKFLOW.read_text(encoding="utf-8")

    assert "B1.1 daily evidence run record schema guard tests" in workflow
    assert "pytest tests/test_b11_daily_evidence_run_record_schema.py -q" in workflow
