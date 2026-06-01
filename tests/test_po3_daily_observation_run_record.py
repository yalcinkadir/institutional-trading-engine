from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PO3_DOC = ROOT / "docs" / "operations" / "po3_daily_observation_run_record.md"


def _doc() -> str:
    return PO3_DOC.read_text(encoding="utf-8")


def test_po3_required_record_fields_are_documented() -> None:
    content = _doc()

    required_fields = (
        "date",
        "status",
        "missing_evidence",
        "incidents",
        "artifact_paths",
        "review_required",
        "review_notes",
        "live_trading_authorized",
        "broker_execution_mode",
        "created_at",
    )
    for field in required_fields:
        assert field in content


def test_po3_status_vocabulary_is_documented() -> None:
    content = _doc()

    assert "ACCEPTED" in content
    assert "REJECTED" in content
    assert "NEEDS_REVIEW" in content
    assert "status: one of ACCEPTED, REJECTED, NEEDS_REVIEW" in content


def test_po3_acceptance_mapping_is_documented() -> None:
    content = _doc()

    assert "ACCEPTED: no missing evidence" in content
    assert "REJECTED: missing required evidence" in content
    assert "NEEDS_REVIEW: core evidence exists" in content
    assert "manual review" in content


def test_po3_live_trading_is_blocked_in_record_contract() -> None:
    content = _doc()

    assert "live_trading_authorized: always false" in content
    assert "broker_execution_mode: paper_only" in content
    assert '"live_trading_authorized": false' in content
    assert '"broker_execution_mode": "paper_only"' in content
    assert "does not authorize live trading" in content


def test_po3_example_record_is_public_safe_and_machine_readable() -> None:
    content = _doc()

    assert '"date": "2026-06-01"' in content
    assert '"status": "ACCEPTED"' in content
    assert '"missing_evidence": []' in content
    assert '"incidents": []' in content
    assert '"artifact_paths"' in content
    assert '"review_required": false' in content
