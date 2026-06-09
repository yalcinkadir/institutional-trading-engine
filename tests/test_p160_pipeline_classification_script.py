from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/classify_pipeline_modules_p160.py"


def test_p160_script_declares_expected_counts_and_baseline() -> None:
    text = SCRIPT.read_text(encoding="utf-8")

    assert "EXPECTED_NEW_COUNT = 88" in text
    assert "EXPECTED_RESULTING_UNCLASSIFIED_BASELINE = 196" in text


def test_p160_runtime_proof_constants_are_present() -> None:
    text = SCRIPT.read_text(encoding="utf-8")

    assert "RUNTIME_ENTRYPOINT" in text
    assert "RUNTIME_EXECUTION_PROOF" in text
    assert "run_historical_entry_exit_backtest.py" in text
    assert "test_bt130_real_historical_evidence_pack_gate.py" in text


def test_p160_script_does_not_delete_existing_classifications() -> None:
    text = SCRIPT.read_text(encoding="utf-8")

    assert "Does NOT touch already-classified modules." in text
    assert "if path in classified:" in text
    assert "skipped.append(path)" in text
