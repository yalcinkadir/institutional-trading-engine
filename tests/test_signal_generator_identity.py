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


def test_build_signals_assigns_native_signal_id() -> None:
    signals = build_signals(
        decision_report=_decision_report(),
        scanner_metrics_map=_scanner_metrics(),
        market_regime="Bullish",
    )

    assert len(signals) == 2
    assert all(signal.signal_id for signal in signals)
    assert signals[0].signal_id.startswith("sig_NVDA_")
    assert signals[1].signal_id.startswith("sig_XLE_")


def test_build_signals_produces_buy_watch_only_with_executable_levels() -> None:
    signals = build_signals(
        decision_report=_decision_report(),
        scanner_metrics_map=_scanner_metrics(),
        market_regime="Bullish",
    )

    nvda = signals[0]
    assert nvda.action == "BUY_WATCH"
    assert nvda.entry_trigger is not None
    assert nvda.stop_loss is not None
    assert nvda.target_1 is not None
    assert nvda.position_size == 1.0


def test_build_signals_downgrades_approved_signal_without_executable_levels() -> None:
    signals = build_signals(
        decision_report=_decision_report(),
        scanner_metrics_map={},
        market_regime="Bullish",
    )

    nvda = signals[0]
    assert nvda.action == "NO_TRADE"
    assert nvda.position_size == 0.0
    assert nvda.entry_trigger is None
    assert nvda.stop_loss is None
    assert nvda.target_1 is None
    assert "downgraded: incomplete executable levels" in nvda.notes
    assert "entry_trigger" in nvda.notes
    assert "stop_loss" in nvda.notes
    assert "target_1" in nvda.notes


def test_build_signals_downgrades_when_only_partial_levels_exist() -> None:
    partial_metrics = {
        "NVDA": {
            "close": 100.0,
            "atr_pct": 4.0,
            "entry": 101.0,
            "stop_loss": 95.0,
        }
    }

    signals = build_signals(
        decision_report=_decision_report(),
        scanner_metrics_map=partial_metrics,
        market_regime="Bullish",
    )

    nvda = signals[0]
    assert nvda.action == "NO_TRADE"
    assert nvda.position_size == 0.0
    assert "target_1" in nvda.notes


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


def test_save_signals_writes_signal_id_to_json_and_markdown(tmp_path: Path) -> None:
    signals = build_signals(
        decision_report=_decision_report(),
        scanner_metrics_map=_scanner_metrics(),
        market_regime="Bullish",
    )

    json_path, md_path = save_signals(signals, date_str="2026-05-21", signals_dir=tmp_path)

    payload = json.loads(json_path.read_text(encoding="utf-8"))
    latest_payload = json.loads((tmp_path / "latest-signals.json").read_text(encoding="utf-8"))
    markdown = md_path.read_text(encoding="utf-8")

    assert all(item.get("signal_id") for item in payload["signals"])
    assert all(item.get("signal_id") for item in latest_payload["signals"])
    assert "Signal ID" in markdown
    assert signals[0].signal_id in markdown


def test_save_signals_actionable_count_excludes_downgraded_signals(tmp_path: Path) -> None:
    signals = build_signals(
        decision_report=_decision_report(),
        scanner_metrics_map={},
        market_regime="Bullish",
    )

    json_path, md_path = save_signals(signals, date_str="2026-05-21", signals_dir=tmp_path)
    payload = json.loads(json_path.read_text(encoding="utf-8"))
    markdown = md_path.read_text(encoding="utf-8")

    assert payload["actionable_count"] == 0
    assert payload["no_trade_count"] == 2
    assert all(item["action"] == "NO_TRADE" for item in payload["signals"])
    assert "No executable BUY_WATCH signals generated" in markdown
    assert "downgraded: incomplete executable levels" in markdown
