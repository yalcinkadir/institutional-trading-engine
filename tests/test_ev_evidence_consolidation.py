from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE_DOC = ROOT / "docs" / "operations" / "ev_evidence_consolidation_full_suite_review.md"
CI_WORKFLOW = ROOT / ".github" / "workflows" / "ci.yml"


EXPECTED_EV_STATUSES = [
    "EV1: done / CI-green",
    "EV2: done / CI-green",
    "EV3: done / CI-green",
    "EV4: done / CI-green",
    "EV5: done / CI-green",
    "EV6: done / CI-green",
    "EV7: done / CI-green",
    "EV8: done / CI-green",
    "EV9: done / CI-green",
    "EV10: done / CI-green",
    "EV11: done / CI-green",
    "EV12: done / CI-green",
]


EXPECTED_CI_STEPS = [
    "EV1-EV2 Sharpe definition regression tests",
    "EV3-EV6 backtest fidelity tests",
    "EV7 decision ranking regression tests",
    "EV8 fixed-date holdout semantics regression tests",
    "EV10 profit-factor infinity regression tests",
    "EV11 conservative setup scoring regression tests",
    "EV12 drawdown magnitude regression tests",
    "Full regression suite",
]


def test_ev_evidence_consolidation_document_lists_all_completed_ev_items() -> None:
    text = EVIDENCE_DOC.read_text(encoding="utf-8")

    for status in EXPECTED_EV_STATUSES:
        assert status in text


def test_ev_evidence_consolidation_document_links_primary_regression_files() -> None:
    text = EVIDENCE_DOC.read_text(encoding="utf-8")

    expected_files = [
        "tests/test_sharpe_definition_regression.py",
        "tests/test_backtest_fidelity_ev3_ev6.py",
        "tests/test_decision_engine.py",
        "tests/test_out_of_sample_lockbox.py",
        "tests/test_historical_edge_validation.py",
        "tests/test_setup_scoring.py",
        "tests/test_ev12_drawdown_magnitude.py",
    ]

    for filename in expected_files:
        assert filename in text


def test_ci_workflow_keeps_ev_targeted_steps_and_full_suite_guard() -> None:
    workflow = CI_WORKFLOW.read_text(encoding="utf-8")

    for step_name in EXPECTED_CI_STEPS:
        assert step_name in workflow
