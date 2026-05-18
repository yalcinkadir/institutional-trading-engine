from __future__ import annotations


def explain_signal_decision(signals: dict[str, float]) -> dict:
    ranked = sorted(
        signals.items(),
        key=lambda item: abs(item[1]),
        reverse=True,
    )

    dominant = ranked[:5]

    explanation = []

    for signal, value in dominant:
        direction = "bullish" if value >= 0 else "bearish"
        explanation.append(
            f"{signal} contributed {direction} influence ({round(value, 2)})"
        )

    return {
        "dominant_signals": dominant,
        "explanations": explanation,
    }
