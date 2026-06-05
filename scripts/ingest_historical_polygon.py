#!/usr/bin/env python3
"""Ingest historical Polygon aggregate bars."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.historical.polygon_ingestion import ingest_historical_symbols


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Ingest historical Polygon aggregate bars.")
    parser.add_argument("--symbols", required=True, help="Comma-separated symbols, e.g. NVDA,AAPL,SPY")
    parser.add_argument("--start-date", required=True, help="YYYY-MM-DD")
    parser.add_argument("--end-date", required=True, help="YYYY-MM-DD")
    parser.add_argument("--multiplier", type=int, default=1)
    parser.add_argument("--timespan", default="day")
    parser.add_argument("--output-root", default="data/historical")
    parser.add_argument("--metadata-path", default="data/historical/metadata/ingestion_status.json")
    parser.add_argument("--coverage-manifest-path", default="data/historical/metadata/coverage_manifest.json")
    parser.add_argument("--json", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    symbols = [symbol.strip().upper() for symbol in args.symbols.split(",") if symbol.strip()]
    if not symbols:
        print("No symbols provided.", file=sys.stderr)
        return 2

    result = ingest_historical_symbols(
        symbols=symbols,
        start_date=args.start_date,
        end_date=args.end_date,
        multiplier=args.multiplier,
        timespan=args.timespan,
        output_root=Path(args.output_root),
        metadata_path=Path(args.metadata_path),
        coverage_manifest_path=Path(args.coverage_manifest_path),
    )

    if args.json:
        print(json.dumps(result.to_dict(), indent=2))
    else:
        print(f"Historical ingestion completed: {result.success_count} ok, {result.warning_count} warnings/errors")
        if result.coverage_manifest_path:
            print(f"Coverage manifest: {result.coverage_manifest_path}")
        for item in result.results:
            mark = "OK" if item.status == "ok" else "WARN"
            print(
                f"{mark} {item.symbol} {item.multiplier}{item.timespan} "
                f"{item.start_date}->{item.end_date}: {item.status} | "
                f"fetched={item.rows_fetched} written={item.rows_written} | {item.output_path}"
            )
            if item.message:
                print(f"   {item.message}")

    return 0 if result.warning_count == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
