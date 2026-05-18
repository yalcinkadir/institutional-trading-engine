from __future__ import annotations


def calculate_performance_statistics(trades: list[dict]) -> dict:
    total_trades = len(trades)

    if total_trades == 0:
        return {
            "total_trades": 0,
            "win_rate": 0,
            "total_pnl": 0,
            "average_pnl_percent": 0,
        }

    wins = [trade for trade in trades if trade.get("outcome") == "WIN"]
    total_pnl = round(sum(trade.get("pnl", 0) for trade in trades), 2)
    avg_pnl_percent = round(
        sum(trade.get("pnl_percent", 0) for trade in trades) / total_trades,
        2,
    )

    return {
        "total_trades": total_trades,
        "win_rate": round((len(wins) / total_trades) * 100, 2),
        "total_pnl": total_pnl,
        "average_pnl_percent": avg_pnl_percent,
    }
