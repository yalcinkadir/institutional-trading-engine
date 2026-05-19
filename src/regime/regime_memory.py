from __future__ import annotations

from dataclasses import dataclass, field

from src.regime.regime_similarity_engine import MarketRegime


@dataclass
class RegimeMemory:
    regimes: list[MarketRegime] = field(default_factory=list)

    def add(self, regime: MarketRegime) -> None:
        self.regimes.append(regime)

    def latest(self, limit: int = 10) -> list[MarketRegime]:
        return self.regimes[-limit:]


regime_memory = RegimeMemory()
