from __future__ import annotations

from dataclasses import dataclass, field

from src.portfolio.adaptive_portfolio_intelligence import PortfolioRiskAdjustment


@dataclass
class PortfolioRiskMemory:
    history: list[PortfolioRiskAdjustment] = field(default_factory=list)

    def add(self, adjustment: PortfolioRiskAdjustment) -> None:
        self.history.append(adjustment)

    def latest(self, limit: int = 20) -> list[PortfolioRiskAdjustment]:
        return self.history[-limit:]


portfolio_risk_memory = PortfolioRiskMemory()
