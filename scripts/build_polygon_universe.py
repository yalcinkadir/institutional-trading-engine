"""Build an active Polygon universe CSV for edge-evidence runs.

By default this command walks all available active tickers returned by Polygon
for the selected market. Use --max-symbols only for smoke tests or cost/rate
control.
"""

from __future__ import annotations

import argparse
import csv
import logging
import os
import time
from pathlib import Path
from typing import Any

import requests

from src.observability.structured_logging import configure_json_logging, emit_structured_log

LOGGER = logging.getLogger("polygon.universe")
COMPONENT = "polygon_universe_builder"

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
    status_code = int(response.status_code)
    if status_code == 429:
        emit_structured_log(
            LOGGER,
            event="polygon_rate_limit",
            level="WARNING",
            component=COMPONENT,
            url=url,
            status_code=status_code,
        )
        raise RuntimeError("rate limit reached")
    try:
        response.raise_for_status()
    except Exception:
        emit_structured_log(
            LOGGER,
            event="polygon_http_error",
            level="ERROR",
            component=COMPONENT,
            url=url,
            status_code=status_code,
        )
        raise
    payload = response.json()
    if not isinstance(payload, dict):
        emit_structured_log(
            LOGGER,
            event="polygon_unexpected_payload",
            level="ERROR",
            component=COMPONENT,
            url=url,
            payload_type=type(payload).__name__,
        )
        raise RuntimeError("unexpected JSON payload")
    emit_structured_log(
        LOGGER,
        event="polygon_page_fetched",
        component=COMPONENT,
        url=url,
        status_code=status_code,
        result_count=len(payload.get("results") or []),
        has_next_url=bool(payload.get("next_url")),
    )
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
    page = 0
    while url:
        page += 1
        emit_structured_log(
            LOGGER,
            event="polygon_ticker_page_request",
            component=COMPONENT,
            page=page,
            market=market,
            has_params=params is not None,
        )
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
            emit_structured_log(
                LOGGER,
                event="polygon_sleep_between_pages",
                component=COMPONENT,
                sleep_seconds=sleep_seconds,
                next_page=page + 1,
            )
            time.sleep(sleep_seconds)


def write_universe(args: argparse.Namespace) -> int:
    session = requests.Session()
    token = _credential()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    duplicates = 0
    seen_symbols: set[str] = set()
    max_symbols = args.max_symbols if args.max_symbols > 0 else None
    emit_structured_log(
        LOGGER,
        event="polygon_universe_build_started",
        component=COMPONENT,
        output=str(args.output),
        market=args.market,
        max_symbols=args.max_symbols,
    )
    with args.output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=COLUMNS)
        writer.writeheader()
        for ticker in iter_tickers(session, market=args.market, sleep_seconds=args.sleep_seconds, token=token):
            symbol = ticker["symbol"]
            if symbol in seen_symbols:
                duplicates += 1
                emit_structured_log(
                    LOGGER,
                    event="polygon_duplicate_symbol_skipped",
                    component=COMPONENT,
                    symbol=symbol,
                    duplicates=duplicates,
                )
                continue
            seen_symbols.add(symbol)
            if max_symbols is not None and count >= max_symbols:
                break
            notes = (
                "source=polygon_reference_tickers;"
                "classification=active_polygon_universe;"
                f"type={ticker['type']};exchange={ticker['exchange']};name={ticker['name']}"
            )
            writer.writerow(
                {
                    "symbol": symbol,
                    "active_from": args.active_from,
                    "active_to": "",
                    "delisting_reason": "",
                    "successor_symbol": "",
                    "final_close_price": "",
                    "notes": notes,
                }
            )
            count += 1
    if duplicates:
        emit_structured_log(
            LOGGER,
            event="polygon_duplicate_symbols_summary",
            component=COMPONENT,
            duplicates=duplicates,
        )
    emit_structured_log(
        LOGGER,
        event="polygon_universe_build_completed",
        component=COMPONENT,
        output=str(args.output),
        symbols_written=count,
        duplicates=duplicates,
    )
    return count


def main() -> int:
    configure_json_logging()
    args = parse_args()
    count = write_universe(args)
    emit_structured_log(
        LOGGER,
        event="polygon_universe_output_written",
        component=COMPONENT,
        output=str(args.output),
        symbols_written=count,
    )
    if count < 500:
        emit_structured_log(
            LOGGER,
            event="polygon_universe_coverage_failed",
            level="ERROR",
            component=COMPONENT,
            symbols_written=count,
            minimum_required=500,
        )
        raise SystemExit("Polygon universe has fewer than 500 symbols")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())