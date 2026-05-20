from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

from src.data.polygon_client import PolygonClient


def test_get_daily_bars_range_uses_expected_endpoint_and_params(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("POLYGON_CACHE_DIR", str(tmp_path))
    client = PolygonClient(api_key="test-key")

    with patch.object(
        client,
        "_request_with_retry",
        return_value={"results": [{"t": 1704067200000, "c": 100.0, "h": 101.0, "l": 99.0}]},
    ) as request:
        bars = client.get_daily_bars_range(
            "AAPL",
            "2024-01-01",
            "2024-01-31",
            limit=123,
            adjusted=True,
            use_ttl_cache=False,
        )

    assert bars == [{"t": 1704067200000, "c": 100.0, "h": 101.0, "l": 99.0}]
    url = request.call_args.args[0]
    params = request.call_args.kwargs["params"]

    assert url.endswith("/v2/aggs/ticker/AAPL/range/1/day/2024-01-01/2024-01-31")
    assert params["adjusted"] == "true"
    assert params["sort"] == "asc"
    assert params["limit"] == 123
    assert params["apiKey"] == "test-key"


def test_get_daily_bars_range_reads_cache_when_available(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr("src.data.polygon_client.CACHE_DIR", tmp_path)
    client = PolygonClient(api_key="test-key")
    cache_file = client._range_cache_key(
        "AAPL",
        "2024-01-01",
        "2024-01-31",
        adjusted=True,
        limit=50000,
    )
    cache_file.parent.mkdir(parents=True, exist_ok=True)
    cache_file.write_text('[{"t": 1, "c": 100.0}]', encoding="utf-8")

    with patch.object(client, "_request_with_retry") as request:
        bars = client.get_daily_bars_range("AAPL", "2024-01-01", "2024-01-31")

    assert bars == [{"t": 1, "c": 100.0}]
    request.assert_not_called()
