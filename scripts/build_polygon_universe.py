"""Build an active Polygon universe CSV for edge-evidence runs.

By default this command walks all available active tickers returned by Polygon
for the selected market. Use --max-symbols only for smoke tests or cost/rate
control.
"""

from __future__ import annotations

import argparse
import csv
import os
import time
from pathlib import Path
from typing import Any

import requests

COLUMNS = [
    "symbol",
    "active_from",
    "active_to",
    "delisting_reason",
    "successor_symbol",
    "final_close_price",
    "notes",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build active Polygon universe")
    parser.add_argument("--output", type=Path, default=Path("data/universe/survivorship_universe.csv"))
    parser.add_argument("--active-from", default="2026-05-24")
    parser.add_argument("--market", default="stocks")
    parser.add_argument("--max-symbols", type=int, default=0, help="Optional cap for tests; 0 means all available symbols")
    parser.add_argument("--sleep-seconds", type=float, default=0.0)
    return parser.parse_args()


def _credential() -> str:
    value = os.environ.get("POLYGON_API_KEY", "").strip()
    if not value:
        raise SystemExit("POLYGON_API_KEY is required")
    return value


def _with_api_key(params: dict[str, Any] | None, token: str) -> dict[str, Any]:
    payload = dict(params or {})
    payload["apiKey"] = token
    return payload


def _fetch_json(session: requests.Session, url: str, params: dict[str, Any] | None, token: str) -> dict[str, Any]:
    response = session.get(url, params=_with_api_key(params, token), timeout=30)
    if response.status_code == 429:
        raise RuntimeError("rate limit reached")
    response.raise_for_status()
    payload = response.json()
    if not isinstance(payload, dict):
        raise RuntimeError("unexpected JSON payload")
    return payload


def iter_tickers(session: requests.Session, *, market: str, sleep_seconds: float, token: str | None = None):
    credential = token or _credential()
    url = "https://api.polygon.io/v3/reference/tickers"
    params: dict[str, Any] | None = {
        "market": market,
        "active": "true",
        "limit": 1000,
        "sort": "ticker",
        "order": "asc",
    }
    while url:
        payload = _fetch_json(session, url, params, credential)
        for item in payload.get("results") or []:
            if not isinstance(item, dict):
                continue
            symbol = str(item.get("ticker") or "").upper().strip()
            if not symbol:
                continue
            yield {
                "symbol": symbol,
                "name": str(item.get("name") or "").replace(";", ","),
                "type": str(item.get("type") or "").upper(),
                "exchange": str(item.get("primary_exchange") or ""),
            }
        url = str(payload.get("next_url") or "")
        params = None
        if url and sleep_seconds:
            time.sleep(sleep_seconds)


def write_universe(args: argparse.Namespace) -> int:
    session = requests.Session()
    token = _credential()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    max_symbols = args.max_symbols if args.max_symbols > 0 else None
    with args.output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=COLUMNS)
        writer.writeheader()
        for ticker in iter_tickers(session, market=args.market, sleep_seconds=args.sleep_seconds, token=token):
            if max_symbols is not None and count >= max_symbols:
                break
            notes = (
                "source=polygon_reference_tickers;"
                "classification=active_polygon_universe;"
                f"type={ticker['type']};exchange={ticker['exchange']};name={ticker['name']}"
            )
            writer.writerow(
                {
                    "symbol": ticker["symbol"],
                    "active_from": args.active_from,
                    "active_to": "",
                    "delisting_reason": "",
                    "successor_symbol": "",
                    "final_close_price": "",
                    "notes": notes,
                }
            )
            count += 1
    return count


def main() -> int:
    args = parse_args()
    count = write_universe(args)
    print(f"Wrote {count} active symbols to {args.output}")
    if count < 500:
        raise SystemExit("Polygon universe has fewer than 500 symbols")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
