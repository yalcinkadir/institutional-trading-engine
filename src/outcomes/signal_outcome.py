from __future__ import annotations


def classify_signal_outcome(
    entry_price: float,
    current_price: float,
    bullish: bool = True,
    neutral_threshold_percent: float = 1.0,
) -> dict:
    performance = ((current_price - entry_price) / entry_price) * 100

    if not bullish:
        performance *= -1

    performance = round(performance, 2)

    if performance > neutral_threshold_percent:
        classification = "WIN"
    elif performance < -neutral_threshold_percent:
        classification = "LOSS"
    else:
        classification = "NEUTRAL"

    return {
        "performance_percent": performance,
        "classification": classification,
    }
