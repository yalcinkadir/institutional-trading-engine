from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.validation.feature_connectivity_matrix_guard import validate_feature_connectivity_matrix


def _matrix():
    return [
        {
            "feature_id": "RGP13",
            "feature_name": "Runtime Proof Pack Summary Builder",
            "owner_phase": "RGP",
            "status": "ci_green",
            "runtime_gate": "build_runtime_proof_pack_summary",
            "guard_test": "tests/test_rgp13_runtime_proof_pack_summary_builder.py",
            "evidence_artifact": "reports/runtime_proof_pack_summary.json",
            "documentation_ref": "ROADMAP.md#phase-rgp-runtime-governance-proof-pack",
            "upstream_dependencies": [],
            "downstream_consumers": ["RPW1"],
        },
        {
            "feature_id": "RPW1",
            "feature_name": "Runtime Proof-Pack Artifact Writer / Retention Index",
            "owner_phase": "Runtime Governance",
            "status": "ci_green",
            "runtime_gate": "write_runtime_proof_pack_artifact",
            "guard_test": "tests/test_rpw1_runtime_proof_pack_artifact_writer.py",
            "evidence_artifact": "reports/runtime_proof_pack/runtime-proof-pack.json",
            "documentation_ref": "ROADMAP.md#phase-fcmrpw-connectivity-and-proof-pack-retention",
            "upstream_dependencies": ["RGP13"],
            "downstream_consumers": ["monthly_review", "retention_index"],
        },
    ]


def test_fcm1_accepts_connected_ci_green_feature_matrix() -> None:
    result = validate_feature_connectivity_matrix(_matrix())

    assert result.valid is True
    assert result.errors == ()
    assert result.summary["feature_connectivity_matrix_status"] == "PASS"
    assert result.summary["feature_count"] == 2
    assert result.summary["ci_green_feature_count"] == 2
    assert result.summary["live_trading_authorized"] is False
    assert result.summary["broker_execution_mode"] == "paper_only"


def test_fcm1_blocks_implemented_feature_without_guard_test_or_artifact() -> None:
    matrix = _matrix()
    matrix[1]["guard_test"] = ""
    matrix[1]["evidence_artifact"] = ""

    result = validate_feature_connectivity_matrix(matrix)

    assert result.valid is False
    assert "RPW1:missing_guard_test" in result.errors
    assert "RPW1:missing_evidence_artifact" in result.errors
    assert result.summary["feature_connectivity_matrix_status"] == "BLOCKED"


def test_fcm1_blocks_unknown_upstream_dependency() -> None:
    matrix = _matrix()
    matrix[1]["upstream_dependencies"] = ["UNKNOWN"]

    result = validate_feature_connectivity_matrix(matrix)

    assert result.valid is False
    assert "RPW1:unknown_upstream_dependencies:UNKNOWN" in result.errors


def test_fcm1_preserves_paper_only_boundary() -> None:
    matrix = _matrix()
    matrix[1]["live_trading_authorized"] = True
    matrix[1]["broker_execution_mode"] = "live"

    result = validate_feature_connectivity_matrix(matrix)

    assert result.valid is False
    assert "RPW1:live_trading_must_remain_false" in result.errors
    assert "RPW1:broker_execution_mode_must_be_paper_only" in result.errors
    assert result.summary["live_trading_authorized"] is False
    assert result.summary["broker_execution_mode"] == "paper_only"
