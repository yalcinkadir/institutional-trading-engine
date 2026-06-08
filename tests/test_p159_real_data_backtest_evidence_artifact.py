from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_PATH = ROOT / "reports/backtests/real-data-evidence-pack/real-data-backtest-evidence-package.json"
WORKFLOW_PATH = ROOT / ".github/workflows/ci-real-data-backtest-gate.yml"
GUARD_PATH = ROOT / "scripts/check_backtest_evidence_readme_guard.py"


def test_p159_committed_artifact_is_blocked_real_data_not_demo() -> None:
    payload = json.loads(ARTIFACT_PATH.read_text(encoding="utf-8"))
    assert payload["status"] == "BLOCKED"
    assert payload["data_source"] == "polygon"
    assert payload["is_demo"] is False
    assert payload["block_reasons"]


def test_p159_ci_gate_and_readme_guard_are_wired() -> None:
    workflow = WORKFLOW_PATH.read_text(encoding="utf-8")
    guard = GUARD_PATH.read_text(encoding="utf-8")
    assert "build_real_data_backtest_evidence_pack.py" in workflow
    assert "check_backtest_evidence_readme_guard.py" in workflow
    assert "real-data-evidence-pack" in workflow
    assert "BT130:" in guard
    assert "status == \"BLOCKED\"" in guard
