from __future__ import annotations

import json
from pathlib import Path

import pytest

from src.signals.signal_generator import Signal, build_signals, save_signals


def _decision_report() -> dict:
    return {
        "decisions": [
            {
                "symbol": "NVDA",
                "decision": "approved",
                "setup_type": "momentum_breakout",
                "risk_tier": "tier_1",
                "position_size_multiplier": 1.0,
                "setup_score": 91.0,
                "regime_alignment": 0.8,
                "blocked_reasons": [],
                "notes": [],
            }
        ]
    }


def _valid_metrics() -> dict:
    return {
        "NVDA": {
            "close": 100.0,
            "atr14": 4.0,
            "atr_pct": 4.0,
            "source": "polygon",
            "source_timestamp": "2026-06-03T14:30:00+00:00",
            "fallback_level": "primary",
            "data_status": "OK",
        }
    }


def _unsafe_actionable_signal() -> Signal:
    return Signal(
        signal_id="unsafe-null-actionable",
        symbol="NVDA",
        action="BUY_WATCH",
        setup_type="momentum_breakout",
        decision="approved",
        risk_tier="tier_1",
        position_size=1.0,
        close=None,
        entry_trigger=None,
        entry_type="breakout",
        entry_reason="unsafe fixture",
        stop_loss=95.0,
        stop_model="atr_stop",
        stop_reason="unsafe fixture",
        target_1=105.0,
        target_2=110.0,
        risk_reward=2.0,
        atr_pct=None,
        setup_score=91.0,
        regime_alignment=0.8,
        valid_until="2026-06-06",
        market_regime="Bullish",
        generated_at="2026-06-03T14:30:00+00:00",
        notes="unsafe fixture should never persist",
        exit_model="momentum_targets",
        exit_reason="unsafe fixture",
        atr14=None,
        data_status="OK",
        source="polygon",
        source_timestamp="2026-06-03T14:30:00+00:00",
        fallback_level="primary",
        score_source="computed",
        data_source="polygon",
        thresholds_version="production",
    )


def test_close1_allows_buy_watch_only_with_complete_close_atr_and_data_provenance() -> None:
    signals = build_signals(
        decision_report=_decision_report(),
        scanner_metrics_map=_valid_metrics(),
        market_regime="Bullish",
    )

    signal = signals[0]
    assert signal.action == "BUY_WATCH"
    assert signal.close == 100.0
    assert signal.atr14 == 4.0
    assert signal.source == "polygon"
    assert signal.source_timestamp == "2026-06-03T14:30:00+00:00"
    assert signal.fallback_level == "primary"
    assert signal.data_status == "OK"
    assert signal.position_size == 1.0


def test_close1_blocks_missing_close_before_actionable_signal() -> None:
    metrics = _valid_metrics()
    metrics["NVDA"]["close"] = None
    metrics["NVDA"]["data_status"] = "BLOCKED"

    signals = build_signals(
        decision_report=_decision_report(),
        scanner_metrics_map=metrics,
        market_regime="Bullish",
    )

    signal = signals[0]
    assert signal.action == "NO_TRADE"
    assert signal.position_size == 0.0
    assert "data_quality: blocked" in signal.notes
    assert "missing_close" in signal.notes


def test_close1_blocks_missing_atr_before_actionable_signal() -> None:
    metrics = _valid_metrics()
    metrics["NVDA"]["atr14"] = None
    metrics["NVDA"]["data_status"] = "BLOCKED"

    signals = build_signals(
        decision_report=_decision_report(),
        scanner_metrics_map=metrics,
        market_regime="Bullish",
    )

    signal = signals[0]
    assert signal.action == "NO_TRADE"
    assert signal.position_size == 0.0
    assert "data_quality: blocked" in signal.notes
    assert "missing_atr" in signal.notes


def test_close1_blocks_degraded_provenance_before_actionable_signal() -> None:
    metrics = _valid_metrics()
    metrics["NVDA"]["source_timestamp"] = None
    metrics["NVDA"]["data_status"] = "DEGRADED"

    signals = build_signals(
        decision_report=_decision_report(),
        scanner_metrics_map=metrics,
        market_regime="Bullish",
    )

    signal = signals[0]
    assert signal.action == "NO_TRADE"
    assert signal.position_size == 0.0
    assert "data_quality: degraded" in signal.notes
    assert "downgraded" in signal.notes


def test_close1_save_signals_blocks_actionable_artifact_with_null_close_entry_or_atr(tmp_path: Path) -> None:
    with pytest.raises(ValueError) as exc:
        save_signals([_unsafe_actionable_signal()], date_str="2026-06-03", signals_dir=tmp_path)

    message = str(exc.value)
    assert "unsafe actionable signal artifact" in message
    assert "unsafe-null-actionable" in message
    assert "missing_close" in message
    assert "missing_entry_trigger" in message
    assert "missing_atr14" in message
    assert not (tmp_path / "2026-06-03-signals.json").exists()
    assert not (tmp_path / "latest-signals.json").exists()


def test_close1_latest_signals_contract_contains_data_quality_and_provenance(tmp_path: Path) -> None:
    signals = build_signals(
        decision_report=_decision_report(),
        scanner_metrics_map=_valid_metrics(),
        market_regime="Bullish",
    )
    save_signals(
        signals,
        date_str="2026-06-03",
        signals_dir=tmp_path,
        data_quality={
            "data_quality_status": "OK",
            "total_symbols": 1,
            "valid_symbols": 1,
            "missing_symbols": [],
            "missing_required_fields": {},
            "missing_provenance_fields": {},
            "stale_symbols": {},
        },
    )

    payload = json.loads((tmp_path / "latest-signals.json").read_text(encoding="utf-8"))
    assert payload["data_quality"]["data_quality_status"] == "OK"
    assert payload["actionable_count"] == 1

    signal = payload["signals"][0]
    assert signal["close"] == 100.0
    assert signal["atr14"] == 4.0
    assert signal["source"] == "polygon"
    assert signal["source_timestamp"] == "2026-06-03T14:30:00+00:00"
    assert signal["fallback_level"] == "primary"
    assert signal["data_status"] == "OK"
