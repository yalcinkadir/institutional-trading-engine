from __future__ import annotations

from pathlib import Path

from src.signals.signal_generator import build_signals


SIGNAL_GENERATOR = Path("src/signals/signal_generator.py")
SIGNAL_HELPER_IMPORTS = [
    "from src.signals.entry_quality import derive_entry_quality",
    "from src.signals.exit_target_quality import derive_exit_target_quality",
    "from src.signals.signal_identity import build_signal_id",
    "from src.signals.stop_loss_quality import derive_stop_loss_quality",
    "from src.signals.trade_plan_validator import validate_long_trade_plan",
]


def test_arch106_signal_generator_declares_runtime_helper_imports() -> None:
    source = SIGNAL_GENERATOR.read_text(encoding="utf-8")

    for import_line in SIGNAL_HELPER_IMPORTS:
        assert import_line in source


def test_arch106_signal_runtime_helpers_execute_on_buy_watch_path() -> None:
    decision_report = {
        "decisions": [
            {
                "symbol": "NVDA",
                "decision": "approved",
                "setup_type": "momentum_breakout",
                "risk_tier": "tier_1",
                "position_size_multiplier": 1.0,
                "setup_score": 91.0,
                "regime_alignment": 0.85,
                "blocked_reasons": [],
                "notes": [],
                "score_source": "institutional_pipeline",
                "data_source": "polygon",
                "thresholds_version": "prod_v1",
            }
        ]
    }
    scanner_metrics_map = {
        "NVDA": {
            "close": 100.0,
            "atr14": 4.0,
            "atr_pct": 4.0,
            "high": 101.0,
            "rvol": 1.2,
            "vwap": 99.0,
            "source": "polygon",
            "source_timestamp": "2026-06-08T13:30:00+00:00",
            "fallback_level": "primary",
            "data_status": "OK",
        }
    }

    signals = build_signals(
        decision_report=decision_report,
        scanner_metrics_map=scanner_metrics_map,
        market_regime="Bullish",
    )

    assert len(signals) == 1
    signal = signals[0]

    assert signal.symbol == "NVDA"
    assert signal.action == "BUY_WATCH"
    assert signal.signal_id.startswith("sig_NVDA_")
    assert signal.entry_type == "breakout"
    assert signal.entry_trigger == 101.1
    assert signal.stop_model == "atr_stop"
    assert signal.stop_loss == 93.1
    assert signal.exit_model == "momentum_targets"
    assert signal.target_1 == 113.1
    assert signal.target_2 == 121.1
    assert signal.risk_reward == 1.5
    assert signal.position_size == 1.0
    assert signal.notes == ""
