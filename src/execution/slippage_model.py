from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SlippageEstimate:
    estimated_slippage_percent: float
    execution_quality: str


class SlippageModel:
    def estimate(
        self,
        volatility_percent: float,
        spread_percent: float,
        order_size_percent_adv: float,
    ) -> SlippageEstimate:
        slippage = (
            (volatility_percent * 0.15)
            + (spread_percent * 2)
            + (order_size_percent_adv * 0.5)
        )

        if slippage <= 0.5:
            quality = "excellent"
        elif slippage <= 1.5:
            quality = "acceptable"
        else:
            quality = "poor"

        return SlippageEstimate(
            estimated_slippage_percent=round(slippage, 2),
            execution_quality=quality,
        )


slippage_model = SlippageModel()
