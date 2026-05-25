from __future__ import annotations

import math
import random
from dataclasses import asdict, dataclass
from statistics import NormalDist
from typing import Iterable


@dataclass(frozen=True)
class BootstrapConfidenceInterval:
    metric: str
    lower: float
    upper: float
    confidence_level: float
    iterations: int
    seed: int

    def to_dict(self) -> dict[str, float | int | str]:
        return asdict(self)


@dataclass(frozen=True)
class StatisticalRobustnessMetrics:
    deflated_sharpe_probability: float
    estimated_trials: int
    observations: int
    skewness: float
    kurtosis: float
    expectancy_ci: BootstrapConfidenceInterval
    win_rate_ci: BootstrapConfidenceInterval

    def to_dict(self) -> dict[str, object]:
        return {
            "deflated_sharpe_probability": self.deflated_sharpe_probability,
            "estimated_trials": self.estimated_trials,
            "observations": self.observations,
            "skewness": self.skewness,
            "kurtosis": self.kurtosis,
            "expectancy_ci": self.expectancy_ci.to_dict(),
            "win_rate_ci": self.win_rate_ci.to_dict(),
        }


def calculate_statistical_robustness(
    values: Iterable[float],
    *,
    observed_sharpe: float,
    estimated_trials: int = 1,
    bootstrap_iterations: int = 1000,
    confidence_level: float = 0.95,
    seed: int = 7,
) -> StatisticalRobustnessMetrics:
    samples = [float(value) for value in values]
    skewness = calculate_skewness(samples)
    kurtosis = calculate_kurtosis(samples)
    deflated_probability = deflated_sharpe_probability(
        observed_sharpe=observed_sharpe,
        n_trials=estimated_trials,
        n_observations=len(samples),
        skewness=skewness,
        kurtosis=kurtosis,
    )
    return StatisticalRobustnessMetrics(
        deflated_sharpe_probability=round(deflated_probability, 6),
        estimated_trials=max(1, int(estimated_trials)),
        observations=len(samples),
        skewness=round(skewness, 6),
        kurtosis=round(kurtosis, 6),
        expectancy_ci=bootstrap_confidence_interval(
            samples,
            metric="expectancy_r",
            reducer=_mean,
            iterations=bootstrap_iterations,
            confidence_level=confidence_level,
            seed=seed,
        ),
        win_rate_ci=bootstrap_confidence_interval(
            samples,
            metric="win_rate",
            reducer=_win_rate,
            iterations=bootstrap_iterations,
            confidence_level=confidence_level,
            seed=seed + 1,
        ),
    )


def deflated_sharpe_probability(
    *,
    observed_sharpe: float,
    n_trials: int,
    n_observations: int,
    skewness: float = 0.0,
    kurtosis: float = 3.0,
) -> float:
    """Return the probability that Sharpe remains significant after deflation.

    This follows the Bailey/Lopez de Prado intuition: the observed Sharpe is
    compared against the expected maximum Sharpe achievable by chance after
    multiple strategy trials and adjusted for non-normality.
    """

    if n_observations < 2:
        return 0.0

    trials = max(1, int(n_trials))
    if trials == 1:
        expected_max_sharpe = 0.0
    else:
        normal = NormalDist()
        euler_mascheroni = 0.5772156649
        expected_max_sharpe = (
            (1.0 - euler_mascheroni) * normal.inv_cdf(1.0 - 1.0 / trials)
            + euler_mascheroni * normal.inv_cdf(1.0 - 1.0 / (trials * math.e))
        )

    variance = (
        1.0
        - skewness * observed_sharpe
        + ((kurtosis - 1.0) / 4.0) * observed_sharpe**2
    ) / max(1, n_observations - 1)
    std_error = math.sqrt(max(variance, 1e-12))
    z_score = (observed_sharpe - expected_max_sharpe) / std_error
    return NormalDist().cdf(z_score)


def bootstrap_confidence_interval(
    values: Iterable[float],
    *,
    metric: str,
    reducer,
    iterations: int = 1000,
    confidence_level: float = 0.95,
    seed: int = 7,
) -> BootstrapConfidenceInterval:
    samples = [float(value) for value in values]
    iterations = max(1, int(iterations))
    confidence_level = min(0.999, max(0.50, float(confidence_level)))

    if not samples:
        return BootstrapConfidenceInterval(
            metric=metric,
            lower=0.0,
            upper=0.0,
            confidence_level=confidence_level,
            iterations=iterations,
            seed=seed,
        )

    rng = random.Random(seed)
    estimates: list[float] = []
    for _ in range(iterations):
        draw = [samples[rng.randrange(len(samples))] for _ in samples]
        estimates.append(float(reducer(draw)))

    estimates.sort()
    alpha = 1.0 - confidence_level
    lower_index = _quantile_index(len(estimates), alpha / 2.0)
    upper_index = _quantile_index(len(estimates), 1.0 - alpha / 2.0)

    return BootstrapConfidenceInterval(
        metric=metric,
        lower=round(estimates[lower_index], 6),
        upper=round(estimates[upper_index], 6),
        confidence_level=confidence_level,
        iterations=iterations,
        seed=seed,
    )


def calculate_skewness(values: Iterable[float]) -> float:
    samples = [float(value) for value in values]
    if len(samples) < 3:
        return 0.0
    mean = _mean(samples)
    std = _sample_std(samples)
    if std == 0:
        return 0.0
    n = len(samples)
    return (n / ((n - 1) * (n - 2))) * sum(((value - mean) / std) ** 3 for value in samples)


def calculate_kurtosis(values: Iterable[float]) -> float:
    samples = [float(value) for value in values]
    if len(samples) < 4:
        return 3.0
    mean = _mean(samples)
    std = _sample_std(samples)
    if std == 0:
        return 3.0
    n = len(samples)
    excess = (
        (n * (n + 1)) / ((n - 1) * (n - 2) * (n - 3))
        * sum(((value - mean) / std) ** 4 for value in samples)
        - (3 * (n - 1) ** 2) / ((n - 2) * (n - 3))
    )
    return excess + 3.0


def _mean(values: Iterable[float]) -> float:
    samples = [float(value) for value in values]
    return sum(samples) / len(samples) if samples else 0.0


def _win_rate(values: Iterable[float]) -> float:
    samples = [float(value) for value in values]
    return sum(1 for value in samples if value > 0) / len(samples) if samples else 0.0


def _sample_std(values: Iterable[float]) -> float:
    samples = [float(value) for value in values]
    if len(samples) < 2:
        return 0.0
    mean = _mean(samples)
    variance = sum((value - mean) ** 2 for value in samples) / (len(samples) - 1)
    return math.sqrt(variance)


def _quantile_index(length: int, quantile: float) -> int:
    return min(length - 1, max(0, int(round((length - 1) * quantile))))
