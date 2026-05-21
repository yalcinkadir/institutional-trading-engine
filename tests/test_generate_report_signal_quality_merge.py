from __future__ import annotations

from scripts.generate_report import _merge_signal_levels_into_decisions
from src.signals.signal_generator import Signal


def test_merge_signal_quality_fields_into_decisions() -> None:
    decision_report = {
        "decisions": [
            {"symbol": "NVDA", "decision": "approved"},
        ]
    }
    signal = Signal(
        signal_id="sig_NVDA_test",
        symbol="NVDA",
        action="BUY_WATCH",
        setup_type="momentum_breakout",
        decision="approved",
        risk_tier="tier_1",
        position_size=1.0,
        close=100.0,
        entry_trigger=102.0,
        entry_type="breakout",
        entry_reason="breakout entry above current close using 0.5 ATR buffer",
        stop_loss=94.0,
        stop_model="atr_stop",
        stop_reason="ATR stop 2 ATR below entry",
        target_1=114.0,
        target_2=122.0,
        risk_reward=1.5,
        atr_pct=4.0,
        setup_score=91.0,
        regime_alignment=0.8,
        valid_until="2026-05-24",
        market_regime="Bullish",
        generated_at="2026-05-21T08:00:00+00:00",
        notes="",
    )

    _merge_signal_levels_into_decisions(decision_report, [signal])

    item = decision_report["decisions"][0]
    assert item["signal_id"] == "sig_NVDA_test"
    assert item["entry_reason"] == "breakout entry above current close using 0.5 ATR buffer"
    assert item["stop_model"] == "atr_stop"
    assert item["stop_reason"] == "ATR stop 2 ATR below entry"
    assert item["target_1"] == 114.0
