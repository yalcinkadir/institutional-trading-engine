#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.validation.execution_kill_switch import (  # noqa: E402
    evaluate_execution_kill_switch,
    load_kill_switch_input,
    write_execution_kill_switch_decision,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Evaluate C7 execution kill-switch governance gates.")
    parser.add_argument(
        "--input-file",
        type=Path,
        required=True,
        help="JSON file with daily_reconciliation_report, fill_quality_report, drawdown_source_validation and optional manual_risk_flags.",
    )
    parser.add_argument("--output-dir", type=Path, required=True, help="Directory for JSON and Markdown decision output.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    payload = load_kill_switch_input(args.input_file)
    decision = evaluate_execution_kill_switch(
        daily_reconciliation_report=payload.get("daily_reconciliation_report"),
        fill_quality_report=payload.get("fill_quality_report"),
        drawdown_source_validation=payload.get("drawdown_source_validation"),
        manual_risk_flags=payload.get("manual_risk_flags", []),
    )
    write_execution_kill_switch_decision(
        decision,
        json_path=args.output_dir / "execution_kill_switch_decision.json",
        markdown_path=args.output_dir / "execution_kill_switch_decision.md",
    )
    print(f"Execution kill-switch status: {decision.status.value}")
    print(f"Blocked: {str(decision.blocked).lower()}")
    print(f"Reasons: {len(decision.reasons)}")
    return 1 if decision.blocked else 0


if __name__ == "__main__":
    raise SystemExit(main())
