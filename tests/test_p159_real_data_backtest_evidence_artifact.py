from __future__ import annotations

import json
from pathlib import Path

from scripts import check_backtest_evidence_readme_guard as readme_guard
from scripts import run_historical_entry_exit_backtest as runner


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_PATH = ROOT / "reports/backtests/real-data-evidence-pack/real-data-backtest-evidence-package.json"


def test_committed_real_data_evidence_package_exists_and_is_not_demo() -> None:
    assert ARTIFACT_PATH.exists()
    payload = json.loads(ARTIFACT_PATH.read_text(encoding="