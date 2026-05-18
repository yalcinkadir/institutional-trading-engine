from __future__ import annotations


def optimize_portfolio_weights(assets: list[dict], max_weight: float = 0.25) -> dict:
    if not assets:
        return {
            "weights": {},
            "total_weight": 0,
        }

    positive_scores = {
        asset["ticker"]: max(asset.get("score", 0), 0)
        for asset in assets
    }

    total_score = sum(positive_scores.values())

    if total_score <= 0:
        equal_weight = round(1 / len(assets), 4)
        weights = {asset["ticker"]: equal_weight for asset in assets}
    else:
        weights = {
            ticker: min(score / total_score, max_weight)
            for ticker, score in positive_scores.items()
        }

    total = sum(weights.values())
    if total > 0:
        weights = {
            ticker: round(weight / total, 4)
            for ticker, weight in weights.items()
        }

    return {
        "weights": weights,
        "total_weight": round(sum(weights.values()), 4),
    }
