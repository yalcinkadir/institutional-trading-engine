from __future__ import annotations

import json
from pathlib import Path

from scripts.generate_outcomes import scan_signal_files
from src.signals.signal_generator import build_signals, save_signals
from src.watchers.entry_exit_watcher import build_watcher_market_data_health


DATA_QUALITY_OK = {
    "source": "polygon",
    "source_timestamp": "2026-06-11T14:30:00+00:00",
    "fallback_level": "primary",
    "data_status": "OK",
}


def _decision_report(*, decision: str = "approved", risk_tier: str = "tier_2") -> dict:
    return {
        "decisions": [
            {
                "symbol": "NVDA",
                "decision": decision,
                "setup_type": "momentum_breakout",
                "risk_tier": risk_tier,
                "position_size_multiplier": 0.75,
                "setup_score": 88.0,
                "regime_alignment": 0.7,
                "blocked_reasons": [],
                "notes": ["candidate accepted by decision layer"],
            }
        ]
    }


def _valid_scanner_metrics() -> dict:
    return {
        "NVDA": {
            **DATA_QUALITY_OK,
            "close": 100.0,
            "atr14": 4.0,
            "atr_pct": 4.0,
            "high": 101.0,
            "rvol": 1.2,
            "vwap": 99.0,
        }
    }


def test_194_no_trade_export_cannot_look_approved_or_executable(tmp_path: Path) -> None:
    """NO_TRADE records must not retain approved/tradable state at the boundary."""
    signals = build_signals(
        decision_report=_decision_report(decision="approved", risk_tier="tier_2"),
        scanner_metrics_map={},
        market_regime="Bullish",
    )

    signal = signals[0]
    assert signal.action == "NO_TRADE"
    assert signal.decision == "blocked"
    assert signal.decision != "approved"
    assert signal.risk_tier == "NO_TRADE"
    assert signal.position_size == 0.0
    assert signal.entry_trigger is None
    assert signal.stop_loss is None
    assert signal.target_1 is None

    json_path, _ = save_signals(signals, date_str="2026-06-11", signals_dir=tmp_path)
    payload = json.loads(json_path.read_text(encoding="utf-8"))
    persisted = payload["signals"][0]

    assert payload["actionable_count"] == 0
    assert persisted["action"] == "NO_TRADE"
    assert persisted["decision"] == "blocked"
    assert persisted["risk_tier"] == "NO_TRADE"
    assert persisted["position_size"] == 0.0
    assert persisted["entry_trigger"] is None

    outcome_scan = scan_signal_files(days=999, signals_dir=tmp_path)
    assert outcome_scan["valid_signal_count"] == 0
    assert outcome_scan["invalid_signal_count"] == 1
    assert "non_actionable_signal" in outcome_scan["skip_reasons"]

    watcher_health = build_watcher_market_data_health(payload["signals"], evaluated_symbols=[])
    assert watcher_health.checked_signal_count == 0
    assert watcher_health.missing_market_data_count == 0


def test_194_buy_watch_keeps_execution_ready_state_only_with_valid_trade_plan() -> None:
    """BUY_WATCH is allowed only when exported fields are consistently executable."""
    signals = build_signals(
        decision_report=_decision_report(decision="approved", risk_tier="tier_2"),
        scanner_metrics_map=_valid_scanner_metrics(),
        market_regime="Bullish",
    )

    signal = signals[0]
    assert signal.action == "BUY_WATCH"
    assert signal.decision == "approved"
    assert signal.risk_tier == "tier_2"
    assert signal.position_size == 0.75
    assert signal.close == 100.0
    assert signal.atr14 == 4.0
    assert signal.entry_trigger is not None
    assert signal.stop_loss is not None
    assert signal.target_1 is not None
    assert signal.source == "polygon"
    assert signal.data_status == "OK"
