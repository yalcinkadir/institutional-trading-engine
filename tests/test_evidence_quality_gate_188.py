from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from src.evidence_quality_gate import evaluate_evidence_quality_gate


REPO_ROOT = Path(__file__).resolve().parents[1]
POLICY_DOC = REPO_ROOT / "docs" / "operations" / "evidence-quality-gate.md"
README = REPO_ROOT / "README.md"
ROADMAP = REPO_ROOT / "ROADMAP.md"
CHANGELOG = REPO_ROOT / "CHANGELOG.md"
CLI = REPO_ROOT / "scripts" / "evaluate_evidence_quality_gate.py"

REQUIRED_BLOCKER_ISSUES = {"#177", "#178", "#181", "#184", "#185", "#186", "#187"}
FORBIDDEN_PROMOTION_CLAIMS = {
    "roadmap_stable",
    "strategy_promotion",
    "production_grade_evidence",
    "paper_confidence_authorized",
    "backtesting_evidence_promotion",
    "live_ready",
    "decision_stack_validated",
}
UNSAFE_DATA_MODES = {"demo", "stub", "synthetic", "placeholder", "degraded"}


def _passing_payload() -> dict:
    return {
        "run_id": "eqg-pass-001",
        "data_mode": "real_data",
        "provenance": "polygon_real_data_with_manifest",
        "checksum_or_manifest": "sha256:abc123",
        "runtime_trace": "scanner->signals->quality->validator->evidence",
        "promotion_claim": True,
        "claim_type": "production_grade_evidence",
        "pipeline_coupled_real_backtest": True,
        "runtime_reachable_decision_modules": True,
        "durable_paper_observation_index": True,
        "persisted_historical_inputs": True,
        "report_validation_green": True,
        "empty_signal_state_classified": True,
        "regime_vix_provenance_or_block": True,
        "open_blockers": [],
    }


def test_188_policy_document_exists_and_references_required_blockers() -> None:
    text = POLICY_DOC.read_text(encoding="utf-8")

    assert "Evidence Quality Gate (#188)" in text
    assert "PASS" in text
    assert "DEGRADED" in text
    assert "BLOCKED" in text
    assert "pytest tests/test_evidence_quality_gate_188.py -q" in text

    for issue in REQUIRED_BLOCKER_ISSUES:
        assert issue in text

    for claim in FORBIDDEN_PROMOTION_CLAIMS:
        assert claim in text


def test_188_gate_passes_only_when_all_evidence_dimensions_are_proven() -> None:
    result = evaluate_evidence_quality_gate(_passing_payload())

    assert result["schema_version"] == 1
    assert result["gate"] == "Evidence Quality Gate #188"
    assert result["status"] == "PASS"
    assert result["blockers"] == []
    assert result["warnings"] == []
    assert result["data_mode"] == "real_data"
    assert result["promotion_claim"] is True


def test_188_gate_blocks_demo_stub_synthetic_placeholder_or_degraded_promotion_claims() -> None:
    for data_mode in UNSAFE_DATA_MODES:
        payload = _passing_payload()
        payload["data_mode"] = data_mode

        result = evaluate_evidence_quality_gate(payload)

        assert result["status"] == "BLOCKED"
        assert any(
            blocker["code"] == "unsafe_data_mode_for_promotion"
            and blocker["issue"] == "#188"
            for blocker in result["blockers"]
        )


def test_188_gate_blocks_missing_required_promotion_fields() -> None:
    payload = _passing_payload()
    payload["checksum_or_manifest"] = ""
    payload["runtime_trace"] = None

    result = evaluate_evidence_quality_gate(payload)

    assert result["status"] == "BLOCKED"
    reasons = {blocker["reason"] for blocker in result["blockers"]}
    assert "Promotion claim requires `checksum_or_manifest`." in reasons
    assert "Promotion claim requires `runtime_trace`." in reasons


def test_188_gate_blocks_unproven_evidence_dimensions_with_issue_references() -> None:
    payload = _passing_payload()
    payload["pipeline_coupled_real_backtest"] = False
    payload["runtime_reachable_decision_modules"] = False
    payload["durable_paper_observation_index"] = False
    payload["persisted_historical_inputs"] = False
    payload["report_validation_green"] = False
    payload["empty_signal_state_classified"] = False
    payload["regime_vix_provenance_or_block"] = False

    result = evaluate_evidence_quality_gate(payload)

    assert result["status"] == "BLOCKED"
    blocker_issues = {blocker["issue"] for blocker in result["blockers"]}
    assert REQUIRED_BLOCKER_ISSUES <= blocker_issues


def test_188_gate_blocks_when_evidence_critical_issue_remains_open() -> None:
    payload = _passing_payload()
    payload["open_blockers"] = ["177", "#184", "999"]

    result = evaluate_evidence_quality_gate(payload)

    assert result["status"] == "BLOCKED"
    blockers = [blocker for blocker in result["blockers"] if blocker["code"] == "evidence_critical_issue_open"]
    assert {blocker["issue"] for blocker in blockers} == {"#177", "#184"}


def test_188_degraded_without_promotion_claim_remains_research_visibility_only() -> None:
    payload = _passing_payload()
    payload["promotion_claim"] = False
    payload["claim_type"] = None
    payload["data_mode"] = "degraded"

    result = evaluate_evidence_quality_gate(payload)

    assert result["status"] == "DEGRADED"
    assert result["blockers"] == []
    assert result["warnings"] == ["Data mode `degraded` is not production-grade; research visibility only."]


def test_188_cli_writes_machine_readable_result_and_exits_nonzero_when_blocked(tmp_path: Path) -> None:
    payload = _passing_payload()
    payload["data_mode"] = "demo"
    input_path = tmp_path / "gate_input.json"
    output_path = tmp_path / "gate_result.json"
    input_path.write_text(json.dumps(payload), encoding="utf-8")

    completed = subprocess.run(
        [
            sys.executable,
            str(CLI),
            "--input",
            str(input_path),
            "--output",
            str(output_path),
        ],
        cwd=REPO_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 1
    result = json.loads(output_path.read_text(encoding="utf-8"))
    assert result["status"] == "BLOCKED"
    assert result["gate"] == "Evidence Quality Gate #188"


def test_188_readme_roadmap_and_changelog_reference_gate_without_live_authorization() -> None:
    readme = README.read_text(encoding="utf-8")
    roadmap = ROADMAP.read_text(encoding="utf-8")
    changelog = CHANGELOG.read_text(encoding="utf-8")

    for text in (readme, roadmap, changelog):
        assert "#188" in text
        assert "Evidence Quality Gate" in text
        assert "live trading" in text.lower() or "live-trading" in text.lower()

    assert "docs/operations/evidence-quality-gate.md" in readme
    assert "tests/test_evidence_quality_gate_188.py" in readme
    assert "docs/operations/evidence-quality-gate.md" in roadmap
    assert "tests/test_evidence_quality_gate_188.py" in roadmap
