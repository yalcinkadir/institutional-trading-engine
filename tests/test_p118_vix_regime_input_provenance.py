from __future__ import annotations

from dataclasses import dataclass

import pytest


@dataclass
class _FakePolygonClient:
    unavailable_tickers: set[str]

    def get_daily_bars(self, ticker: str, days: int = 260) -> list[dict]:
        if ticker in self.unavailable_tickers:
            raise RuntimeError(f"unsupported tier for {ticker}")

        if ticker == "I:VIX":
            closes = [16.0 for _ in range(days)]
        else:
            closes = [100.0 + i * 0.2 for i in range(days)]

        return [
            {"c": close, "h": close + 1.0, "l": close - 1.0, "v": 1_000_000}
            for close in closes
        ]


def test_p118_vix_input_provenance_is_recorded_for_live_vix(monkeypatch: pytest.MonkeyPatch) -> None:
    from src.reporting import market_regime

    monkeypatch.setattr(market_regime, "PolygonClient", lambda: _FakePolygonClient(unavailable_tickers=set()))

    summary = market_regime.build_market_regime_summary("premarket")

    regime_input = summary["regime_input"]
    assert regime_input["vix"]["symbol"] == "I:VIX"
    assert regime_input["vix"]["source"] == "polygon"
    assert regime_input["vix"]["status"] == "LIVE"
    assert regime_input["vix"]["fallback_used"] is False
    assert regime_input["vix"]["timestamp"] == summary["timestamp_utc"]
    assert summary["regime_policy"]["action"] == "ALLOW"
    assert summary["regime_policy"]["confidence"] == "FULL"
    assert summary["data_status"] == "LIVE"
    assert "VIX" in summary["symbols"]


def test_p118_unavailable_vix_is_deterministic_blocked_input(monkeypatch: pytest.MonkeyPatch) -> None:
    from src.reporting import market_regime

    monkeypatch.setattr(market_regime, "PolygonClient", lambda: _FakePolygonClient(unavailable_tickers={"I:VIX"}))

    summary = market_regime.build_market_regime_summary("premarket")

    regime_input = summary["regime_input"]
    assert regime_input["vix"]["symbol"] == "I:VIX"
    assert regime_input["vix"]["source"] == "polygon"
    assert regime_input["vix"]["status"] == "BLOCKED"
    assert regime_input["vix"]["fallback_used"] is True
    assert regime_input["vix"]["fallback_value"] is None
    assert "unsupported tier for I:VIX" in regime_input["vix"]["error"]
    assert summary["data_status"] == "PARTIAL"
    assert summary["regime"] == market_regime.BLOCKED_MARKET_REGIME_UNAVAILABLE
    assert summary["regime"] != "Unknown"
    assert summary["regime_policy"]["action"] == "BLOCK"
    assert summary["regime_policy"]["confidence"] == "BLOCKED"
    assert any("blocked" in note.lower() for note in summary["notes"])


def test_p118_missing_core_indices_blocks_regime_input(monkeypatch: pytest.MonkeyPatch) -> None:
    from src.reporting import market_regime

    monkeypatch.setattr(
        market_regime,
        "PolygonClient",
        lambda: _FakePolygonClient(unavailable_tickers={"SPY", "QQQ", "I:VIX"}),
    )

    summary = market_regime.build_market_regime_summary("premarket")

    assert summary["regime"] == market_regime.BLOCKED_MARKET_REGIME_UNAVAILABLE
    assert summary["regime"] != "Unknown"
    assert summary["data_status"] == "FALLBACK"
    assert summary["regime_input"]["vix"]["status"] == "BLOCKED"
    assert summary["regime_input"]["index_trend"]["status"] == "BLOCKED"
    assert summary["regime_policy"]["action"] == "BLOCK"
    assert summary["regime_policy"]["confidence"] == "BLOCKED"
