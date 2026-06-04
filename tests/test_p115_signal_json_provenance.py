from __future__ import annotations

import json
from pathlib import Path

from src.signals.signal_generator import build_signals, save_signals


def _decision_report() -> dict:
    return {
        "decisions": [
            {
                "symbol": "NVDA",
                "decision": "approved",
                "setup_type": "momentum_breakout",
                "risk_tier": "tier_1",
                "position_size_multiplier": 1.0,
                "setup_score": 79.0,
                "regime_alignment": 0.81,
                "score_source": "scanner_derived",
                "data_source": "live",
                "thresholds_version": "report_scoring_v2",
                "blocked_reasons": [],
                "notes": [],
            }
        ]
    }


def _scanner_metrics() -> dict:
    return {
        "NVDA": {
            "close": 100.0,
            "atr14": 4.0,
            "atr_pct": 4.0,
            "entry": 101.0,
            "stop_loss": 95.0,
            "exit_1": 108.0,
            "exit_2": 112.0,
            "source": "polygon",
            "source_timestamp": "2026-06-04T14:30:00+00:00",
            "fallback_level": "primary",
            "data_status": "OK",
        }
    }


def test_p115_signal_json_contains_score_and_data_provenance(tmp_path: Path) -> None:
    signals = build_signals(
        decision_report=_decision_report(),
        scanner_metrics_map=_scanner_metrics(),
        market_regime="Bullish",
    )

    json_path, _md_path = save_signals(
        signals,
        date_str="2026-06-04",
        signals_dir=tmp_path,
        data_quality={"data_quality_status": "OK", "total_symbols": 1, "valid_symbols": 1},
    )
    payload = json.loads(json_path.read_text(encoding="utf-8"))
    signal = payload["signals"][0]

    assert signal["score_source"] == "scanner_derived"
    assert signal["data_source"] == "live"
    assert signal["thresholds_version"] == "report_scoring_v2"
    assert signal["score_source"] != "demo_arithmetic_sequence"
    assert signal["data_source"] != "demo"
    assert signal["thresholds_version"] != "public_demo"


def test_p115_build_signals_rejects_demo_score_provenance() -> None:
    report = _decision_report()
    report["decisions"][0]["score_source"] = "demo_arithmetic_sequence"

    signals = build_signals(
        decision_report=report,
        scanner_metrics_map=_scanner_metrics(),
        market_regime="Bullish",
    )

    signal = signals[0]
    assert signal.action == "NO_TRADE"
    assert signal.score_source == "demo_arithmetic_sequence"
    assert "demo_score_provenance" in signal.notes


def test_p115_build_signals_rejects_demo_data_source() -> None:
    report = _decision_report()
    report["decisions"][0]["data_source"] = "demo"

    signals = build_signals(
        decision_report=report,
        scanner_metrics_map=_scanner_metrics(),
        market_regime="Bullish",
    )

    signal = signals[0]
    assert signal.action == "NO_TRADE"
    assert signal.data_source == "demo"
    assert "demo_data_source" in signal.notes
