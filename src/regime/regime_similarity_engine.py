from __future__ import annotations

import math
from dataclasses import dataclass


VOLATILITY_CAP = 80.0
MOMENTUM_FLOOR = -100.0
MOMENTUM_CEILING = 100.0
DISTANCE_NORMALIZATION_FACTOR = math.sqrt(2) * 100
DISTANCE_SIMILARITY_WEIGHT = 0.70
COSINE_SIMILARITY_WEIGHT = 0.30

REGIME_DISTANCE_WEIGHTS = {
    "volatility": 0.40,
    "market_health_score": 0.25,
    "breadth": 0.20,
    "momentum": 0.15,
}


@dataclass(frozen=True)
class MarketRegime:
    name: str
    market_health_score: float
    volatility: float
    breadth: float
    momentum: float


@dataclass(frozen=True)
class NormalizedRegimeVector:
    market_health_score: float
    volatility: float
    breadth: float
    momentum: float

    def as_ordered_tuple(self) -> tuple[float, float, float, float]:
        return (
            self.volatility,
            self.market_health_score,
            self.breadth,
            self.momentum,
        )


@dataclass(frozen=True)
class RegimeSimilarity:
    current_regime: str
    historical_regime: str
    similarity_score: float
    distance_similarity_score: float = 0.0
    cosine_similarity_score: float = 0.0
    weighted_distance: float = 0.0


class RegimeSimilarityEngine:
    def compare(
        self,
        current: MarketRegime,
        historical: list[MarketRegime],
    ) -> list[RegimeSimilarity]:
        similarities: list[RegimeSimilarity] = []

        for regime in historical:
            score = self._calculate_similarity(current, regime)
            distance_similarity = self._calculate_distance_similarity(current, regime)
            cosine_similarity = self._calculate_cosine_similarity(current, regime)
            weighted_distance = self._calculate_weighted_distance(current, regime)

            similarities.append(
                RegimeSimilarity(
                    current_regime=current.name,
                    historical_regime=regime.name,
                    similarity_score=round(score, 2),
                    distance_similarity_score=round(distance_similarity, 2),
                    cosine_similarity_score=round(cosine_similarity, 2),
                    weighted_distance=round(weighted_distance, 4),
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
        distance_similarity = self._calculate_distance_similarity(current, historical)
        cosine_similarity = self._calculate_cosine_similarity(current, historical)

        similarity = (
            distance_similarity * DISTANCE_SIMILARITY_WEIGHT
            + cosine_similarity * COSINE_SIMILARITY_WEIGHT
        )

        return self._clamp(similarity, 0.0, 100.0)

    def _calculate_distance_similarity(
        self,
        current: MarketRegime,
        historical: MarketRegime,
    ) -> float:
        weighted_distance = self._calculate_weighted_distance(current, historical)
        similarity = max(
            0.0,
            100.0 - (weighted_distance * DISTANCE_NORMALIZATION_FACTOR),
        )
        return self._clamp(similarity, 0.0, 100.0)

    def _calculate_weighted_distance(
        self,
        current: MarketRegime,
        historical: MarketRegime,
    ) -> float:
        current_vector = normalize_regime_vector(current)
        historical_vector = normalize_regime_vector(historical)

        weighted_squared_distance = (
            REGIME_DISTANCE_WEIGHTS["volatility"]
            * (current_vector.volatility - historical_vector.volatility) ** 2
            + REGIME_DISTANCE_WEIGHTS["market_health_score"]
            * (
                current_vector.market_health_score
                - historical_vector.market_health_score
            )
            ** 2
            + REGIME_DISTANCE_WEIGHTS["breadth"]
            * (current_vector.breadth - historical_vector.breadth) ** 2
            + REGIME_DISTANCE_WEIGHTS["momentum"]
            * (current_vector.momentum - historical_vector.momentum) ** 2
        )

        return math.sqrt(weighted_squared_distance)

    def _calculate_cosine_similarity(
        self,
        current: MarketRegime,
        historical: MarketRegime,
    ) -> float:
        current_vector = normalize_regime_vector(current).as_ordered_tuple()
        historical_vector = normalize_regime_vector(historical).as_ordered_tuple()

        dot_product = sum(
            current_value * historical_value
            for current_value, historical_value in zip(current_vector, historical_vector)
        )
        current_norm = math.sqrt(sum(value**2 for value in current_vector))
        historical_norm = math.sqrt(sum(value**2 for value in historical_vector))

        if current_norm == 0.0 or historical_norm == 0.0:
            return 0.0

        cosine = dot_product / (current_norm * historical_norm)
        return self._clamp(cosine * 100.0, 0.0, 100.0)

    @staticmethod
    def _clamp(value: float, minimum: float, maximum: float) -> float:
        return max(minimum, min(maximum, value))


def normalize_regime_vector(regime: MarketRegime) -> NormalizedRegimeVector:
    market_health_score = _clamp(regime.market_health_score, 0.0, 100.0) / 100.0
    volatility = _clamp(regime.volatility, 0.0, VOLATILITY_CAP) / VOLATILITY_CAP
    breadth = _clamp(regime.breadth, 0.0, 100.0) / 100.0
    momentum = (
        _clamp(regime.momentum, MOMENTUM_FLOOR, MOMENTUM_CEILING) + 100.0
    ) / 200.0

    return NormalizedRegimeVector(
        market_health_score=market_health_score,
        volatility=volatility,
        breadth=breadth,
        momentum=momentum,
    )


def _clamp(value: float, minimum: float, maximum: float) -> float:
    return max(minimum, min(maximum, value))


regime_similarity_engine = RegimeSimilarityEngine()
