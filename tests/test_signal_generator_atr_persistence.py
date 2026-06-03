from __future__ import annotations

import json

from src.signals.signal_generator import build_signals, save_signals


def _decision_report() -> dict:
    return {
        "decisions": [
            {
                "symbol": "NVDA",
                "decision": "approved",
                "setup_type": "momentum_breakout",
                "risk_tier": "tier_2",
                "position_size_multiplier": 0.5,
                "setup_score": 82.0,
                "regime_alignment": 0.8,
            }
        ]
    }


def _scanner_metrics() -> dict:
    return {
        "NVDA": {
            "close": 100.0,
            "high": 101.0,
            "atr14": 4.0,
            "atr_pct": 0.0,
            "rvol": 1.2,
            "vwap": 99.0,
            "source": "polygon",
            "source_timestamp": "2026-06-03T14:30:00+00:00",
            "fallback_level": "primary",
            "data_status": "OK",
        }
    }


def test_build_signals_persists_atr14_for_watcher_trailing_stop_path() -> None:
    signals = build_signals(_decision_report(), _scanner_metrics(), market_regime="Bullish")

    assert len(signals) == 1
    signal = signals[0]
    assert signal.action == "BUY_WATCH"
    assert signal.atr14 == 4.0
    assert signal.atr_pct == 0.0
    assert signal.source == "polygon"
    assert signal.source_timestamp == "2026-06-03T14:30:00+00:00"
    assert signal.fallback_level == "primary"
    assert signal.data_status == "OK"


def test_save_signals_writes_atr14_to_json_and_markdown(tmp_path) -> None:
    signals = build_signals(_decision_report(), _scanner_metrics(), market_regime="Bullish")

    json_path, md_path = save_signals(signals, date_str="2026-05-31", signals_dir=tmp_path)

    payload = json.loads(json_path.read_text(encoding="utf-8"))
    persisted_signal = payload["signals"][0]
    assert persisted_signal["atr14"] == 4.0
    assert persisted_signal["atr_pct"] == 0.0
    assert persisted_signal["source"] == "polygon"
    assert persisted_signal["source_timestamp"] == "2026-06-03T14:30:00+00:00"
    assert persisted_signal["fallback_level"] == "primary"
    assert persisted_signal["data_status"] == "OK"

    latest_payload = json.loads((tmp_path / "latest-signals.json").read_text(encoding="utf-8"))
    assert latest_payload["signals"][0]["atr14"] == 4.0

    markdown = md_path.read_text(encoding="utf-8")
    assert "ATR14: 4.00" in markdown
    assert "ATR%: 0.00%" in markdown
    assert "Source: polygon" in markdown
