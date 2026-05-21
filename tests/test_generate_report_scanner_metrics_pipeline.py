from __future__ import annotations

from scripts.generate_report import _merge_signal_levels_into_decisions
from src.signals.scanner_metrics_pipeline import normalize_scanner_metrics_map
from src.signals.signal_generator import build_signals


def test_report_path_scanner_metrics_reach_generated_signals() -> None:
    decision_report = {
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
    raw_metrics = {
        "NVDA": {
            "symbol": "NVDA",
            "close": 100.0,
            "atr14": 4.0,
            "atr_pct": 4.0,
        }
    }

    normalized, diagnostics = normalize_scanner_metrics_map(raw_metrics, ["NVDA"])
    signals = build_signals(
        decision_report=decision_report,
        scanner_metrics_map=normalized,
        market_regime="Bullish",
    )
    _merge_signal_levels_into_decisions(decision_report, signals)

    assert not diagnostics.has_warnings
    assert diagnostics.valid_symbols == 1

    signal = signals[0]
    assert signal.action == "BUY_WATCH"
    assert signal.close == 100.0
    assert signal.atr_pct == 4.0
    assert signal.entry_trigger is not None
    assert signal.stop_loss is not None
    assert signal.target_1 is not None

    decision = decision_report["decisions"][0]
    assert decision["close"] == 100.0
    assert decision["entry_trigger"] == signal.entry_trigger
    assert decision["stop_loss"] == signal.stop_loss
    assert decision["target_1"] == signal.target_1
    assert decision["entry_reason"] == signal.entry_reason
    assert decision["stop_reason"] == signal.stop_reason
    assert decision["exit_reason"] == signal.exit_reason


def test_report_path_missing_metrics_stays_visible_and_non_fatal() -> None:
    decision_report = {
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

    normalized, diagnostics = normalize_scanner_metrics_map({}, ["NVDA"])
    signals = build_signals(
        decision_report=decision_report,
        scanner_metrics_map=normalized,
        market_regime="Bullish",
    )

    assert diagnostics.has_warnings
    assert diagnostics.warning_lines() == ["scanner_metrics_missing:NVDA"]
    assert signals[0].action == "NO_TRADE"
    assert "missing_close" in signals[0].notes
