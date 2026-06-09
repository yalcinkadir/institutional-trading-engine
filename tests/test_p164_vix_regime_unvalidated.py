from __future__ import annotations

from src.reporting import market_regime as mr


def _bars(days: int = 260, *, close: float = 500.0, step: float = 1.0) -> list[dict]:
    return [
        {
            "o": close + (idx * step),
            "h": close + (idx * step) + 1,
            "l": close + (idx * step) - 1,
            "c": close + (idx * step),
            "v": 1_000_000 + idx,
        }
        for idx in range(days)
    ]


class _ProxyCapablePolygonClient:
    def get_daily_bars(self, ticker: str, days: int = 250) -> list[dict]:
        if ticker == mr.VIX_TICKER:
            raise RuntimeError("entitlement unavailable for VIX index ticker")
        if ticker == mr.DEFAULT_VOLATILITY_PROXY_SYMBOL:
            return _bars(days=max(days, 260), close=18.0, step=0.05)
        return _bars(days=max(days, 260), close=500.0 if ticker == "SPY" else 450.0)


class _NoProxyPolygonClient:
    def get_daily_bars(self, ticker: str, days: int = 250) -> list[dict]:
        if ticker == mr.VIX_TICKER:
            raise RuntimeError("entitlement unavailable for VIX index ticker")
        if ticker == mr.DEFAULT_VOLATILITY_PROXY_SYMBOL:
            raise RuntimeError("proxy unavailable")
        return _bars(days=max(days, 260), close=500.0 if ticker == "SPY" else 450.0)


def test_vix_entitlement_error_uses_proxy_when_available(monkeypatch) -> None:
    monkeypatch.setattr(mr, "PolygonClient", _ProxyCapablePolygonClient)

    summary = mr.build_market_regime_summary("premarket")

    assert summary["regime"] != "Unknown"
    assert summary["regime"] != mr.UNVALIDATED_REGIME
    assert summary["regime_validation_status"] == mr.REGIME_STATUS_DEGRADED
    assert summary["data_status"] == "PARTIAL"
    assert summary["market_health_score"] != "DATA_UNAVAILABLE"

    vix_input = summary["regime_input"]["vix"]
    assert vix_input["source"] == "polygon_proxy"
    assert vix_input["proxy_symbol"] == mr.DEFAULT_VOLATILITY_PROXY_SYMBOL
    assert vix_input["status"] == mr.REGIME_STATUS_PROXY_DEGRADED
    assert vix_input["validation_status"] == mr.REGIME_STATUS_DEGRADED
    assert vix_input["reason"] == mr.VIX_PROXY_FALLBACK
    assert vix_input["fallback_used"] is True
    assert vix_input["live_or_paper_confidence_authorized"] is False

    assert "SPY" in summary["symbols"]
    assert "QQQ" in summary["symbols"]
    assert "VIX" not in summary["symbols"]
    assert "VIX_PROXY" in summary["symbols"]
    assert any(mr.VIX_UNAVAILABLE_ENTITLEMENT in error for error in summary["errors"])
    assert any("proxy" in note.lower() for note in summary["notes"])


def test_vix_entitlement_error_without_proxy_remains_unvalidated(monkeypatch) -> None:
    monkeypatch.setattr(mr, "PolygonClient", _NoProxyPolygonClient)

    summary = mr.build_market_regime_summary("postmarket")

    assert summary["regime"] == mr.UNVALIDATED_REGIME
    assert summary["regime_validation_status"] == mr.REGIME_STATUS_UNVALIDATED
    assert summary["regime_input"]["vix"]["reason"] == mr.VIX_UNAVAILABLE_ENTITLEMENT
    assert "VIX_PROXY" not in summary["symbols"]
    assert any("UNVALIDATED" in note for note in summary["notes"])
