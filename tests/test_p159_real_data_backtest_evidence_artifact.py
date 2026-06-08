from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_PATH = ROOT / "reports/backtests/real-data-evidence-pack/real-data-backtest-evidence-package.json"
WORKFLOW_PATH = ROOT / ".github/workflows/ci-real-data-backtest-gate.yml"
GUARD_PATH = ROOT / "scripts/check_backtest_evidence_readme_guard.py"
