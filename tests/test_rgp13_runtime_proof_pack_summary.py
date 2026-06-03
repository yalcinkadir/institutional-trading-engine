from __future__ import annotations

from src.runtime.runtime_proof_pack_summary import build_runtime_proof_pack_summary


def test_rgp13_builds_review_ready_runtime_proof_pack_summary() -> None:
    result = build_runtime_proof_pack_summary(
        {
            "observation_date": "2026-06-03",
            "portfolio_state": {"governance_valid": True, "warnings": []},
            "approval_gate": {"approved": True, "decision": "APPROVED", "reason": "paper_observation"},
            "signal_lifecycle": {"status": "ACTIVE", "signal_id": "sig-1"},
            "runtime_evidence": {"manifest_path": "reports/runtime/2026-06-03/manifest.json"},
            "live_trading_authorized": False,
            "broker_execution_mode": "paper_only",
        }
    )

    assert result.valid is True
    assert result.errors == ()
    assert result.summary["runtime_proof_status"] == "REVIEW_READY"
    assert result.summary["approved_for_runtime_review"] is True
    assert result.summary["evidence_paths"] == ["reports/runtime/2026-06-03/manifest.json"]
    assert result.summary["live_trading_authorized"] is False
    assert result.summary["broker_execution_mode"] == "paper_only"


def test_rgp13_blocks_missing_required_runtime_sections() -> None:
    result = build_runtime_proof_pack_summary(
        {
            "observation_date": "2026-06-03",
            "portfolio_state": {"governance_valid": True, "warnings": []},
            "live_trading_authorized": False,
            "broker_execution_mode": "paper_only",
        }
    )

    assert result.valid is False
    assert result.summary["runtime_proof_status"] == "BLOCKED"
    assert result.summary["approved_for_runtime_review"] is False
    assert "missing_approval_gate" in result.errors
    assert "missing_signal_lifecycle" in result.errors
    assert "missing_runtime_evidence" in result.errors


def test_rgp13_surfaces_fail_closed_portfolio_state() -> None:
    result = build_runtime_proof_pack_summary(
        {
            "observation_date": "2026-06-03",
            "portfolio_state": {"governance_valid": False, "warnings": ["missing_portfolio_state"]},
            "approval_gate": {"approved": False, "decision": "BLOCKED", "reason": "portfolio_state_invalid"},
            "signal_lifecycle": {"status": "BLOCKED", "signal_id": "sig-1"},
            "runtime_evidence": {"manifest_path": "reports/runtime/2026-06-03/manifest.json"},
            "live_trading_authorized": False,
            "broker_execution_mode": "paper_only",
        }
    )

    assert result.valid is False
    assert "portfolio_state_governance_invalid" in result.errors
    assert "approval_gate_not_approved" in result.errors
    assert result.summary["portfolio_warnings"] == ["missing_portfolio_state"]


def test_rgp13_blocks_live_or_non_paper_boundaries() -> None:
    result = build_runtime_proof_pack_summary(
        {
            "observation_date": "2026-06-03",
            "portfolio_state": {"governance_valid": True, "warnings": []},
            "approval_gate": {"approved": True, "decision": "APPROVED"},
            "signal_lifecycle": {"status": "ACTIVE", "signal_id": "sig-1"},
            "runtime_evidence": {"manifest_path": "reports/runtime/2026-06-03/manifest.json"},
            "live_trading_authorized": True,
            "broker_execution_mode": "live",
        }
    )

    assert result.valid is False
    assert "live_trading_must_remain_false" in result.errors
    assert "broker_execution_mode_must_be_paper_only" in result.errors
    assert result.summary["live_trading_authorized"] is False
    assert result.summary["broker_execution_mode"] == "paper_only"
