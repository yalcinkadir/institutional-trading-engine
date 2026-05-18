from __future__ import annotations


def optimize_position_sizes(
    positions: list[dict],
    max_position_percent: float = 20,
) -> list[dict]:
    optimized: list[dict] = []

    for position in positions:
        exposure = position.get("exposure_percent", 0)

        recommendation = "KEEP"
        if exposure > max_position_percent:
            recommendation = "REDUCE"
        elif exposure < max_position_percent * 0.5:
            recommendation = "CAN_INCREASE"

        optimized.append(
            {
                **position,
                "position_recommendation": recommendation,
            }
        )

    return optimized
