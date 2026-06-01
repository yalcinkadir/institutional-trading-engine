from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PO1_DOC = ROOT / "docs" / "operations" / "po1_paper_observation_timeline.md"


def _doc() -> str:
    return PO1_DOC.read_text(encoding="utf-8")


def test_po1_timeline_dates_are_documented() -> None:
    content = _doc()

    assert "Paper Observation start date: 2026-06-01" in content
    assert "Minimum duration: 3 months" in content
    assert "Target duration: 3-6 months" in content
    assert "First review date: 2026-07-01" in content
    assert "Major evidence review date: 2026-09-01" in content
    assert "Target extended review date: 2026-12-01" in content


def test_po1_review_gates_are_documented() -> None:
    content = _doc()

    assert "30-day review" in content
    assert "90-day review" in content
    assert "daily evidence completeness" in content
    assert "forward paper evidence quality" in content
    assert "capacity/turnover realism" in content
    assert "execution-quality evidence" in content
    assert "risk attribution" in content
    assert "regime/drift behavior" in content


def test_po1_required_evidence_families_are_documented() -> None:
    content = _doc()

    required = (
        "Daily Evidence reports",
        "Runtime Evidence manifests",
        "Drift and regime evidence",
        "Fill-quality evidence",
        "Backtesting Evidence reports",
        "Capacity / turnover realism evidence",
        "Runtime governance proof status",
        "Manual review notes",
    )
    for item in required:
        assert item in content


def test_po1_live_trading_remains_blocked() -> None:
    content = _doc()

    assert "Live trading authorization: not granted by code" in content
    assert "Broker execution: paper-only infrastructure" in content
    assert "Real-money execution: blocked" in content
    assert "not a live-trading authorization" in content
