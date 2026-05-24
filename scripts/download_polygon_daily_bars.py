"""Download Polygon daily OHLCV bars for a universe CSV."""

from __future__ import annotations

import argparse
import csv
import os
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import requests

BAR_COLUMNS = ["date", "open", "high", "low", "close", "volume"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Download Polygon daily bars")
    parser.add_argument("--universe", type=Path, default=Path("data/universe/survivorship_universe.csv"))
    parser.add_argument("--output-dir", type=Path, default=Path("data/historical_bars"))
    parser.add_argument("--from-date", default="2016-01-01")
    parser.add_argument("--to-date", default="2026-05-24")
    parser.add_argument("--max-symbols", type=int, default=0, help="0 means no limit")
    parser.add_argument("--min-bars", type=int, default=120)
    parser.add_argument("--sleep-seconds", type=float, default=0.0)
    parser.add_argument("--manifest", type=Path, default=Path("reports/edge_evidence_data/polygon-bars-manifest.md"))
    return parser.parse_args()


def _credential() -> str:
    value = os.environ.get("POLYGON_API_KEY", "").strip()
    if not value:
        raise SystemExit("POLYGON_API_KEY is required")
    return value


def load_symbols(path: Path) -> list[str]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        return [str(row.get("symbol") or "").upper().strip() for row in reader if row.get("symbol")]


def fetch_bars(session: requests.Session, symbol: str, *, from_date: str, to_date: str, token: str) -> list[dict[str, Any]]:
    url = f"https://api.polygon.io/v2/aggs/ticker/{symbol}/range/1/day/{from_date}/{to_date}"
    response = session.get(
        url,
        params={"adjusted": "true", "sort": "asc", "limit": 50000, "apiKey": token},
        timeout=60,
    )
    if response.status_code == 429:
        raise RuntimeError("rate limit reached")
    response.raise_for_status()
    payload = response.json()
    if not isinstance(payload, dict):
        raise RuntimeError("unexpected JSON payload")
    return [item for item in payload.get("results") or [] if isinstance(item, dict)]


def bar_to_row(bar: dict[str, Any]) -> dict[str, Any]:
    day = datetime.fromtimestamp(int(bar.get("t") or 0) / 1000, UTC).date().isoformat()
    return {
        "date": day,
        "open": bar.get("o"),
        "high": bar.get("h"),
        "low": bar.get("l"),
        "close": bar.get("c"),
        "volume": bar.get("v"),
    }


def write_bars(symbol: str, bars: list[dict[str, Any]], output_dir: Path) -> int:
    output_dir.mkdir(parents=True, exist_ok=True)
    with (output_dir / f"{symbol}.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=BAR_COLUMNS)
        writer.writeheader()
        for bar in bars:
            writer.writerow(bar_to_row(bar))
    return len(bars)


def write_manifest(path: Path, *, requested: int, downloaded: int, skipped: int, failed: int, bars_written: int, failures: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Polygon Daily Bars Download",
        "",
        f"Requested symbols: **{requested}**",
        f"Downloaded symbols: **{downloaded}**",
        f"Skipped symbols: **{skipped}**",
        f"Failed symbols: **{failed}**",
        f"Bars written: **{bars_written}**",
        "",
        "## Failures / skips",
        "",
    ]
    lines.extend(f"- {item}" for item in failures[:200]) if failures else lines.append("- none")
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def main() -> int:
    args = parse_args()
    token = _credential()
    symbols = load_symbols(args.universe)
    max_symbols = args.max_symbols if args.max_symbols > 0 else None
    session = requests.Session()

    requested = downloaded = skipped = failed = bars_written = 0
    failures: list[str] = []
    for symbol in symbols:
        if max_symbols is not None and requested >= max_symbols:
            break
        requested += 1
        try:
            bars = fetch_bars(session, symbol, from_date=args.from_date, to_date=args.to_date, token=token)
            if len(bars) < args.min_bars:
                skipped += 1
                failures.append(f"{symbol}: insufficient bars ({len(bars)} < {args.min_bars})")
                continue
            bars_written += write_bars(symbol, bars, args.output_dir)
            downloaded += 1
        except Exception as exc:  # noqa: BLE001
            failed += 1
            failures.append(f"{symbol}: {exc}")
        if args.sleep_seconds:
            time.sleep(args.sleep_seconds)

    write_manifest(
        args.manifest,
        requested=requested,
        downloaded=downloaded,
        skipped=skipped,
        failed=failed,
        bars_written=bars_written,
        failures=failures,
    )
    print(f"Downloaded bars for {downloaded}/{requested} symbols")
    if downloaded < 500 and max_symbols is None:
        raise SystemExit("Fewer than 500 symbols have usable bars")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
