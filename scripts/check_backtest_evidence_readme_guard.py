#!/usr/bin/env python3
"""CI guard: real-data backtest evidence artifact must exist and README must not claim
productive backtesting without a VALID artifact.

Exits 0 when:
- Artifact exists with status=VALID and bt130_gate_status=PASSED
- Artifact exists with status=BLOCKED (expected in CI without Polygon API key)

Exits 1 when:
- Artifact file is missing entirely
- Artifact is malformed JSON
- README claims 'CI-green' for BT130 but artifact is not VALID
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

ARTIFACT_PATH = ROOT / "reports/backtests/real-data-evidence-pack/real-data-backtest-evidence-package.json"
README_PATH = ROOT / "README.md"

BT130_CI_GREEN_MARKER = "BT130:"
PRODUCTIVE_CLAIM_MARKERS = ["CI-green", "productive", "VALID"]


def _load_artifact() -> dict:
    if not ARTIFACT_PATH.exists():
        print(f"FAIL: evidence artifact not found at {ARTIFACT_PATH.relative_to(ROOT)}")
        print("      Run the real-data evidence pack pipeline to produce a BLOCKED or VALID artifact.")
        print("      Example: python scripts/build_real_data_backtest_evidence_pack.py ...")
        sys.exit(1)
    try:
        return json.loads(ARTIFACT_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"FAIL: evidence artifact is malformed JSON: {exc}")
        sys.exit(1)


def _check_readme_claim(artifact_status: str, bt130_gate: str) -> None:
    if not README_PATH.exists():
        return
    readme = README_PATH.read_text(encoding="utf-8")
    for line in readme.splitlines():
        if not line.strip().startswith(BT130_CI_GREEN_MARKER):
            continue
        claims_ci_green = "CI-green" in line and "BLOCKED" not in line
        if claims_ci_green and artifact_status != "VALID":
            print(f"FAIL: README claims BT130 CI-green but artifact status is {artifact_status!r} (bt130_gate={bt130_gate!r})")
            print(f"      README line: {line.strip()}")
            print("      Update README to reflect the actual artifact status before claiming CI-green.")
            sys.exit(1)


def main() -> None:
    artifact = _load_artifact()

    status = artifact.get("status", "UNKNOWN")
    bt130_gate = artifact.get("bt130_gate_status", "UNKNOWN")
    block_reasons = artifact.get("block_reasons", [])
    run_id = artifact.get("run_id", "unknown")

    print(f"Real-data backtest evidence artifact: {ARTIFACT_PATH.relative_to(ROOT)}")
    print(f"  run_id          : {run_id}")
    print(f"  status          : {status}")
    print(f"  bt130_gate      : {bt130_gate}")
    if block_reasons:
        print(f"  block_reasons   : {', '.join(block_reasons)}")

    _check_readme_claim(status, bt130_gate)

    if status == "VALID" and bt130_gate == "PASSED":
        print("PASS: real-data backtest evidence artifact is VALID with BT130 gate PASSED.")
        sys.exit(0)

    if status == "BLOCKED":
        print("PASS: artifact is BLOCKED — expected in CI without licensed Polygon data.")
        print("      Supply POLYGON_API_KEY and real trade plans to produce a VALID artifact.")
        sys.exit(0)

    print(f"FAIL: unexpected artifact status={status!r}, bt130_gate={bt130_gate!r}")
    sys.exit(1)


if __name__ == "__main__":
    main()
