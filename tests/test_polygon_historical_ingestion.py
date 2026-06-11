from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from scripts.validate_bt9_real_historical_input_pack import validate_bt9_input_pack
from src.historical.polygon_ingestion import (
    HistoricalIngestionResult,
    build_coverage_manifest,
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


def test_ingest_historical_symbol_writes_csv_metadata_and_sha256(tmp_path: Path) -> None:
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
    assert len(result.output_sha256) == 64

    df = pd.read_csv(result.output_path)
    assert list(df["close"]) == [101.0, 102.0]

    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    assert metadata["symbols"]["NVDA:1:day"]["status"] == "ok"
    assert metadata["symbols"]["NVDA:1:day"]["output_sha256"] == result.output_sha256
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
    assert len(result.output_sha256) == 64


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
    assert result.output_sha256 == ""
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
    assert result.output_sha256 == ""
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
        coverage_manifest_path=tmp_path / "coverage_manifest.json",
        http_client=client,
    )

    assert batch.success_count == 2
    assert batch.warning_count == 0
    assert len(batch.to_dict()["results"]) == 2
    assert all(len(item["output_sha256"]) == 64 for item in batch.to_dict()["results"])
    assert batch.coverage_manifest_path == str(tmp_path / "coverage_manifest.json")


def test_historical_coverage_manifest_contains_vendor_timestamp_and_missing_summary(tmp_path: Path) -> None:
    client = MockHttpClient({"results": [_polygon_bar(1_609_459_200_000, 101.0)]})
    manifest_path = tmp_path / "metadata" / "coverage_manifest.json"

    ingest_historical_symbols(
        symbols=["NVDA", "AAPL"],
        start_date="2021-01-01",
        end_date="2021-01-02",
        api_key="test-key",
        output_root=tmp_path,
        metadata_path=tmp_path / "metadata" / "ingestion_status.json",
        coverage_manifest_path=manifest_path,
        http_client=client,
    )

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest["vendor"] == "polygon"
    assert manifest["generated_at"]
    assert manifest["requested_start_date"] == "2021-01-01"
    assert manifest["requested_end_date"] == "2021-01-02"
    assert manifest["symbol_count"] == 2
    assert manifest["ok_symbol_count"] == 2
    assert manifest["status"] == "ok"
    assert {item["symbol"] for item in manifest["symbols"]} == {"NVDA", "AAPL"}
    assert all(item["bar_count"] == 1 for item in manifest["symbols"])
    assert all(len(item["output_sha256"]) == 64 for item in manifest["symbols"])


def test_historical_coverage_manifest_marks_partial_payload_as_degraded() -> None:
    ok = HistoricalIngestionResult(
        symbol="NVDA",
        timespan="day",
        multiplier=1,
        start_date="2021-01-01",
        end_date="2021-01-02",
        rows_fetched=1,
        rows_written=1,
        output_path="data/historical/bars/1day/NVDA.csv",
        status="ok",
        output_sha256="a" * 64,
    )
    empty = HistoricalIngestionResult(
        symbol="MSFT",
        timespan="day",
        multiplier=1,
        start_date="2021-01-01",
        end_date="2021-01-02",
        rows_fetched=0,
        rows_written=0,
        output_path="data/historical/bars/1day/MSFT.csv",
        status="empty",
        message="Polygon returned no usable bars",
    )

    manifest = build_coverage_manifest([ok, empty]).to_dict()
    assert manifest["status"] == "degraded"
    assert "MSFT:empty" in manifest["missing_data_summary"]
    assert "MSFT:no_canonical_bars_written" in manifest["missing_data_summary"]


def test_hist1_output_is_compatible_with_bt9_input_pack(tmp_path: Path) -> None:
    client = MockHttpClient({"results": [_polygon_bar(1_609_459_200_000, 101.0), _polygon_bar(1_609_545_600_000, 102.0)]})
    coverage_manifest = tmp_path / "historical" / "metadata" / "coverage_manifest.json"
    ingest_historical_symbols(
        symbols=["SPY"],
        start_date="2021-01-01",
        end_date="2021-01-02",
        api_key="test-key",
        output_root=tmp_path / "historical",
        metadata_path=tmp_path / "historical" / "metadata" / "ingestion_status.json",
        coverage_manifest_path=coverage_manifest,
        http_client=client,
    )
    universe = tmp_path / "survivorship_universe.csv"
    universe.write_text(
        "symbol,effective_from,effective_to,active,asset_class,exchange,source,status,reason\n"
        "SPY,2020-01-01,,true,etf,NYSEARCA,initial_universe,active,initial test universe\n",
        encoding="utf-8",
    )
    plans = tmp_path / "historical_trade_plans.json"
    plans.write_text(
        json.dumps(
            {
                "plans": [
                    {
                        "signal_id": "sig_spy_1",
                        "symbol": "SPY",
                        "signal_date": "2021-01-01",
                        "entry_trigger": 101.0,
                        "stop_loss": 99.0,
                        "target_1": 105.0,
                    }
                ]
            }
        ),
        encoding="utf-8",
    )

    report = validate_bt9_input_pack(
        universe_path=universe,
        bars_root=tmp_path / "historical" / "bars" / "1day",
        trade_plans_path=plans,
        coverage_manifest_path=coverage_manifest,
    )

    assert report.passed
    assert report.symbols == ["SPY"]
    assert report.input_checksums
