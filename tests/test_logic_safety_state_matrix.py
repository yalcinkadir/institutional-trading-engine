from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SYSTEM_INVARIANTS = REPO_ROOT / "docs" / "architecture" / "system-invariants.md"
LOGIC_SAFETY = REPO_ROOT / "docs" / "operations" / "logic-safety-governance.md"

FORBIDDEN_CONVERSIONS = [
    ("`UNKNOWN`", "`PASS`"),
    ("`DEGRADED`", "`PASS`"),
    ("`BLOCKED`", "`NO_TRADE_VALID`"),
    ("`FAILED`", "`NO_TRADE_VALID`"),
]

STATE_MATRIX_CASES = [
    "VIX missing and no fallback exists",
    "VIX proxy fallback is used",
    "Empty signal batch in production outcome tracking",
    "Real-data backtest is not pipeline-coupled",
    "Decision-critical module is not runtime-reachable",
    "Demo/stub/synthetic data is used",
    "Input checksum/provenance is missing",
    "Regime is unknown/unvalidated",
]


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_logic_safety_state_matrix_covers_known_dangerous_conditions() -> None:
    content = _read(SYSTEM_INVARIANTS)

    missing = [case for case in STATE_MATRIX_CASES if case not in content]

    assert missing == []


def test_degraded_and_unknown_cannot_be_documented_as_pass_equivalents() -> None:
    policy = _read(LOGIC_SAFETY)

    for source_state, target_state in FORBIDDEN_CONVERSIONS:
        assert source_state in policy
        assert target_state in policy

    assert "Unknown is not evidence" in policy
    assert "Degraded states do not authorize full claims" in policy


def test_degraded_state_has_forbidden_claim_boundary() -> None:
    content = _read(SYSTEM_INVARIANTS)

    required_phrases = [
        "full confidence",
        "production readiness",
        "strategy validation",
        "live-readiness",
        "forbidden_claims",
    ]

    missing = [phrase for phrase in required_phrases if phrase not in content]

    assert missing == []
