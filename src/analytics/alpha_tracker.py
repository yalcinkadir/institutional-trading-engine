from __future__ import annotations


def calculate_alpha(
    asset_return_percent: float,
    benchmark_return_percent: float,
) -> dict:
    alpha = round(asset_return_percent - benchmark_return_percent, 2)

    if alpha > 2:
        quality = "Strong Alpha"
    elif alpha > 0:
        quality = "Positive Alpha"
    elif alpha == 0:
        quality = "Market Perform"
    else:
        quality = "Negative Alpha"

    return {
        "alpha_percent": alpha,
        "quality": quality,
    }


def summarize_alpha(results: list[dict]) -> dict:
    if not results:
        return {
            "signals": 0,
            "average_alpha_percent": 0,
            "positive_alpha_rate": 0,
        }

    alphas = [result.get("alpha_percent", 0) for result in results]
    positive = [alpha for alpha in alphas if alpha > 0]

    return {
        "signals": len(results),
        "average_alpha_percent": round(sum(alphas) / len(alphas), 2),
        "positive_alpha_rate": round((len(positive) / len(alphas)) * 100, 2),
    }
