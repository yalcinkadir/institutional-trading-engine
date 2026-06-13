#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.validation.production_readiness_gate import evaluate_production_readiness


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build unified production readiness evidence.")
    parser.add_argument("--paper-health-file", default="reports/validation/latest-paper-observation-health.json")
    parser.add_argument("--scheduled-liveness-file", default="reports/health/report-liveness-latest.json")
    parser.add_argument("--signals-file", default="reports/signals/latest-signals.json")
    parser.add_argument("--watcher-lifecycle-file", default="reports/backtests/real_data/latest/bt207-watcher-coupled-lifecycle-report.json")
    parser.add_argument("--backtest-file", default="reports/backtests/real_data/latest/bt207-watcher-coupled-lifecycle-report.json")
    parser.add_argument("--output-file", default="reports/readiness/latest-production-readiness.json")
    parser.add_argument("--backtest-min-sample", type=int, default=30)
    parser.add_argument("--workflow-name", default=os.environ.get("GITHUB_WORKFLOW"))
    parser.add_argument("--commit-sha", default=os.environ.get("GITHUB_SHA"))
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    report = evaluate_production_readiness(
        paper_health=_read_json(args.paper_health_file),
        scheduled_liveness=_read_json(args.scheduled_liveness_file),
        signals=_read_json(args.signals_file),
        watcher_lifecycle=_read_json(args.watcher_lifecycle_file),
        backtest=_read_json(args.backtest_file),
        commit_sha=args.commit_sha,
        workflow_name=args.workflow_name,
        backtest_min_sample=args.backtest_min_sample,
    )

    output_file = Path(args.output_file)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(f"Production readiness: {'PASS' if report['production_ready'] else 'BLOCKED'}")
    print(f"Paper observation ready: {report['paper_observation_ready']}")
    print(f"Backtesting ready: {report['backtesting_ready']}")
    print(f"Live trading authorized: {report['live_trading_authorized']}")
    print(f"Capital allocation authorized: {report['capital_allocation_authorized']}")
    print(f"Output file: {output_file}")
    if report["blockers"]:
        print("Blockers:")
        for blocker in report["blockers"]:
            print(f"- {blocker}")

    return 0 if report["production_ready"] else 1


def _read_json(path_value: str | None) -> dict[str, Any]:
    if not path_value:
        return {}
    path = Path(path_value)
    if not path.exists():
        return {}
    payload = json.loads(path.read_text(encoding="utf-8"))
    return payload if isinstance(payload, dict) else {}


if __name__ == "__main__":
    raise SystemExit(main())
