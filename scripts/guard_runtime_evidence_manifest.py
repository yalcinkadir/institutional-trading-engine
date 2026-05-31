"""
Guard a daily runtime evidence manifest.

Examples:

python scripts/guard_runtime_evidence_manifest.py --trading-date 2026-05-31

python scripts/guard_runtime_evidence_manifest.py \
  --manifest reports/evidence/manifests/2026-05-31-runtime-evidence-manifest.json \
  --report reports/evidence/manifests/2026-05-31-runtime-evidence-guard.json
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from src.operations.runtime_evidence_manifest_guard import (
    evaluate_runtime_evidence_manifest_file,
    evaluate_runtime_evidence_manifest_for_date,
    write_manifest_guard_report,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fail closed when a daily runtime evidence manifest is missing or invalid."
    )
    parser.add_argument(
        "--trading-date",
        help="Trading date in YYYY-MM-DD format. Used with --manifest-dir.",
    )
    parser.add_argument(
        "--manifest",
        help="Explicit manifest path. Takes precedence over --trading-date.",
    )
    parser.add_argument(
        "--manifest-dir",
        default="reports/evidence/manifests",
        help="Directory containing daily runtime evidence manifests.",
    )
    parser.add_argument(
        "--report",
        help="Optional JSON path where the guard result should be written.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if args.manifest:
        result = evaluate_runtime_evidence_manifest_file(Path(args.manifest))
    elif args.trading_date:
        result = evaluate_runtime_evidence_manifest_for_date(
            args.trading_date,
            manifest_dir=Path(args.manifest_dir),
        )
    else:
        raise SystemExit("Provide either --manifest or --trading-date.")

    if args.report:
        write_manifest_guard_report(result, output_path=Path(args.report))

    print(json.dumps(result.to_dict(), indent=2, sort_keys=True))

    return 0 if result.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())