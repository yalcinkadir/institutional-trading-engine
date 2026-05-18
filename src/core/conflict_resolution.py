from __future__ import annotations


def resolve_signal_conflicts(signals: dict[str, str]) -> dict:
    bullish = sum(1 for value in signals.values() if "bullish" in value.lower())
    bearish = sum(1 for value in signals.values() if "bearish" in value.lower())

    if bullish > bearish:
        resolution = "Bullish Consensus"
    elif bearish > bullish:
        resolution = "Bearish Consensus"
    else:
        resolution = "Mixed Signals"

    confidence_penalty = abs(bullish - bearish) * 5

    return {
        "resolution": resolution,
        "bullish_signals": bullish,
        "bearish_signals": bearish,
        "confidence_penalty": confidence_penalty,
    }
