from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.validation.backtesting_evidence_report import (  # noqa: E402
    load_backtesting_evidence_report_from_contracts_json,
    write_backtesting_evidence_report,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a BT8 backtesting evidence report from BT3 backtest run contracts.")
    parser.add_argument("--contracts-json", required=True, help="Path to a JSON file containing BT3 backtest run contracts.")
    parser.add_argument("--output-json", required=True, help="Path for the BT8 JSON report output.")
    parser.add_argument("--output-md", required=True, help="Path for the BT8 Markdown report output.")
    parser.add_argument("--generated-at", default=None, help="Optional deterministic generation timestamp.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    report = load_backtesting_evidence_report_from_contracts_json(
        Path(args.contracts_json),
        generated_at=args.generated_at,
    )
    write_backtesting_evidence_report(
        report,
        output_json=Path(args.output_json),
        output_md=Path(args.output_md),
    )
    return 0 if report.summary.overall_status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
