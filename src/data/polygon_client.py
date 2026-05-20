from __future__ import annotations

import json
import os
import time
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any

import requests

BASE_URL = "https://api.polygon.io"
CACHE_DIR = Path(os.getenv("POLYGON_CACHE_DIR", ".cache/polygon"))
CACHE_TTL_SECONDS = int(os.getenv("POLYGON_CACHE_TTL_SECONDS", "21600"))
MAX_RETRIES = int(os.getenv("POLYGON_MAX_RETRIES", "3"))
BACKOFF_SECONDS = float(os.getenv("POLYGON_BACKOFF_SECONDS", "2"))


class PolygonClient:
    def __init__(self, api_key: str | None = None) -> None:
        self.api_key = api_key or os.getenv("POLYGON_API_KEY")

        if not self.api_key:
            raise ValueError("POLYGON_API_KEY is missing")

        CACHE_DIR.mkdir(parents=True, exist_ok=True)

    def get_daily_bars(self, ticker: str, days: int = 250) -> list[dict]:
        cache_key = self._cache_key(ticker, days)
        cached = self._read_cache(cache_key)

        if cached is not None:
            return cached

        end_date = datetime.utcnow().date()
        start_date = end_date - timedelta(days=days * 2)

        results = self.get_daily_bars_range(
            ticker=ticker,
            start_date=start_date,
            end_date=end_date,
            limit=days,
            use_ttl_cache=False,
        )

        self._write_cache(cache_key, results)

        return results

    def get_daily_bars_range(
        self,
        ticker: str,
        start_date: str | date,
        end_date: str | date,
        *,
        limit: int = 50000,
        adjusted: bool = True,
        use_ttl_cache: bool = True,
    ) -> list[dict]:
        """Fetch historical daily aggregate bars for an explicit date range.

        This wraps Polygon's `/v2/aggs/ticker/{ticker}/range/1/day/...` endpoint
        and keeps data access isolated behind the client for backtesting and
        historical validation flows.
        """

        start = self._normalize_date(start_date)
        end = self._normalize_date(end_date)
        cache_key = self._range_cache_key(ticker, start, end, adjusted=adjusted, limit=limit)

        cached = self._read_cache(cache_key) if use_ttl_cache else None
        if cached is not None:
            return cached

        url = f"{BASE_URL}/v2/aggs/ticker/{ticker}/range/1/day/{start}/{end}"

        payload = self._request_with_retry(
            url,
            params={
                "adjusted": str(adjusted).lower(),
                "sort": "asc",
                "limit": limit,
                "apiKey": self.api_key,
            },
        )

        results = payload.get("results", [])
        self._write_cache(cache_key, results)

        return results

    def _request_with_retry(self, url: str, params: dict[str, Any]) -> dict:
        last_error: Exception | None = None

        for attempt in range(1, MAX_RETRIES + 1):
            try:
                response = requests.get(url, params=params, timeout=30)

                if response.status_code == 429:
                    retry_after = response.headers.get("Retry-After")
                    wait_seconds = float(retry_after) if retry_after else BACKOFF_SECONDS * attempt
                    print(f"Polygon rate limit hit. Retry {attempt}/{MAX_RETRIES} in {wait_seconds}s")
                    time.sleep(wait_seconds)
                    continue

                if 500 <= response.status_code < 600:
                    wait_seconds = BACKOFF_SECONDS * attempt
                    print(f"Polygon server error {response.status_code}. Retry {attempt}/{MAX_RETRIES} in {wait_seconds}s")
                    time.sleep(wait_seconds)
                    continue

                response.raise_for_status()
                return response.json()
            except requests.RequestException as exc:
                last_error = exc
                wait_seconds = BACKOFF_SECONDS * attempt
                print(f"Polygon request failed: {exc}. Retry {attempt}/{MAX_RETRIES} in {wait_seconds}s")
                time.sleep(wait_seconds)

        raise RuntimeError(f"Polygon request failed after {MAX_RETRIES} retries: {last_error}")

    def _cache_key(self, ticker: str, days: int) -> Path:
        safe_ticker = self._safe_ticker(ticker)
        current_date = datetime.utcnow().strftime("%Y-%m-%d")
        return CACHE_DIR / f"{safe_ticker}_{days}_{current_date}.json"

    def _range_cache_key(
        self,
        ticker: str,
        start_date: str,
        end_date: str,
        *,
        adjusted: bool,
        limit: int,
    ) -> Path:
        safe_ticker = self._safe_ticker(ticker)
        adjusted_suffix = "adjusted" if adjusted else "raw"
        return CACHE_DIR / "historical" / f"{safe_ticker}_1d_{start_date}_{end_date}_{adjusted_suffix}_{limit}.json"

    def _read_cache(self, cache_file: Path) -> list[dict] | None:
        if not cache_file.exists():
            return None

        age_seconds = time.time() - cache_file.stat().st_mtime
        if age_seconds > CACHE_TTL_SECONDS:
            return None

        try:
            return json.loads(cache_file.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return None

    def _write_cache(self, cache_file: Path, payload: list[dict]) -> None:
        cache_file.parent.mkdir(parents=True, exist_ok=True)
        cache_file.write_text(json.dumps(payload), encoding="utf-8")

    @staticmethod
    def _safe_ticker(ticker: str) -> str:
        return ticker.replace(":", "_").replace("/", "_")

    @staticmethod
    def _normalize_date(value: str | date) -> str:
        if isinstance(value, date):
            return value.isoformat()
        return value
