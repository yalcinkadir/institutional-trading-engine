"""Historical Polygon aggregate ingestion.

P23 scope: daily OHLCV bars, deterministic local storage and mocked tests.

Storage intentionally uses CSV plus JSON metadata because the project currently
has pandas but no parquet engine dependency such as pyarrow or fastparquet.
"""

from __future__ import annotations

import json
import os
import time
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Protocol

import pandas as pd
import requests


DEFAULT_HISTORICAL_ROOT = Path("data/historical")
DEFAULT_METADATA_PATH = DEFAULT_HISTORICAL_ROOT / "metadata" / "ingestion_status.json"


class HttpClient(Protocol):
    def get(self, url: str, *, params: dict[str, Any], timeout: int) -> Any: ...


@dataclass(frozen=True)
class HistoricalIngestionResult:
    symbol: str
    timespan: str
    multiplier: int
    start_date: str
    end_date: str
    rows_fetched: int
    rows_written: int
    output_path: str
    status: str
    message: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class HistoricalIngestionBatchResult:
    results: list[HistoricalIngestionResult] = field(default_factory=list)

    @property
    def success_count(self) -> int:
        return sum(1 for result in self.results if result.status == "ok")

    @property
    def warning_count(self) -> int:
        return sum(1 for result in self.results if result.status != "ok")

    def to_dict(self) -> dict[str, Any]:
        return {
            "success_count": self.success_count,
            "warning_count": self.warning_count,
            "results": [result.to_dict() for result in self.results],
        }


def utc_now_iso() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat()


def polygon_aggregate_url(symbol: str, multiplier: int, timespan: str, start_date: str, end_date: str) -> str:
    return (
        f"https://api.polygon.io/v2/aggs/ticker/{symbol}/range/"
        f"{multiplier}/{timespan}/{start_date}/{end_date}"
    )


def normalize_polygon_aggregate_bars(results: list[dict[str, Any]]) -> pd.DataFrame:
    """Normalize Polygon aggregate results into date/open/high/low/close/volume rows."""
    rows: list[dict[str, Any]] = []
    for item in results:
        if not isinstance(item, dict):
            continue
        timestamp = item.get("t")
        if timestamp is None:
            continue
        try:
            dt = datetime.fromtimestamp(float(timestamp) / 1000, tz=UTC)
            rows.append(
                {
                    "date": dt.date().isoformat(),
                    "timestamp": dt.isoformat(),
                    "open": float(item["o"]),
                    "high": float(item["h"]),
                    "low": float(item["l"]),
                    "close": float(item["c"]),
                    "volume": float(item.get("v", 0.0)),
                }
            )
        except (KeyError, TypeError, ValueError):
            continue

    if not rows:
        return pd.DataFrame(columns=["date", "timestamp", "open", "high", "low", "close", "volume"])

    df = pd.DataFrame(rows)
    df = df.drop_duplicates(subset=["timestamp"]).sort_values("timestamp").reset_index(drop=True)
    return df[["date", "timestamp", "open", "high", "low", "close", "volume"]]


