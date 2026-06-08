from __future__ import annotations

import pandas as pd
import requests

from src.signals.scanner_metrics_pipeline import normalize_scanner_metrics_map
import src.scanner as scanner


class _Response:
    def __init__(self, status_code: int, payload: dict | None = None) -> None:
        self.status_code = status_code
        self._payload = payload or {}

    def json(self) -> dict:
        return self._payload

    def raise_for_status(self) -> None:
        if self.status_code >= 400:
            raise requests.HTTPError(f"{self.status_code} error")


def _configure_api_key(monkeypatch) -> None:
    monkeypatch.setattr(scanner, "API_KEY", "test-key")
    scanner.clear_market_data_failures()


def _bars(closes: list[float]) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "date": pd.date_range("2026-01-01", periods=len(closes)).date,
            "open": closes,
            "high": [value + 1 for value in closes],
            "low": [value - 1 for value in closes],
            "close": closes,
            "volume": [1000] * len(closes),
        }
    )


def test_daily_bars_classifies_polygon_403_as_auth_forbidden(monkeypatch) -> None:
    _configure_api_key(monkeypatch)
    monkeypatch.setattr(scanner.requests, "get", lambda *args, **kwargs: _Response(403))

    assert scanner.get_daily_bars("I:VIX", retries=1) is None

    failure = scanner.get_market_data_failure("I:VIX")
    assert failure is not None
    assert failure.kind == scanner.MarketDataFailureKind.AUTH_FORBIDDEN
    assert failure.status_code == 403


def test_daily_bars_classifies_empty_results_separately(monkeypatch) -> None:
    _configure_api_key(monkeypatch)
    monkeypatch.setattr(scanner.requests, "get", lambda *args, **kwargs: _Response(200, {"results": []}))

    assert scanner.get_daily_bars("SPY", retries=1) is None

    failure = scanner.get_market_data_failure("SPY")
    assert failure is not None
    assert failure.kind == scanner.MarketDataFailureKind.EMPTY_BARS
    assert failure.status_code == 200


def test_daily_bars_classifies_rate_limit(monkeypatch) -> None:
    _configure_api_key(monkeypatch)
    monkeypatch.setattr(scanner.time, "sleep", lambda *_args, **_kwargs: None)
    monkeypatch.setattr(scanner.requests, "get", lambda *args, **kwargs: _Response(429))

    assert scanner.get_daily_bars("QQQ", retries=1) is None

    failure = scanner.get_market_data_failure("QQQ")
    assert failure is not None
    assert failure.kind == scanner.MarketDataFailureKind.RATE_LIMIT
    assert failure.status_code == 429


def test_failure_stub_reaches_scanner_diagnostics(monkeypatch) -> None:
    _configure_api_key(monkeypatch)
    monkeypatch.setattr(scanner.requests, "get", lambda *args, **kwargs: _Response(403))

    metrics = scanner.build_symbol_metrics("SPY", {})
    normalized, diagnostics = normalize_scanner_metrics_map({"SPY": metrics}, ["SPY"])

    assert normalized["SPY"]["close"] is None
    assert normalized["SPY"]["atr14"] is None
    assert diagnostics.data_quality_status == "BLOCKED"
    assert diagnostics.market_data_failures["SPY"]["kind"] == "AUTH_FORBIDDEN"
    assert "market_data_failure:SPY:AUTH_FORBIDDEN" in "\n".join(diagnostics.warning_lines())


def test_vix_defaults_to_supported_proxy_with_degraded_provenance(monkeypatch) -> None:
    _configure_api_key(monkeypatch)
    monkeypatch.delenv("POLYGON_INDEX_DATA_ENABLED", raising=False)
    monkeypatch.setenv("VOLATILITY_PROXY_SYMBOL", "VIXY")
    calls: list[str] = []

    def fake_get_daily_bars(symbol: str, days: int = 500, retries: int = 3):
        calls.append(symbol)
        assert symbol == "VIXY"
        return _bars([10.0, 11.0])

    monkeypatch.setattr(scanner, "get_daily_bars", fake_get_daily_bars)

    vix = scanner.get_vix_value(retries=1)

    assert calls == ["VIXY"]
    assert vix["close"] == 11.0
    assert vix["direction"] == "Rising"
    assert vix["source"] == "polygon"
    assert vix["source_symbol"] == "VIXY"
    assert vix["proxy_for"] == "I:VIX"
    assert vix["fallback_level"] == "proxy"
    assert vix["data_status"] == "DEGRADED"
    assert vix["data_failure_kind"] == "AUTH_FORBIDDEN"


def test_vix_primary_index_path_when_explicitly_enabled(monkeypatch) -> None:
    _configure_api_key(monkeypatch)
    monkeypatch.setenv("POLYGON_INDEX_DATA_ENABLED", "true")
    calls: list[str] = []

    def fake_get_daily_bars(symbol: str, days: int = 500, retries: int = 3):
        calls.append(symbol)
        assert symbol == "I:VIX"
        return _bars([18.0, 17.0])

    monkeypatch.setattr(scanner, "get_daily_bars", fake_get_daily_bars)

    vix = scanner.get_vix_value(retries=1)

    assert calls == ["I:VIX"]
    assert vix["close"] == 17.0
    assert vix["direction"] == "Falling"
    assert vix["source_symbol"] == "I:VIX"
    assert vix["fallback_level"] == "primary"
    assert vix["data_status"] == "OK"
    assert "data_failure_kind" not in vix


def test_vix_proxy_failure_blocks_regime_context(monkeypatch) -> None:
    _configure_api_key(monkeypatch)
    monkeypatch.delenv("POLYGON_INDEX_DATA_ENABLED", raising=False)

    def fake_get_daily_bars(symbol: str, days: int = 500, retries: int = 3):
        scanner._record_market_data_failure(
            scanner.MarketDataFailure(
                symbol=symbol,
                kind=scanner.MarketDataFailureKind.EMPTY_BARS,
                message="proxy returned no bars",
                status_code=200,
            )
        )
        return None

    monkeypatch.setattr(scanner, "get_daily_bars", fake_get_daily_bars)

    vix = scanner.get_vix_value(retries=1)

    assert pd.isna(vix["close"])
    assert vix["direction"] == "Unavailable"
    assert vix["source_symbol"] == "VIXY"
    assert vix["fallback_level"] == "none"
    assert vix["data_status"] == "BLOCKED"
    assert vix["data_failure_kind"] == "EMPTY_BARS"


def test_market_regime_report_stamps_proxy_health_and_source() -> None:
    metrics_map = {
        "SPY": {"trend": "Uptrend", "rsi14": 60, "atr_pct": 1.0},
        "QQQ": {"trend": "Uptrend", "rsi14": 58, "atr_pct": 1.1},
    }
    vix_data = {
        "close": 11.0,
        "direction": "Rising",
        "source": "polygon",
        "source_symbol": "VIXY",
        "fallback_level": "proxy",
        "data_status": "DEGRADED",
        "proxy_for": "I:VIX",
        "data_failure_kind": "AUTH_FORBIDDEN",
    }

    lines = scanner.build_market_regime_summary(metrics_map, vix_data)
    report = "\n".join(lines)

    assert "- Risk State: Cautious" in report
    assert "- VIX: 11.00 (Rising) proxy_for=I:VIX" in report
    assert "- Volatility Data Health: DEGRADED" in report
    assert "- VIX Source: polygon:VIXY (proxy)" in report
    assert "primary volatility source failed with AUTH_FORBIDDEN" in report
