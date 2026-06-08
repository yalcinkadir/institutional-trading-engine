from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/classify_pipeline_modules_p160.py"


def test_p160_script_declares_expected_counts_and_baseline() -> None:
    text = SCRIPT.read_text(encoding="utf-8")

    assert "EXPECTED_NEW_COUNT = 102" in text
    assert "EXPECTED_RESULTING_UNCLASSIFIED_BASELINE = 182" in text
    assert "src/backtesting/historical_entry_exit_backtest.py" in text
    assert "src/backtesting/historical_models.py" in text
    assert "src/backtesting/historical_report.py" in text


def test_p160_connected_runtime_entries_require_runtime_proof() -> None:
    text = SCRIPT.read_text(encoding="utf-8")

    assert text.count('"classification": "connected_runtime"') == 3
    assert text.count('"runtime_entrypoint": "scripts/run_historical_entry_exit_backtest.py"') == 3
    assert "tests/test_bt130_real_historical_evidence_pack_gate.py" in text


def test_p160_script_does_not_delete_existing_classifications() -> None:
    text = SCRIPT.read_text(encoding="utf-8")

    assert "Does NOT touch already-classified modules." in text
    assert "if path in classified:" in text
    assert "skipped.append(path)" in text
