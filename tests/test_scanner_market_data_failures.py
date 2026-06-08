from __future__ import annotations

import requests

from src.market_data_failures import MarketDataFailureKind
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


def test_daily_bars_classifies_polygon_403_as_auth_forbidden(monkeypatch) -> None:
    _configure_api_key(monkeypatch)
    monkeypatch.setattr(scanner.requests, "get", lambda *args, **kwargs: _Response(403))

    assert scanner.get_daily_bars("I:VIX", retries=1) is None

    failure = scanner.get_market_data_failure("I:VIX")
    assert failure is not None
    assert failure.kind == MarketDataFailureKind.AUTH_FORBIDDEN
    assert failure.status_code == 403


def test_daily_bars_classifies_empty_results_separately(monkeypatch) -> None:
    _configure_api_key(monkeypatch)
    monkeypatch.setattr(scanner.requests, "get", lambda *args, **kwargs: _Response(200, {"results": []}))

    assert scanner.get_daily_bars("SPY", retries=1) is None

    failure = scanner.get_market_data_failure("SPY")
    assert failure is not None
    assert failure.kind == MarketDataFailureKind.EMPTY_BARS
    assert failure.status_code == 200


def test_daily_bars_classifies_rate_limit(monkeypatch) -> None:
    _configure_api_key(monkeypatch)
    monkeypatch.setattr(scanner.time, "sleep", lambda *_args, **_kwargs: None)
    monkeypatch.setattr(scanner.requests, "get", lambda *args, **kwargs: _Response(429))

    assert scanner.get_daily_bars("QQQ", retries=1) is None

    failure = scanner.get_market_data_failure("QQQ")
    assert failure is not None
    assert failure.kind == MarketDataFailureKind.RATE_LIMIT
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
