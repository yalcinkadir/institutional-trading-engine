"""Download Polygon daily OHLCV bars for a universe CSV."""

from __future__ import annotations

import argparse
import csv
import logging
import os
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import requests

from src.observability.structured_logging import configure_json_logging, emit_structured_log

LOGGER = logging.getLogger("polygon.daily_bars")
COMPONENT = "polygon_daily_bars_downloader"

BAR_COLUMNS = ["date", "open", "high", "low", "close", "volume"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Download Polygon daily bars")
    parser.add_argument("--universe", type=Path, default=Path("data/universe/survivorship_universe.csv"))
    parser.add_argument("--output-dir", type=Path, default=Path("data/historical_bars"))
    parser.add_argument("--from-date", default="2016-01-01")
    parser.add_argument("--to-date", default="2026-05-24")
    parser.add_argument("--max-symbols", type=int, default=0, help="0 means no limit")
    parser.add_argument("--batch-size", type=int, default=0, help="0 means one full-universe batch")
    parser.add_argument("--batch-index", type=int, default=0, help="Zero-based batch index when --batch-size is set")
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
        symbols = [str(row.get("symbol") or "").upper().strip() for row in reader if row.get("symbol")]
    emit_structured_log(
        LOGGER,
        event="polygon_universe_symbols_loaded",
        component=COMPONENT,
        path=str(path),
        symbol_count=len(symbols),
    )
    return symbols


def select_symbol_batch(symbols: list[str], *, batch_size: int, batch_index: int, max_symbols: int = 0) -> list[str]:
    if batch_index < 0:
        raise ValueError("batch_index must be >= 0")
    if batch_size < 0:
        raise ValueError("batch_size must be >= 0")
    selected = symbols
    if max_symbols > 0:
        selected = selected[:max_symbols]
    if batch_size <= 0:
        return selected
    start = batch_index * batch_size
    end = start + batch_size
    return selected[start:end]


def fetch_bars(session: requests.Session, symbol: str, *, from_date: str, to_date: str, token: str) -> list[dict[str, Any]]:
    url = f"https://api.polygon.io/v2/aggs/ticker/{symbol}/range/1/day/{from_date}/{to_date}"
    emit_structured_log(
        LOGGER,
        event="polygon_bars_request",
        component=COMPONENT,
        symbol=symbol,
        from_date=from_date,
        to_date=to_date,
    )
    response = session.get(
        url,
        params={"adjusted": "true", "sort": "asc", "limit": 50000, "apiKey": token},
        timeout=60,
    )
    status_code = int(response.status_code)
    if status_code == 429:
        emit_structured_log(
            LOGGER,
            event="polygon_rate_limit",
            level="WARNING",
            component=COMPONENT,
            symbol=symbol,
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
            symbol=symbol,
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
            symbol=symbol,
            payload_type=type(payload).__name__,
        )
        raise RuntimeError("unexpected JSON payload")
    bars = [item for item in payload.get("results") or [] if isinstance(item, dict)]
    emit_structured_log(
        LOGGER,
        event="polygon_bars_response",
        component=COMPONENT,
        symbol=symbol,
        status_code=status_code,
        bar_count=len(bars),
    )
    return bars


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
    emit_structured_log(
        LOGGER,
        event="polygon_bars_written",
        component=COMPONENT,
        symbol=symbol,
        output=str(output_dir / f"{symbol}.csv"),
        bar_count=len(bars),
    )
    return len(bars)


def write_manifest(
    path: Path,
    *,
    requested: int,
    downloaded: int,
    skipped: int,
    failed: int,
    bars_written: int,
    failures: list[str],
    total_symbols: int = 0,
    batch_size: int = 0,
    batch_index: int = 0,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Polygon Daily Bars Download",
        "",
        f"Total universe symbols: **{total_symbols}**",
        f"Batch size: **{batch_size}**",
        f"Batch index: **{batch_index}**",
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
    emit_structured_log(
        LOGGER,
        event="polygon_bars_manifest_written",
        component=COMPONENT,
        manifest=str(path),
        requested=requested,
        downloaded=downloaded,
        skipped=skipped,
        failed=failed,
        bars_written=bars_written,
    )


def main() -> int:
    configure_json_logging()
    args = parse_args()
    token = _credential()
    all_symbols = load_symbols(args.universe)
    symbols = select_symbol_batch(
        all_symbols,
        batch_size=args.batch_size,
        batch_index=args.batch_index,
        max_symbols=args.max_symbols,
    )
    session = requests.Session()

    emit_structured_log(
        LOGGER,
        event="polygon_bars_download_started",
        component=COMPONENT,
        total_symbols=len(all_symbols),
        selected_symbols=len(symbols),
        batch_size=args.batch_size,
        batch_index=args.batch_index,
        from_date=args.from_date,
        to_date=args.to_date,
        min_bars=args.min_bars,
    )

    requested = downloaded = skipped = failed = bars_written = 0
    failures: list[str] = []
    for symbol in symbols:
        requested += 1
        try:
            bars = fetch_bars(session, symbol, from_date=args.from_date, to_date=args.to_date, token=token)
            if len(bars) < args.min_bars:
                skipped += 1
                reason = f"{symbol}: insufficient bars ({len(bars)} < {args.min_bars})"
                failures.append(reason)
                emit_structured_log(
                    LOGGER,
                    event="polygon_symbol_skipped_insufficient_bars",
                    level="WARNING",
                    component=COMPONENT,
                    symbol=symbol,
                    bar_count=len(bars),
                    min_bars=args.min_bars,
                )
                continue
            bars_written += write_bars(symbol, bars, args.output_dir)
            downloaded += 1
        except Exception as exc:  # noqa: BLE001
            failed += 1
            failures.append(f"{symbol}: {exc}")
            emit_structured_log(
                LOGGER,
                event="polygon_symbol_download_failed",
                level="ERROR",
                component=COMPONENT,
                symbol=symbol,
                error=str(exc),
                error_type=type(exc).__name__,
            )
        if args.sleep_seconds:
            emit_structured_log(
                LOGGER,
                event="polygon_sleep_between_symbols",
                component=COMPONENT,
                sleep_seconds=args.sleep_seconds,
                requested=requested,
            )
            time.sleep(args.sleep_seconds)

    write_manifest(
        args.manifest,
        requested=requested,
        downloaded=downloaded,
        skipped=skipped,
        failed=failed,
        bars_written=bars_written,
        failures=failures,
        total_symbols=len(all_symbols),
        batch_size=args.batch_size,
        batch_index=args.batch_index,
    )
    emit_structured_log(
        LOGGER,
        event="polygon_bars_download_completed",
        component=COMPONENT,
        total_symbols=len(all_symbols),
        requested=requested,
        downloaded=downloaded,
        skipped=skipped,
        failed=failed,
        bars_written=bars_written,
    )
    if downloaded < 500 and args.batch_size <= 0 and args.max_symbols <= 0:
        emit_structured_log(
            LOGGER,
            event="polygon_bars_coverage_failed",
            level="ERROR",
            component=COMPONENT,
            downloaded=downloaded,
            minimum_required=500,
        )
        raise SystemExit("Fewer than 500 symbols have usable bars")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())