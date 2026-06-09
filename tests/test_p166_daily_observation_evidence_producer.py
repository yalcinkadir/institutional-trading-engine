from __future__ import annotations

import json
from pathlib import Path

import scripts.produce_daily_observation_evidence_p166 as producer


def _regime(validation_status: str = "DEGRADED", data_status: str = "PARTIAL") -> dict:
    return {
        "timestamp_utc": "2026-06-09T00:00:00+00:00",
        "market_health_score": 72,
        "regime": "Neutral Bullish (VIX proxy degraded)",
        "regime_validation_status": validation_status,
        "data_status": data_status,
        "errors": [],
        "regime_input": {
            "vix": {
                "symbol": "I:VIX",
                "source": "polygon_proxy",
                "proxy_symbol": "VIXY",
                "status": "PROXY_DEGRADED",
                "validation_status": validation_status,
                "reason": "VIX_PROXY_FALLBACK",
                "fallback_used": True,
                "live_or_paper_confidence_authorized": False,
            },
            "index_trend": {"status": "LIVE", "symbols": ["SPY", "QQQ"]},
        },
        "symbols": {},
        "breadth": {},
        "notes": [],
    }


def test_p166_producer_builds_schema_valid_daily_evidence_with_vix_proxy(monkeypatch) -> None:
    monkeypatch.setattr(producer, "build_market_regime_summary", lambda _report_type: _regime())

    record = producer.build_daily_evidence(
        observation_date="2026-06-09",
        selected_symbols=["MSFT", "NVDA"],
        created_at="2026-06-09T00:00:00+00:00",
    )

    assert record["date"] == "2026-06-09"
    assert record["status"] == "NEEDS_REVIEW"
    assert record["run_health_status"] == "DEGRADED"
    assert record["data_quality_status"] == "PARTIAL"
    assert record["selection_mode"] == "configured_watchlist"
    assert record["selected_symbols"] == ["MSFT", "NVDA"]
    assert record["paper_only_safety_boundary"]["live_trading_authorized"] is False
    assert record["paper_only_safety_boundary"]["broker_execution_mode"] == "paper_only"
    assert record["demo_or_synthetic"] is False
    assert record["productive_evidence"] is False

    vix_input = record["source_provenance"]["vix_input"]
    assert vix_input["source"] == "polygon_proxy"
    assert vix_input["proxy_symbol"] == "VIXY"
    assert vix_input["reason"] == "VIX_PROXY_FALLBACK"
    assert vix_input["live_or_paper_confidence_authorized"] is False


def test_p166_producer_blocks_when_regime_unvalidated(monkeypatch) -> None:
    monkeypatch.setattr(producer, "build_market_regime_summary", lambda _report_type: _regime("UNVALIDATED", "FALLBACK"))

    record = producer.build_daily_evidence(
        observation_date="2026-06-09",
        selected_symbols=["MSFT"],
        created_at="2026-06-09T00:00:00+00:00",
    )

    assert record["status"] == "REJECTED"
    assert record["signal_generation_status"] == "BLOCKED_DATA_QUALITY"
    assert "regime_validation_status:UNVALIDATED" in record["missing_evidence"]
    assert record["productive_evidence"] is False


def test_p166_producer_writes_canonical_daily_evidence(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setattr(producer, "build_market_regime_summary", lambda _report_type: _regime("LIVE", "LIVE"))

    record = producer.build_daily_evidence(
        observation_date="2026-06-09",
        selected_symbols=["MSFT"],
        created_at="2026-06-09T00:00:00+00:00",
    )
    path = producer.write_daily_evidence(record, output_root=tmp_path)

    assert path == tmp_path / "2026-06-09.json"
    written = json.loads(path.read_text(encoding="utf-8"))
    assert written["status"] == "ACCEPTED"
    assert written["productive_evidence"] is True
    assert written["market_regime"]["regime_validation_status"] == "LIVE"
