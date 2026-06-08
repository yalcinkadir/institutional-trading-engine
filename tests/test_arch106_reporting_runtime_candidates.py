from __future__ import annotations

from pathlib import Path


CANDIDATE_DOC = Path("docs/architecture/arch106_reporting_runtime_candidates.md")
RUNTIME_PROOF_TEST = Path("tests/test_architecture_runtime_execution_guard.py")


CANDIDATES = [
    "src/reporting/cross_asset_report.py",
    "src/reporting/report_formatter.py",
]


def test_arch106_reporting_runtime_candidates_document_policy_and_follow_up() -> None:
    content = CANDIDATE_DOC.read_text(encoding="utf-8")

    assert "Reachability is necessary but not sufficient." in content
    assert "module_classification.json" in content
    assert "module_inventory.generated.json" in content
    assert "python scripts/generate_module_inventory.py --check" in content

    for candidate in CANDIDATES:
        assert candidate in content
        assert "Proposed classification: `connected_runtime`" in content


def test_arch106_reporting_runtime_candidates_have_runtime_proof_markers() -> None:
    proof = RUNTIME_PROOF_TEST.read_text(encoding="utf-8")

    assert "from src.reporting.cross_asset_report import build_cross_asset_report" in proof
    assert "cross_asset_called" in proof
    assert "from src.reporting.report_formatter import format_report" in proof
    assert "format_report_called" in proof
