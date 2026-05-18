from __future__ import annotations


def analyze_trade_memory(trades: list[dict]) -> dict:
    if not trades:
        return {
            "best_setup": None,
            "worst_setup": None,
            "setup_statistics": {},
        }

    grouped: dict[str, list[float]] = {}

    for trade in trades:
        setup = trade.get("setup", "Unknown")
        grouped.setdefault(setup, []).append(trade.get("pnl_percent", 0))

    statistics = {
        setup: round(sum(values) / len(values), 2)
        for setup, values in grouped.items()
    }

    best_setup = max(statistics.items(), key=lambda item: item[1])
    worst_setup = min(statistics.items(), key=lambda item: item[1])

    return {
        "best_setup": best_setup,
        "worst_setup": worst_setup,
        "setup_statistics": statistics,
    }
