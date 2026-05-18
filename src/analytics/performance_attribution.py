from __future__ import annotations


def attribute_performance(trades: list[dict]) -> dict:
    attribution: dict[str, float] = {}

    for trade in trades:
        factor = trade.get("factor", "unknown")
        pnl = float(trade.get("pnl_percent", 0))
        attribution[factor] = attribution.get(factor, 0) + pnl

    ranked = sorted(
        attribution.items(),
        key=lambda item: item[1],
        reverse=True,
    )

    return {
        "factor_count": len(ranked),
        "top_contributors": ranked[:5],
        "bottom_contributors": ranked[-5:],
    }
