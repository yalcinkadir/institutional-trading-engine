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


class _VixAvailableClient:
    def get_daily_bars(self, ticker: str, days: int = 250) -> list[dict]:
        if ticker == mr.VIX_TICKER:
            return _bars(days=max(days, 260), close=16.0, step=0.01)
        return _bars(days=max(days, 260), close=500.0 if ticker == "SPY" else 450.0)


class _VixMissingProxyAvailableClient:
    def get_daily_bars(self, ticker: str, days: int = 250) -> list[dict]:
        if ticker == mr.VIX_TICKER:
            raise RuntimeError("403 forbidden entitlement unavailable for VIX index ticker")
        if ticker == mr.DEFAULT_VOLATILITY_PROXY_SYMBOL:
            return _bars(days=max(days, 260), close=18.0, step=0.05)
        return _bars(days=max(days, 260), close=500.0 if ticker == "SPY" else 450.0)


class _VixAndProxyMissingClient:
    def get_daily_bars(self, ticker: str, days: int = 250) -> list[dict]:
        if ticker == mr.VIX_TICKER:
            raise RuntimeError("403 forbidden entitlement unavailable for VIX index ticker")
        if ticker == mr.DEFAULT_VOLATILITY_PROXY_SYMBOL:
            raise RuntimeError("proxy unavailable")
        return _bars(days=max(days, 260), close=500.0 if ticker == "SPY" else 450.0)


class _NoIndexDataClient:
    def get_daily_bars(self, ticker: str, days: int = 250) -> list[dict]:
        raise RuntimeError(f"{ticker} unavailable")


class _BrokenClient:
    def __init__(self) -> None:
        raise RuntimeError("api key missing")


def _assert_policy_payload(summary: dict) -> None:
    policy = summary["regime_policy"]
    assert policy["source"]
    assert "fallback_used" in policy
    assert policy["confidence"] in {"FULL", "DEGRADED", "BLOCKED"}
    assert policy["status"] in {"LIVE", "DEGRADED", "BLOCKED"}
    assert policy["action"] in {"ALLOW", "DEGRADE", "BLOCK"}


def test_187_vix_available_policy_is_live_and_explained(monkeypatch) -> None:
    monkeypatch.setattr(mr, "PolygonClient", _VixAvailableClient)

    summary = mr.build_market_regime_summary("premarket")

    assert summary["regime"] != "Unknown"
    assert summary["regime_validation_status"] == mr.REGIME_STATUS_LIVE
    assert summary["regime_policy"]["status"] == "LIVE"
    assert summary["regime_policy"]["source"] == "polygon"
    assert summary["regime_policy"]["fallback_used"] is False
    assert summary["regime_policy"]["confidence"] == "FULL"
    assert summary["regime_policy"]["action"] == "ALLOW"
    _assert_policy_payload(summary)


def test_187_vix_missing_proxy_available_policy_is_degraded(monkeypatch) -> None:
    monkeypatch.setattr(mr, "PolygonClient", _VixMissingProxyAvailableClient)

    summary = mr.build_market_regime_summary("premarket")

    assert summary["regime"] != "Unknown"
    assert summary["regime_validation_status"] == mr.REGIME_STATUS_DEGRADED
    assert summary["regime_policy"]["status"] == "DEGRADED"
    assert summary["regime_policy"]["source"] == "polygon_proxy"
    assert summary["regime_policy"]["fallback_used"] is True
    assert summary["regime_policy"]["confidence"] == "DEGRADED"
    assert summary["regime_policy"]["action"] == "DEGRADE"
    assert summary["regime_policy"]["reason"] == mr.VIX_PROXY_FALLBACK
    _assert_policy_payload(summary)


def test_187_vix_missing_without_proxy_blocks_regime_policy(monkeypatch) -> None:
    monkeypatch.setattr(mr, "PolygonClient", _VixAndProxyMissingClient)

    summary = mr.build_market_regime_summary("postmarket")

    assert summary["regime"] == mr.BLOCKED_MARKET_REGIME_UNAVAILABLE
    assert summary["regime_validation_status"] == mr.REGIME_STATUS_BLOCKED
    assert summary["regime_policy"]["status"] == "BLOCKED"
    assert summary["regime_policy"]["source"] == "polygon"
    assert summary["regime_policy"]["fallback_used"] is True
    assert summary["regime_policy"]["confidence"] == "BLOCKED"
    assert summary["regime_policy"]["action"] == "BLOCK"
    assert summary["regime_policy"]["reason"] == mr.VIX_UNAVAILABLE_ENTITLEMENT
    _assert_policy_payload(summary)


def test_187_index_data_missing_does_not_emit_unknown_regime(monkeypatch) -> None:
    monkeypatch.setattr(mr, "PolygonClient", _NoIndexDataClient)

    summary = mr.build_market_regime_summary("premarket")

    assert summary["regime"] == mr.BLOCKED_MARKET_REGIME_UNAVAILABLE
    assert summary["regime"] != "Unknown"
    assert summary["regime_policy"]["status"] == "BLOCKED"
    assert summary["regime_policy"]["action"] == "BLOCK"
    _assert_policy_payload(summary)


def test_187_polygon_client_failure_does_not_emit_unknown_regime(monkeypatch) -> None:
    monkeypatch.setattr(mr, "PolygonClient", _BrokenClient)

    summary = mr.build_market_regime_summary("postmarket")

    assert summary["regime"] == mr.BLOCKED_MARKET_REGIME_UNAVAILABLE
    assert summary["regime"] != "Unknown"
    assert summary["regime_policy"]["status"] == "BLOCKED"
    assert summary["regime_policy"]["action"] == "BLOCK"
    assert summary["regime_policy"]["confidence"] == "BLOCKED"
    _assert_policy_payload(summary)
