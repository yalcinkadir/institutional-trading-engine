from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SYSTEM_INVARIANTS = REPO_ROOT / "docs" / "architecture" / "system-invariants.md"
LOGIC_SAFETY = REPO_ROOT / "docs" / "operations" / "logic-safety-governance.md"

REQUIRED_TRACEABILITY_FIELDS = [
    "run_id",
    "workflow_run_id",
    "input_data_source",
    "input_data_checksum",
    "symbol_universe",
    "date_range",
    "pipeline_version",
    "runtime_trace",
    "generator_version",
    "data_mode",
    "status",
    "blocked_reasons",
    "degradation_reasons",
]

REQUIRED_DATA_MODES = [
    "real",
    "demo",
    "stub",
    "synthetic",
]


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_system_invariants_define_evidence_traceability_minimum_fields() -> None:
    content = _read(SYSTEM_INVARIANTS)

    missing = [field for field in REQUIRED_TRACEABILITY_FIELDS if field not in content]

    assert missing == []


def test_logic_safety_policy_defines_evidence_traceability_minimum_fields() -> None:
    content = _read(LOGIC_SAFETY)

    missing = [field for field in REQUIRED_TRACEABILITY_FIELDS if field not in content]

    assert missing == []


def test_data_mode_vocabulary_separates_real_demo_stub_and_synthetic_evidence() -> None:
    combined = _read(SYSTEM_INVARIANTS) + "\n" + _read(LOGIC_SAFETY)

    missing = [mode for mode in REQUIRED_DATA_MODES if mode not in combined]

    assert missing == []
    assert "Demo data is not strategy evidence" in combined
