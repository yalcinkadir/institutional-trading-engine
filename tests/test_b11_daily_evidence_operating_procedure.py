from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNBOOK = ROOT / "docs" / "operations" / "b11_daily_evidence_operating_procedure.md"
CI_WORKFLOW = ROOT / ".github" / "workflows" / "ci.yml"


REQUIRED_BOUNDARY_MARKERS = [
    "mode: observation_only",
    "real_money_execution: prohibited",
    "manual_review_required: true",
    "private_edge_publication: prohibited",
    "real-money execution remains explicitly unauthorized",
]


REQUIRED_DAILY_FIELDS = [
    "commit_sha",
    "run_date",
    "observation_mode",
    "input_validation_status",
    "source_collection_status",
    "reconciliation_status",
    "daily_evidence_status",
    "runtime_report_location",
    "notification_status",
    "exceptions_or_manual_overrides",
]


REQUIRED_FAIL_CLOSED_CONDITIONS = [
    "input validation fails",
    "source collection is incomplete",
    "reconciliation is not clean",
    "required evidence artifact is missing",
    "runtime report path points to committed public examples",
    "notification content implies live trading authorization",
    "private edge values are exposed",
    "manual override is present without rationale",
]


def test_b11_daily_evidence_runbook_preserves_observation_only_boundary() -> None:
    text = RUNBOOK.read_text(encoding="utf-8")

    for marker in REQUIRED_BOUNDARY_MARKERS:
        assert marker in text


def test_b11_daily_evidence_runbook_lists_required_daily_fields() -> None:
    text = RUNBOOK.read_text(encoding="utf-8")

    for field in REQUIRED_DAILY_FIELDS:
        assert field in text


def test_b11_daily_evidence_runbook_lists_fail_closed_conditions() -> None:
    text = RUNBOOK.read_text(encoding="utf-8")

    for condition in REQUIRED_FAIL_CLOSED_CONDITIONS:
        assert condition in text


def test_b11_daily_evidence_runbook_ci_guard_is_wired() -> None:
    workflow = CI_WORKFLOW.read_text(encoding="utf-8")

    assert "B1.1 daily evidence operating procedure guard tests" in workflow
    assert "pytest tests/test_b11_daily_evidence_operating_procedure.py -q" in workflow
