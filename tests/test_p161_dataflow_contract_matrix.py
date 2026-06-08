from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "docs/architecture/dataflow_contract_matrix.md"


def test_p161_dataflow_contract_matrix_exists_and_names_runtime_path() -> None:
    text = MATRIX.read_text(encoding="utf-8")
    assert "Scanner → Signals → Quality → Validator → Watcher → Evidence" in text
    assert "atr14" in text
    assert "run_health_status" in text

