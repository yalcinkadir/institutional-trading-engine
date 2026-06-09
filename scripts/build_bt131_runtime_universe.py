#!/usr/bin/env python3
"""Build a BT131 runtime universe from a historical coverage manifest.

The BT131 workflow ingests a requested symbol set into a run-local coverage
manifest. A static survivorship universe can contain symbols that were not
requested in this run, and it may omit newly requested ETFs/equities. This
script creates a conservative run-local universe containing only symbols with
successful coverage in the current run.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


FIELDNAMES = [
    "symbol",
    "effective_from",
    "effective_to",
    "active",
    "asset_class",
    "exchange",
    "source",
    "status",
    "reason",
]

ETF_SYMBOLS = {"SPY", "QQQ", "GLD", "SLV", "VIXY"}
NYSE_ARCA_SYMBOLS = {"SPY", "GLD", "SLV", "VIXY"}


def _asset_class(symbol: str) -> str:
    return "etf" if symbol.upper() in ETF_SYMBOLS else "equity"


def _exchange(symbol: str) -> str:
    return "NYSEARCA" if symbol.upper() in NYSE_ARCA_SYMBOLS else "NASDAQ"


def _load_manifest(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise SystemExit(f"coverage manifest not found: {path}")
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise SystemExit("coverage manifest must be a JSON object")
    return payload


def _covered_symbols(manifest: dict[str, Any]) -> list[str]:
    symbols = manifest.get("symbols")
    if not isinstance(symbols, list):
        raise SystemExit("coverage manifest missing symbols list")

    covered: list[str] = []
    for item in symbols:
        if not isinstance(item, dict):
            continue
        symbol = str(item.get("symbol") or "").strip().upper()
        status = str(item.get("status") or "").strip().lower()
        bar_count = int(item.get("bar_count") or item.get("rows_written") or item.get("rows_fetched") or 0)
        if symbol and status == "ok" and bar_count > 0:
            covered.append(symbol)

    if not covered:
        raise SystemExit("coverage manifest contains no covered symbols")
    return sorted(dict.fromkeys(covered))


def build_runtime_universe(manifest_path: Path, output_path: Path) -> dict[str, Any]:
    manifest = _load_manifest(manifest_path)
    symbols = _covered_symbols(manifest)
    start = str(manifest.get("requested_start_date") or "1900-01-01")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
        writer.writeheader()
        for symbol in symbols:
            writer.writerow(
                {
                    "symbol": symbol,
                    "effective_from": start,
                    "effective_to": "",
                    "active": "true",
                    "asset_class": _asset_class(symbol),
                    "exchange": _exchange(symbol),
                    "source": "bt131_runtime_coverage_manifest",
                    "status": "active",
                    "reason": "covered in BT131 historical ingestion run",
                }
            )

    return {
        "coverage_manifest": str(manifest_path),
        "runtime_universe": str(output_path),
        "symbol_count": len(symbols),
        "symbols": symbols,
        "status": "OK",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--coverage-manifest", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--summary-output", required=False)
    args = parser.parse_args()

    summary = build_runtime_universe(Path(args.coverage_manifest), Path(args.output))
    summary_text = json.dumps(summary, indent=2, sort_keys=True) + "\n"
    if args.summary_output:
        summary_path = Path(args.summary_output)
        summary_path.parent.mkdir(parents=True, exist_ok=True)
        summary_path.write_text(summary_text, encoding="utf-8")
    print(summary_text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
