from __future__ import annotations


def build_dynamic_watchlist(
    leaders: list[dict],
    weak_names: list[dict],
    market_regime: str,
) -> dict:
    focus = "balanced"

    if market_regime in {"Strong Bullish", "Bullish"}:
        focus = "aggressive_growth"
    elif market_regime in {"Defensive", "Risk-Off"}:
        focus = "capital_preservation"

    return {
        "focus": focus,
        "leaders": leaders[:5],
        "weak_names": weak_names[:5],
    }
