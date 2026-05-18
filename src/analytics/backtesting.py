from __future__ import annotations


def simple_backtest(
    recommendations: list[dict],
    final_prices: dict[str, float],
) -> dict:
    results: list[dict] = []

    for recommendation in recommendations:
        ticker = recommendation["ticker"]

        if ticker not in final_prices:
            continue

        entry_price = recommendation.get("entry_price")
        if entry_price is None:
            continue

        final_price = final_prices[ticker]
        pnl_percent = round(((final_price - entry_price) / entry_price) * 100, 2)

        results.append(
            {
                "ticker": ticker,
                "entry_price": entry_price,
                "final_price": final_price,
                "pnl_percent": pnl_percent,
            }
        )

    if not results:
        return {
            "tested_assets": 0,
            "average_pnl_percent": 0,
            "results": [],
        }

    average = round(
        sum(result["pnl_percent"] for result in results) / len(results),
        2,
    )

    return {
        "tested_assets": len(results),
        "average_pnl_percent": average,
        "results": results,
    }
