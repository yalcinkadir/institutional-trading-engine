from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "docs" / "operations" / "b11_daily_evidence_artifact_contract.md"
CI_WORKFLOW = ROOT / ".github" / "workflows" / "ci.yml"


REQUIRED_METADATA_FIELDS = [
    "artifact_type",
    "artifact_version",
    "commit_sha",
    "run_date_utc",
    "created_at_utc",
    "research_mode",
    "source_name",
    "source_fingerprint",
    "input_fingerprint",
    "output_fingerprint",
    "reconciliation_status",
    "evidence_status",
    "manual_override_status",
    "private_edge_status",
    "public_safety_status",
]


REQUIRED_STATUS_VALUES = [
    "research_mode: paper_observation_only",
    "private_edge_status: clean",
    "public_safety_status: public_safe",
]


REQUIRED_REFERENCES = [
    "input_source_path",
    "runtime_report_path",
    "reconciliation_record_path",
    "notification_record_path",
    "exception_record_path",
]


def test_daily_evidence_artifact_contract_lists_required_metadata() -> None:
    text = CONTRACT.read_text(encoding="utf-8")

    for field in REQUIRED_METADATA_FIELDS:
        assert field in text


def test_daily_evidence_artifact_contract_lists_required_status_values() -> None:
    text = CONTRACT.read_text(encoding="utf-8")

    for status_value in REQUIRED_STATUS_VALUES:
        assert status_value in text


def test_daily_evidence_artifact_contract_lists_required_references() -> None:
    text = CONTRACT.read_text(encoding="utf-8")

    for reference in REQUIRED_REFERENCES:
        assert reference in text


def test_daily_evidence_artifact_contract_rejects_ambiguous_completion_markers() -> None:
    text = CONTRACT.read_text(encoding="utf-8")

    assert "production_ready" in text
    assert "complete_without_review" in text
    assert "must not use ambiguous values" in text


def test_daily_evidence_artifact_contract_ci_guard_is_wired() -> None:
    workflow = CI_WORKFLOW.read_text(encoding="utf-8")

    assert "B1.1 daily evidence artifact contract guard tests" in workflow
    assert "pytest tests/test_b11_daily_evidence_artifact_contract.py -q" in workflow
