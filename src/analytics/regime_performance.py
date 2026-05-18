from __future__ import annotations


def analyze_regime_performance(trades: list[dict]) -> dict:
    grouped: dict[str, list[dict]] = {}

    for trade in trades:
        regime = trade.get("market_regime", "Unknown")
        grouped.setdefault(regime, []).append(trade)

    summary: dict[str, dict] = {}

    for regime, regime_trades in grouped.items():
        pnl_values = [trade.get("pnl_percent", 0) for trade in regime_trades]
        wins = [value for value in pnl_values if value > 0]

        summary[regime] = {
            "trades": len(regime_trades),
            "average_pnl_percent": round(sum(pnl_values) / len(pnl_values), 2),
            "win_rate": round((len(wins) / len(pnl_values)) * 100, 2),
        }

    return summary
