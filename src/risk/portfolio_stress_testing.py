from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class StressScenario:
    market_drop_percent: float
    volatility_spike_percent: float
    correlation_breakdown_percent: float


@dataclass(frozen=True)
class StressTestResult:
    projected_drawdown_percent: float
    projected_portfolio_stress: str


class PortfolioStressTester:
    def simulate(
        self,
        portfolio_beta: float,
        scenario: StressScenario,
    ) -> StressTestResult:
        projected_drawdown = (
            (scenario.market_drop_percent * portfolio_beta)
            + (scenario.volatility_spike_percent * 0.15)
            + (scenario.correlation_breakdown_percent * 0.1)
        )

        if projected_drawdown >= 35:
            stress = "severe"
        elif projected_drawdown >= 20:
            stress = "high"
        elif projected_drawdown >= 10:
            stress = "moderate"
        else:
            stress = "manageable"

        return StressTestResult(
            projected_drawdown_percent=round(projected_drawdown, 2),
            projected_portfolio_stress=stress,
        )


portfolio_stress_tester = PortfolioStressTester()
