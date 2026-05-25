from __future__ import annotations

import math
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Mapping


DEFAULT_REGIME_MULTIPLIERS: Mapping[str, float] = MappingProxyType(
    {
        "low_vol_bull": 1.0,
        "normal": 1.0,
        "neutral": 1.1,
        "high_vol": 1.4,
        "high_vol_transition": 1.5,
        "volatile": 1.6,
        "risk_off": 2.0,
        "panic": 3.0,
        "panic_dislocation": 3.5,
    }
)


@dataclass(frozen=True)
class SlippageEstimate:
    estimated_slippage_percent: float
    execution_quality: str
    spread_cost_percent: float
    market_impact_percent: float
    regime_multiplier: float
    model_version: str


@dataclass(frozen=True)
class SlippageConfig:
    """Configuration for the square-root market-impact model.

    Inputs and outputs are percentages, not decimals. For example, pass `0.05`
    for five basis points and `1.0` for one percent.
    """

    model_version: str = "sqrt-impact-v1"
    spread_multiplier: float = 1.5
    impact_coefficient: float = 0.314
    regime_multipliers: Mapping[str, float] = field(default_factory=lambda: DEFAULT_REGIME_MULTIPLIERS)
    excellent_threshold_percent: float = 0.05
    acceptable_threshold_percent: float = 0.20
    poor_threshold_percent: float = 0.50


class SlippageModel:
    """Estimate execution slippage using a regime-aware square-root impact model.

    The model separates half-spread cost from market impact. Market impact follows
    the common square-root intuition: larger orders consume liquidity in a
    non-linear way, while volatile and stressed regimes amplify impact.
    """

    def __init__(self, config: SlippageConfig | None = None):
        self.config = config or SlippageConfig()

    def estimate(
        self,
        volatility_percent: float,
        spread_percent: float,
        order_size_percent_adv: float,
        regime_label: str = "neutral",
    ) -> SlippageEstimate:
        volatility = _non_negative(volatility_percent)
        spread = _non_negative(spread_percent)
        order_size = _non_negative(order_size_percent_adv)

        spread_cost = (spread / 2.0) * self.config.spread_multiplier
        raw_impact = volatility * math.sqrt(order_size / 100.0) * self.config.impact_coefficient if order_size > 0 else 0.0
        regime_multiplier = self._regime_multiplier(regime_label)
        market_impact = raw_impact * regime_multiplier
        total = spread_cost + market_impact

        return SlippageEstimate(
            estimated_slippage_percent=round(total, 4),
            execution_quality=self._quality(total),
            spread_cost_percent=round(spread_cost, 4),
            market_impact_percent=round(market_impact, 4),
            regime_multiplier=round(regime_multiplier, 4),
            model_version=self.config.model_version,
        )

    def _regime_multiplier(self, regime_label: str) -> float:
        normalized = str(regime_label or "neutral").strip().lower()
        return float(self.config.regime_multipliers.get(normalized, self.config.regime_multipliers.get("neutral", 1.0)))

    def _quality(self, total_slippage_percent: float) -> str:
        if total_slippage_percent <= self.config.excellent_threshold_percent:
            return "excellent"
        if total_slippage_percent <= self.config.acceptable_threshold_percent:
            return "acceptable"
        if total_slippage_percent <= self.config.poor_threshold_percent:
            return "poor"
        return "prohibitive"


def _non_negative(value: float) -> float:
    return max(0.0, float(value))


slippage_model = SlippageModel()
