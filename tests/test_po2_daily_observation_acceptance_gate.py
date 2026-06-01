from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PO2_DOC = ROOT / "docs" / "operations" / "po2_daily_observation_acceptance_gate.md"


def _doc() -> str:
    return PO2_DOC.read_text(encoding="utf-8")


def test_po2_acceptance_rule_is_documented() -> None:
    content = _doc()

    assert "A Paper Observation day is accepted only when every required evidence family is present" in content
    assert "accepted_day = required_evidence_present" in content
    assert "reports_generated_successfully" in content
    assert "manifests_reference_required_artifacts" in content
    assert "no_live_trading_authorization" in content
    assert "no_real_money_execution" in content


def test_po2_required_evidence_families_are_documented() -> None:
    content = _doc()

    required = (
        "Daily Evidence report",
        "Runtime Evidence manifest",
        "Drift and regime evidence",
        "Fill-quality evidence when paper fills exist",
        "Backtesting Evidence reference",
        "Capacity / turnover realism reference",
        "Runtime governance status",
        "Incident notes",
    )
    for item in required:
        assert item in content


def test_po2_rejection_reasons_are_documented() -> None:
    content = _doc()

    rejection_reasons = (
        "required report missing",
        "required manifest missing",
        "report generation failed",
        "artifact hash/reference mismatch",
        "missing data is not documented",
        "provider degradation is not documented",
        "drift/regime event is not documented",
        "fill-quality evidence is missing for paper fills",
        "live trading is implied or authorized",
        "real-money execution is implied or authorized",
    )
    for reason in rejection_reasons:
        assert reason in content


def test_po2_status_vocabulary_and_live_block_are_documented() -> None:
    content = _doc()

    assert "ACCEPTED" in content
    assert "REJECTED" in content
    assert "NEEDS_REVIEW" in content
    assert "does not authorize live trading" in content
    assert "research / paper-observation only" in content
