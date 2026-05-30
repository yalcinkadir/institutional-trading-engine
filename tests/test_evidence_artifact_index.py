from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "docs" / "operations" / "evidence_artifact_index.md"
CI_WORKFLOW = ROOT / ".github" / "workflows" / "ci.yml"


REQUIRED_INDEX_LINKS = [
    "docs/operations/ev_evidence_consolidation_full_suite_review.md",
    "docs/operations/ev_evidence_consolidation_ci_green_completion.md",
    "docs/operations/full_suite_flake_review.md",
    "ROADMAP.md",
    ".github/workflows/ci.yml",
    "tests/test_ev_evidence_consolidation.py",
    "tests/test_roadmap_ev_completion_guard.py",
    "tests/test_full_suite_flake_review_policy.py",
    "tests/test_ev12_drawdown_magnitude.py",
    "tests/test_backtest_fidelity_ev3_ev6.py",
    "tests/test_sharpe_definition_regression.py",
]


REQUIRED_STATUS_MARKERS = [
    "EV1-EV12 evidence consolidation",
    "Roadmap EV completion cleanup",
    "Full-suite flake review",
    "CI runtime simplification",
    "Done / CI-green",
]


def test_evidence_artifact_index_links_current_documents_and_guard_tests() -> None:
    text = INDEX.read_text(encoding="utf-8")

    for link in REQUIRED_INDEX_LINKS:
        assert link in text


def test_evidence_artifact_index_marks_current_stabilization_status() -> None:
    text = INDEX.read_text(encoding="utf-8")

    for marker in REQUIRED_STATUS_MARKERS:
        assert marker in text


def test_ci_wires_evidence_artifact_index_guard() -> None:
    workflow = CI_WORKFLOW.read_text(encoding="utf-8")

    assert "Evidence artifact index guard tests" in workflow
    assert "pytest tests/test_evidence_artifact_index.py -q" in workflow
