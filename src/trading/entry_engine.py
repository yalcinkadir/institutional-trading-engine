from __future__ import annotations


def evaluate_entry(
    setup_status: str,
    confidence_level: str,
    market_regime: str,
) -> dict:
    if setup_status == "READY" and confidence_level in {"Very High", "High"}:
        action = "ENTER"
    elif setup_status == "WATCH":
        action = "MONITOR"
    elif setup_status in {"EARLY", "RISKY"}:
        action = "WAIT"
    else:
        action = "AVOID"

    aggressive = market_regime in {"Strong Bullish", "Bullish"}

    return {
        "action": action,
        "aggressive_mode": aggressive,
    }
