from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "docs" / "operations" / "full_suite_flake_review.md"
CI_WORKFLOW = ROOT / ".github" / "workflows" / "ci.yml"


REQUIRED_FAILURE_CATEGORIES = [
    "product_failure",
    "regression_failure",
    "environment_failure",
    "timing_or_ordering_flake",
    "external_service_dependency",
    "unknown_flake",
]


REQUIRED_TRIAGE_FIELDS = [
    "failing test name",
    "CI step name",
    "failure category",
    "first failing commit",
    "reproduction command",
    "retry decision",
    "owner or remediation path",
]


def test_full_suite_flake_review_policy_defines_failure_categories() -> None:
    text = POLICY.read_text(encoding="utf-8")

    for category in REQUIRED_FAILURE_CATEGORIES:
        assert category in text


def test_full_suite_flake_review_policy_defines_triage_note_contract() -> None:
    text = POLICY.read_text(encoding="utf-8")

    for field in REQUIRED_TRIAGE_FIELDS:
        assert field in text


def test_full_suite_flake_review_policy_defines_retry_and_escalation_rules() -> None:
    text = POLICY.read_text(encoding="utf-8")

    assert "one automatic retry is acceptable" in text
    assert "no blind repeated retry" in text
    assert "the same test fails twice" in text
    assert "the same module flakes more than once in seven days" in text


def test_ci_keeps_targeted_gates_and_residual_suite_shape() -> None:
    workflow = CI_WORKFLOW.read_text(encoding="utf-8")

    expected_steps = [
        "EV evidence consolidation guard tests",
        "Roadmap EV completion guard tests",
        "Full regression suite residual tests",
        "EV12 drawdown magnitude regression tests",
        "GOV7-GOV10 pre-live hygiene tests",
        "CL2/CL3 scoring and drawdown-source governance tests",
    ]

    for step in expected_steps:
        assert step in workflow

    assert "--ignore=tests/test_ev_evidence_consolidation.py" in workflow
    assert "--ignore=tests/test_roadmap_ev_completion_guard.py" in workflow
