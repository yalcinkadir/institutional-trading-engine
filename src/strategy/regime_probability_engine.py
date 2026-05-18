from __future__ import annotations


def estimate_regime_probabilities(
    bullish_signals: int,
    bearish_signals: int,
    neutral_signals: int,
) -> dict:
    total = bullish_signals + bearish_signals + neutral_signals

    if total <= 0:
        return {
            "bullish_probability": 0,
            "bearish_probability": 0,
            "neutral_probability": 0,
        }

    bullish_probability = round((bullish_signals / total) * 100, 2)
    bearish_probability = round((bearish_signals / total) * 100, 2)
    neutral_probability = round((neutral_signals / total) * 100, 2)

    dominant = max(
        {
            "bullish": bullish_probability,
            "bearish": bearish_probability,
            "neutral": neutral_probability,
        }.items(),
        key=lambda item: item[1],
    )[0]

    return {
        "bullish_probability": bullish_probability,
        "bearish_probability": bearish_probability,
        "neutral_probability": neutral_probability,
        "dominant_regime": dominant,
    }
