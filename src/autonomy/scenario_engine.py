from __future__ import annotations


def build_market_scenarios(
    market_regime: str,
    vix: float,
    breadth_percent: float,
) -> dict:
    scenarios: list[dict] = []

    if market_regime in {"Strong Bullish", "Bullish"} and vix < 20:
        scenarios.append(
            {
                "scenario": "Risk-On Continuation",
                "probability": 70,
                "strategy": "Favor leaders and momentum continuation",
            }
        )

    if breadth_percent < 45:
        scenarios.append(
            {
                "scenario": "Weak Breadth Rotation",
                "probability": 55,
                "strategy": "Reduce aggressive exposure",
            }
        )

    if vix > 25:
        scenarios.append(
            {
                "scenario": "Volatility Expansion",
                "probability": 65,
                "strategy": "Increase defensive positioning",
            }
        )

    if not scenarios:
        scenarios.append(
            {
                "scenario": "Neutral Consolidation",
                "probability": 50,
                "strategy": "Wait for confirmation",
            }
        )

    return {
        "scenario_count": len(scenarios),
        "scenarios": scenarios,
    }
