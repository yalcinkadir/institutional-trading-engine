from __future__ import annotations

from src.reporting import market_regime as mr


def _bars(days: int = 260, *, close: float = 500.0) -> list[dict]:
    return [
        {
            "o": close + idx,
            "h": close + idx + 1,
            "l": close + idx - 1,
            "c": close + idx,
            "v": 1_000_000 + idx,
        }
        for idx in range(days)
    ]


class _FakePolygonClient:
    def get_daily_bars(self, ticker: str, days: int = 250) -> list[dict]:
        if ticker == mr.VIX_TICKER:
            raise RuntimeError("entitlement unavailable for VIX index ticker")
        return _bars(days=max(days, 260), close=500.0 if ticker == "SPY" else 450.0)


def test_vix_entitlement_error_marks_regime_unvalidated(monkeypatch) -> None:
    monkeypatch.setattr(mr, "PolygonClient", _FakePolygonClient)

    summary = mr.build_market_regime_summary("premarket")

    assert summary["regime"] == mr.UNVALIDATED_REGIME
    assert summary["regime_validation_status"] == mr.REGIME_STATUS_UNVALIDATED
    assert summary["data_status"] == "PARTIAL"
    assert summary["market_health_score"] != "DATA_UNAVAILABLE"

    vix_input = summary["regime_input"]["vix"]
    assert vix_input["source"] == "polygon"
    assert vix_input["status"] == mr.REGIME_STATUS_UNVALIDATED
    assert vix_input["validation_status"] == mr.REGIME_STATUS_UNVALIDATED
    assert vix_input["reason"] == mr.VIX_UNAVAILABLE_ENTITLEMENT
    assert vix_input["fallback_used"] is True
    assert vix_input["live_or_paper_confidence_authorized"] is False

    assert "SPY" in summary["symbols"]
    assert "QQQ" in summary["symbols"]
    assert "VIX" not in summary["symbols"]
    assert any(mr.VIX_UNAVAILABLE_ENTITLEMENT in error for error in summary["errors"])
    assert any("UNVALIDATED" in note for note in summary["notes"])


def test_vix_entitlement_error_is_not_plain_unknown(monkeypatch) -> None:
    monkeypatch.setattr(mr, "PolygonClient", _FakePolygonClient)

    summary = mr.build_market_regime_summary("postmarket")

    assert summary["regime"] != "Unknown"
    assert summary["regime"] == mr.UNVALIDATED_REGIME
    assert summary["regime_input"]["vix"]["reason"] == mr.VIX_UNAVAILABLE_ENTITLEMENT
