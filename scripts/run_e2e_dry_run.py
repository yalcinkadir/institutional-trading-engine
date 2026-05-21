#!/usr/bin/env python3
"""Run local end-to-end dry-run validation."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.operations.e2e_dry_run import run_e2e_dry_run_validation


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate local E2E dry-run readiness.")
    parser.add_argument("--signals-file", default="reports/signals/latest-signals.json")
    parser.add_argument("--alerts-dir", default="reports/alerts")
    parser.add_argument("--lifecycle-dir", default="data")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON output.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    result = run_e2e_dry_run_validation(
        signal_file=Path(args.signals_file),
        alerts_dir=Path(args.alerts_dir),
        lifecycle_dir=Path(args.lifecycle_dir),
    )

    if args.json:
        print(json.dumps(result.to_dict(), indent=2))
    else:
        status = "PASS" if result.passed else "FAIL"
        print(f"E2E dry-run validation: {status}")
        for check in result.checks:
            mark = "✅" if check.passed else "❌"
            print(f"{mark} {check.name}: {check.message}")

    return 0 if result.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
