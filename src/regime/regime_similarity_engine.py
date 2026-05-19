from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class MarketRegime:
    name: str
    market_health_score: float
    volatility: float
    breadth: float
    momentum: float


@dataclass(frozen=True)
class RegimeSimilarity:
    current_regime: str
    historical_regime: str
    similarity_score: float


class RegimeSimilarityEngine:
    def compare(
        self,
        current: MarketRegime,
        historical: list[MarketRegime],
    ) -> list[RegimeSimilarity]:
        similarities: list[RegimeSimilarity] = []

        for regime in historical:
            score = self._calculate_similarity(current, regime)

            similarities.append(
                RegimeSimilarity(
                    current_regime=current.name,
                    historical_regime=regime.name,
                    similarity_score=round(score, 2),
                )
            )

        similarities.sort(
            key=lambda item: item.similarity_score,
            reverse=True,
        )

        return similarities

    def _calculate_similarity(
        self,
        current: MarketRegime,
        historical: MarketRegime,
    ) -> float:
        differences = [
            abs(current.market_health_score - historical.market_health_score),
            abs(current.volatility - historical.volatility),
            abs(current.breadth - historical.breadth),
            abs(current.momentum - historical.momentum),
        ]

        normalized_difference = sum(differences) / (len(differences) * 100)

        similarity = max(0.0, 100 - (normalized_difference * 100))

        return similarity


regime_similarity_engine = RegimeSimilarityEngine()
