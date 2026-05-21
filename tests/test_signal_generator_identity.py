from __future__ import annotations

import json
from pathlib import Path

from src.signals.signal_generator import build_signals, save_signals


def _decision_report(setup_type: str = "momentum_breakout") -> dict:
    return {
        "decisions": [
            {
                "symbol": "NVDA",
                "decision": "approved",
                "setup_type": setup_type,
                "risk_tier": "tier_1",
                "position_size_multiplier": 1.0,
                "setup_score": 91.0,
                "regime_alignment": 0.8,
                "blocked_reasons": [],
                "notes": ["leader"],
            },
            {
                "symbol": "XLE",
                "decision": "no_trade",
                "setup_type": "defensive_rotation",
                "risk_tier": "no_trade",
                "position_size_multiplier": 0.0,
                "setup_score": 44.0,
                "regime_alignment": 0.2,
                "blocked_reasons": ["weak setup"],
                "notes": [],
            },
        ]
    }


def _scanner_metrics() -> dict:
    return {
        "NVDA": {
            "close": 100.0,
            "atr14": 4.0,
            "atr_pct": 4.0,
        }
    }


def _breakout_context_metrics() -> dict:
    return {
        "NVDA": {
            "close": 100.0,
            "atr14": 4.0,
            "atr_pct": 4.0,
            "high": 101.0,
            "rvol": 1.2,
            "vwap": 99.0,
        }
    }


def test_build_signals_assigns_native_signal_id() -> None:
    signals = build_signals(_decision_report(), _scanner_metrics(), "Bullish")

    assert len(signals) == 2
    assert all(signal.signal_id for signal in signals)
    assert signals[0].signal_id.startswith("sig_NVDA_")
    assert signals[1].signal_id.startswith("sig_XLE_")


def test_build_signals_produces_buy_watch_only_with_valid_trade_plan() -> None:
    signals = build_signals(_decision_report(), _scanner_metrics(), "Bullish")

    nvda = signals[0]
    assert nvda.action == "BUY_WATCH"
    assert nvda.entry_trigger is not None
    assert nvda.stop_loss is not None
    assert nvda.target_1 is not None
    assert nvda.entry_type == "breakout"
    assert nvda.entry_reason
    assert nvda.stop_model == "atr_stop"
    assert nvda.stop_reason
    assert nvda.exit_model == "momentum_targets"
    assert nvda.exit_reason
    assert nvda.risk_reward is not None
    assert nvda.risk_reward >= 1.2
    assert nvda.position_size == 1.0


def test_build_signals_uses_high_trigger_for_breakout_context() -> None:
    signals = build_signals(_decision_report(), _breakout_context_metrics(), "Bullish")

    nvda = signals[0]
    assert nvda.action == "BUY_WATCH"
    assert nvda.entry_trigger == 101.1
    assert "scanner high" in nvda.entry_reason


def test_build_signals_uses_swing_low_structure_stop() -> None:
    metrics = _breakout_context_metrics()
    metrics["NVDA"]["swing_low_3bar"] = 96.0

    signals = build_signals(_decision_report(), metrics, "Bullish")

    nvda = signals[0]
    assert nvda.action == "BUY_WATCH"
    assert nvda.stop_model == "swing_low_structure_stop"
    assert nvda.stop_loss == 95.81
    assert "swing-low structure stop" in nvda.stop_reason


def test_build_signals_downgrades_low_rvol_breakout() -> None:
    metrics = _breakout_context_metrics()
    metrics["NVDA"]["rvol"] = 0.7

    signals = build_signals(_decision_report(), metrics, "Bullish")

    nvda = signals[0]
    assert nvda.action == "NO_TRADE"
    assert "insufficient_volume_for_breakout" in nvda.notes


def test_build_signals_downgrades_breakout_below_vwap() -> None:
    metrics = _breakout_context_metrics()
    metrics["NVDA"]["close"] = 99.0
    metrics["NVDA"]["vwap"] = 100.0

    signals = build_signals(_decision_report(), metrics, "Bullish")

    nvda = signals[0]
    assert nvda.action == "NO_TRADE"
    assert "breakout_entry_below_vwap" in nvda.notes


def test_build_signals_supports_pullback_entry_stop_and_exit_reason() -> None:
    signals = build_signals(
        _decision_report(setup_type="pullback_continuation"),
        _scanner_metrics(),
        "Bullish",
    )

    nvda = signals[0]
    assert nvda.action == "BUY_WATCH"
    assert nvda.entry_type == "pullback"
    assert "pullback entry" in nvda.entry_reason
    assert nvda.stop_model == "pullback_structure_stop"
    assert "pullback structure stop" in nvda.stop_reason
    assert nvda.exit_model == "pullback_targets"
    assert "pullback continuation targets" in nvda.exit_reason


def test_build_signals_downgrades_approved_signal_without_executable_levels() -> None:
    signals = build_signals(_decision_report(), {}, "Bullish")

    nvda = signals[0]
    assert nvda.action == "NO_TRADE"
    assert nvda.position_size == 0.0
    assert nvda.entry_trigger is None
    assert nvda.stop_loss is None
    assert nvda.target_1 is None
    assert "missing_close" in nvda.notes
    assert "missing_entry_trigger" in nvda.notes
    assert "missing_stop_loss" in nvda.notes
    assert "missing_target_1" in nvda.notes


