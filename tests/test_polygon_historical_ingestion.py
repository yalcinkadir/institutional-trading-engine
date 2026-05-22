from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from src.historical.polygon_ingestion import (
    ingest_historical_symbol,
    ingest_historical_symbols,
    normalize_polygon_aggregate_bars,
    polygon_aggregate_url,
)


class MockResponse:
    def __init__(self, payload, status_code: int = 200):
        self._payload = payload
        self.status_code = status_code

    def json(self):
        return self._payload

    def raise_for_status(self):
        if self.status_code >= 400:
            raise RuntimeError(f"HTTP {self.status_code}")


class MockHttpClient:
    def __init__(self, payload, status_code: int = 200):
        self.payload = payload
        self.status_code = status_code
        self.calls = []

    def get(self, url, *, params, timeout):
        self.calls.append({"url": url, "params": params, "timeout": timeout})
        return MockResponse(self.payload, self.status_code)


def _polygon_bar(ts_ms: int, close: float = 100.0) -> dict:
    return {
        "t": ts_ms,
        "o": close - 1,
        "h": close + 2,
        "l": close - 2,
        "c": close,
        "v": 1000,
    }


def test_polygon_aggregate_url() -> None:
    assert polygon_aggregate_url("NVDA", 1, "day", "2020-01-01", "2020-01-31") == (
        "https://api.polygon.io/v2/aggs/ticker/NVDA/range/1/day/2020-01-01/2020-01-31"
    )


def test_normalize_polygon_aggregate_bars_deduplicates_and_sorts() -> None:
    bars = [
        _polygon_bar(1_609_545_600_000, 102.0),
        _polygon_bar(1_609_459_200_000, 101.0),
        _polygon_bar(1_609_459_200_000, 101.0),
        {"bad": "row"},
    ]

    df = normalize_polygon_aggregate_bars(bars)

    assert list(df["close"]) == [101.0, 102.0]
    assert list(df.columns) == ["date", "timestamp", "open", "high", "low", "close", "volume"]


def test_ingest_historical_symbol_writes_csv_and_metadata(tmp_path: Path) -> None:
    client = MockHttpClient({"results": [_polygon_bar(1_609_459_200_000, 101.0), _polygon_bar(1_609_545_600_000, 102.0)]})
    metadata_path = tmp_path / "metadata" / "ingestion_status.json"

    result = ingest_historical_symbol(
        symbol="NVDA",
        start_date="2021-01-01",
        end_date="2021-01-02",
        api_key="test-key",
        output_root=tmp_path,
        metadata_path=metadata_path,
        http_client=client,
    )

    assert result.status == "ok"
    assert result.rows_fetched == 2
    assert result.rows_written == 2
    assert Path(result.output_path).exists()

    df = pd.read_csv(result.output_path)
    assert list(df["close"]) == [101.0, 102.0]

    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    assert metadata["symbols"]["NVDA:1:day"]["status"] == "ok"
    assert client.calls[0]["params"]["apiKey"] == "test-key"


def test_ingest_historical_symbol_merges_without_duplicates(tmp_path: Path) -> None:
    metadata_path = tmp_path / "metadata" / "ingestion_status.json"
    first_client = MockHttpClient({"results": [_polygon_bar(1_609_459_200_000, 101.0)]})
    second_client = MockHttpClient({"results": [_polygon_bar(1_609_459_200_000, 101.0), _polygon_bar(1_609_545_600_000, 102.0)]})

    ingest_historical_symbol(
        symbol="NVDA",
        start_date="2021-01-01",
        end_date="2021-01-01",
        api_key="test-key",
        output_root=tmp_path,
        metadata_path=metadata_path,
        http_client=first_client,
    )
    result = ingest_historical_symbol(
        symbol="NVDA",
        start_date="2021-01-01",
        end_date="2021-01-02",
        api_key="test-key",
        output_root=tmp_path,
        metadata_path=metadata_path,
        http_client=second_client,
    )

    df = pd.read_csv(result.output_path)
    assert len(df) == 2
    assert result.rows_written == 2


def test_ingest_historical_symbol_records_empty_response(tmp_path: Path) -> None:
    client = MockHttpClient({"results": []})
    metadata_path = tmp_path / "metadata" / "ingestion_status.json"

    result = ingest_historical_symbol(
        symbol="EMPTY",
        start_date="2021-01-01",
        end_date="2021-01-02",
        api_key="test-key",
        output_root=tmp_path,
        metadata_path=metadata_path,
        http_client=client,
    )

    assert result.status == "empty"
    assert result.rows_fetched == 0
    assert "no usable bars" in result.message
    assert Path(result.output_path).exists()


def test_ingest_historical_symbol_records_missing_api_key(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.delenv("POLYGON_API_KEY", raising=False)
    metadata_path = tmp_path / "metadata" / "ingestion_status.json"

    result = ingest_historical_symbol(
        symbol="NVDA",
        start_date="2021-01-01",
        end_date="2021-01-02",
        output_root=tmp_path,
        metadata_path=metadata_path,
    )

    assert result.status == "error"
    assert result.message == "missing POLYGON_API_KEY"
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    assert metadata["symbols"]["NVDA:1:day"]["status"] == "error"


def test_ingest_historical_symbols_batch_counts_results(tmp_path: Path) -> None:
    client = MockHttpClient({"results": [_polygon_bar(1_609_459_200_000, 101.0)]})

    batch = ingest_historical_symbols(
        symbols=["NVDA", "AAPL"],
        start_date="2021-01-01",
        end_date="2021-01-02",
        api_key="test-key",
        output_root=tmp_path,
        metadata_path=tmp_path / "metadata.json",
        http_client=client,
    )

    assert batch.success_count == 2
    assert batch.warning_count == 0
    assert len(batch.to_dict()["results"]) == 2