def _read_existing_bars(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame(columns=["date", "timestamp", "open", "high", "low", "close", "volume"])
    try:
        return pd.read_csv(path)
    except Exception:
        return pd.DataFrame(columns=["date", "timestamp", "open", "high", "low", "close", "volume"])


def merge_and_save_bars(df: pd.DataFrame, output_path: Path) -> int:
    """Merge new bars with existing CSV storage and remove duplicates."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    existing = _read_existing_bars(output_path)
    combined = pd.concat([existing, df], ignore_index=True)
    if combined.empty:
        combined.to_csv(output_path, index=False)
        return 0
    combined = combined.drop_duplicates(subset=["timestamp"]).sort_values("timestamp").reset_index(drop=True)
    combined.to_csv(output_path, index=False)
    return int(len(combined))


def _load_metadata(metadata_path: Path) -> dict[str, Any]:
    if not metadata_path.exists():
        return {"updated_at": None, "symbols": {}}
    try:
        payload = json.loads(metadata_path.read_text(encoding="utf-8"))
        if isinstance(payload, dict):
            payload.setdefault("symbols", {})
            return payload
    except json.JSONDecodeError:
        pass
    return {"updated_at": None, "symbols": {}}


def update_ingestion_metadata(metadata_path: Path, result: HistoricalIngestionResult) -> None:
    metadata_path.parent.mkdir(parents=True, exist_ok=True)
    metadata = _load_metadata(metadata_path)
    metadata["updated_at"] = utc_now_iso()
    key = f"{result.symbol}:{result.multiplier}:{result.timespan}"
    metadata["symbols"][key] = result.to_dict() | {"last_updated_at": metadata["updated_at"]}
    metadata_path.write_text(json.dumps(metadata, indent=2, sort_keys=True), encoding="utf-8")


def fetch_polygon_aggregate_bars(
    *,
    symbol: str,
    start_date: str,
    end_date: str,
    api_key: str,
    multiplier: int = 1,
    timespan: str = "day",
    http_client: HttpClient = requests,
    retries: int = 3,
    sleep_seconds: float = 1.0,
) -> list[dict[str, Any]]:
    """Fetch Polygon aggregate bars with simple retry/rate-limit handling."""
    url = polygon_aggregate_url(symbol, multiplier, timespan, start_date, end_date)
    params = {
        "adjusted": "true",
        "sort": "asc",
        "limit": 50000,
        "apiKey": api_key,
    }

    last_error = ""
    for attempt in range(retries):
        response = http_client.get(url, params=params, timeout=30)
        status_code = int(getattr(response, "status_code", 0))
        if status_code == 429 or status_code >= 500:
            last_error = f"HTTP {status_code}"
            if attempt < retries - 1:
                time.sleep(sleep_seconds)
                continue
        if hasattr(response, "raise_for_status"):
            response.raise_for_status()
        payload = response.json()
        results = payload.get("results", []) if isinstance(payload, dict) else []
        return results if isinstance(results, list) else []

    raise RuntimeError(f"Polygon request failed after {retries} retries: {last_error}")


def ingest_historical_symbol(
    *,
    symbol: str,
    start_date: str,
    end_date: str,
    api_key: str | None = None,
    multiplier: int = 1,
    timespan: str = "day",
    output_root: Path = DEFAULT_HISTORICAL_ROOT,
    metadata_path: Path = DEFAULT_METADATA_PATH,
    http_client: HttpClient = requests,
) -> HistoricalIngestionResult:
    """Fetch, normalize, store and register historical bars for one symbol."""
    resolved_api_key = api_key or os.getenv("POLYGON_API_KEY")
    output_path = output_root / "bars" / f"{multiplier}{timespan}" / f"{symbol}.csv"

    if not resolved_api_key:
        result = HistoricalIngestionResult(
            symbol=symbol,
            timespan=timespan,
            multiplier=multiplier,
            start_date=start_date,
            end_date=end_date,
            rows_fetched=0,
            rows_written=0,
            output_path=str(output_path),
            status="error",
            message="missing POLYGON_API_KEY",
        )
        update_ingestion_metadata(metadata_path, result)
        return result

    try:
        raw_bars = fetch_polygon_aggregate_bars(
            symbol=symbol,
            start_date=start_date,
            end_date=end_date,
            api_key=resolved_api_key,
            multiplier=multiplier,
            timespan=timespan,
            http_client=http_client,
        )
        df = normalize_polygon_aggregate_bars(raw_bars)
        rows_written = merge_and_save_bars(df, output_path)
        status = "ok" if not df.empty else "empty"
        message = "" if status == "ok" else "Polygon returned no usable bars"
        result = HistoricalIngestionResult(
            symbol=symbol,
            timespan=timespan,
            multiplier=multiplier,
            start_date=start_date,
            end_date=end_date,
            rows_fetched=len(raw_bars),
            rows_written=rows_written,
            output_path=str(output_path),
            status=status,
            message=message,
        )
    except Exception as exc:
        result = HistoricalIngestionResult(
            symbol=symbol,
            timespan=timespan,
            multiplier=multiplier,
            start_date=start_date,
            end_date=end_date,
            rows_fetched=0,
            rows_written=0,
            output_path=str(output_path),
            status="error",
            message=f"{type(exc).__name__}: {exc}",
        )

    update_ingestion_metadata(metadata_path, result)
    return result


def ingest_historical_symbols(
    *,
    symbols: list[str],
    start_date: str,
    end_date: str,
    api_key: str | None = None,
    multiplier: int = 1,
    timespan: str = "day",
    output_root: Path = DEFAULT_HISTORICAL_ROOT,
    metadata_path: Path = DEFAULT_METADATA_PATH,
    http_client: HttpClient = requests,
) -> HistoricalIngestionBatchResult:
    results = [
        ingest_historical_symbol(
            symbol=symbol,
            start_date=start_date,
            end_date=end_date,
            api_key=api_key,
            multiplier=multiplier,
            timespan=timespan,
            output_root=output_root,
            metadata_path=metadata_path,
            http_client=http_client,
        )
        for symbol in symbols
    ]
    return HistoricalIngestionBatchResult(results=results)