def test_build_signals_downgrades_when_entry_stop_exist_but_atr_missing() -> None:
    partial_metrics = {
        "NVDA": {
            "close": 100.0,
            "atr_pct": 4.0,
            "entry": 101.0,
            "stop_loss": 95.0,
        }
    }

    signals = build_signals(_decision_report(), partial_metrics, "Bullish")

    nvda = signals[0]
    assert nvda.action == "NO_TRADE"
    assert nvda.position_size == 0.0
    assert "missing_or_invalid_atr" in nvda.notes
    assert "missing_entry_trigger" in nvda.notes
    assert "missing_stop_loss" in nvda.notes
    assert "missing_target_1" in nvda.notes


def test_build_signals_downgrades_low_risk_reward_trade_plan() -> None:
    low_rr_metrics = {
        "NVDA": {
            "close": 100.0,
            "atr14": 4.0,
            "atr_pct": 4.0,
            "entry": 100.0,
            "stop_loss": 96.0,
            "exit_1": 103.0,
        }
    }

    signals = build_signals(_decision_report(), low_rr_metrics, "Bullish")

    nvda = signals[0]
    assert nvda.action == "NO_TRADE"
    assert nvda.risk_reward is None
    assert "risk_reward_below_minimum" in nvda.notes


def test_build_signals_downgrades_inverted_stop_trade_plan() -> None:
    inverted_stop_metrics = {
        "NVDA": {
            "close": 100.0,
            "atr14": 4.0,
            "atr_pct": 4.0,
            "entry": 100.0,
            "stop_loss": 101.0,
            "exit_1": 108.0,
        }
    }

    signals = build_signals(_decision_report(), inverted_stop_metrics, "Bullish")

    nvda = signals[0]
    assert nvda.action == "NO_TRADE"
    assert "scanner_stop_not_below_entry" in nvda.notes
    assert "missing_target_1" in nvda.notes


def test_build_signals_downgrades_invalid_scanner_target() -> None:
    invalid_target_metrics = {
        "NVDA": {
            "close": 100.0,
            "atr14": 4.0,
            "atr_pct": 4.0,
            "entry": 102.0,
            "stop_loss": 94.0,
            "exit_1": 101.0,
        }
    }

    signals = build_signals(_decision_report(), invalid_target_metrics, "Bullish")

    nvda = signals[0]
    assert nvda.action == "NO_TRADE"
    assert "target_1_not_above_entry" in nvda.notes


def test_build_signals_downgrades_late_scanner_entry() -> None:
    late_metrics = {
        "NVDA": {
            "close": 110.0,
            "atr14": 4.0,
            "atr_pct": 3.6,
            "entry": 100.0,
            "entry_type": "breakout",
            "stop_loss": 96.0,
            "exit_1": 108.0,
        }
    }

    signals = build_signals(_decision_report(), late_metrics, "Bullish")

    nvda = signals[0]
    assert nvda.action == "NO_TRADE"
    assert "late_entry_price_extended_beyond_trigger" in nvda.notes


def test_build_signals_produces_stable_ids_when_time_is_fixed(monkeypatch) -> None:
    class FixedDatetime:
        @staticmethod
        def now(tz=None):
            from datetime import datetime
            return datetime(2026, 5, 21, 8, 0, 0, tzinfo=tz)

    monkeypatch.setattr("src.signals.signal_generator.datetime", FixedDatetime)

    first = build_signals(_decision_report(), _scanner_metrics(), "Bullish")
    second = build_signals(_decision_report(), _scanner_metrics(), "Bullish")

    assert [signal.signal_id for signal in first] == [signal.signal_id for signal in second]


def test_save_signals_writes_quality_fields_to_json_and_markdown(tmp_path: Path) -> None:
    signals = build_signals(_decision_report(), _scanner_metrics(), "Bullish")

    json_path, md_path = save_signals(signals, date_str="2026-05-21", signals_dir=tmp_path)

    payload = json.loads(json_path.read_text(encoding="utf-8"))
    latest_payload = json.loads((tmp_path / "latest-signals.json").read_text(encoding="utf-8"))
    markdown = md_path.read_text(encoding="utf-8")

    assert all(item.get("signal_id") for item in payload["signals"])
    assert all(item.get("entry_reason") for item in payload["signals"])
    assert all(item.get("stop_reason") for item in payload["signals"])
    assert all(item.get("exit_reason") for item in payload["signals"])
    assert all(item.get("signal_id") for item in latest_payload["signals"])
    assert "Signal ID" in markdown
    assert "Entry Reason:" in markdown
    assert "Stop Reason:" in markdown
    assert "Exit Reason:" in markdown
    assert signals[0].signal_id in markdown


def test_save_signals_actionable_count_excludes_downgraded_signals(tmp_path: Path) -> None:
    signals = build_signals(_decision_report(), {}, "Bullish")

    json_path, md_path = save_signals(signals, date_str="2026-05-21", signals_dir=tmp_path)
    payload = json.loads(json_path.read_text(encoding="utf-8"))
    markdown = md_path.read_text(encoding="utf-8")

    assert payload["actionable_count"] == 0
    assert payload["no_trade_count"] == 2
    assert all(item["action"] == "NO_TRADE" for item in payload["signals"])
    assert "No executable BUY_WATCH signals generated" in markdown
    assert "downgraded: invalid trade plan" in markdown
