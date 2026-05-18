from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.exposure_correlation_engine import (  # noqa: E402
    ExposurePosition,
    evaluate_exposure_correlation,
)


def test_exposure_engine_detects_clustered_risk():
    shared_returns = tuple([0.01, 0.02, 0.015, 0.03, 0.025, 0.01])

    result = evaluate_exposure_correlation(
        [
            ExposurePosition(
                symbol="NVDA",
                sector="Technology",
                factor_tags=("ai", "momentum", "growth"),
                weight=0.28,
                beta=1.6,
                volatility_20d=0.09,
                returns_20d=shared_returns,
            ),
            ExposurePosition(
                symbol="AMD",
                sector="Technology",
                factor_tags=("ai", "momentum", "growth"),
                weight=0.24,
                beta=1.5,
                volatility_20d=0.085,
                returns_20d=shared_returns,
            ),
            ExposurePosition(
                symbol="MU",
                sector="Technology",
                factor_tags=("ai", "memory", "growth"),
                weight=0.20,
                beta=1.4,
                volatility_20d=0.08,
                returns_20d=shared_returns,
            ),
        ]
    )

    assert result.exposure_state in {
        "exposure_correlation_high",
        "exposure_correlation_extreme",
    }
    assert len(result.clusters) > 0


def test_exposure_engine_accepts_diversified_portfolio():
    result = evaluate_exposure_correlation(
        [
            ExposurePosition(
                symbol="XLU",
                sector="Utilities",
                factor_tags=("defensive",),
                weight=0.15,
                beta=0.6,
                volatility_20d=0.02,
                returns_20d=(0.01, 0.0, -0.01, 0.01, 0.0),
            ),
            ExposurePosition(
                symbol="GLD",
                sector="Metals",
                factor_tags=("inflation_hedge",),
                weight=0.15,
                beta=0.3,
                volatility_20d=0.015,
                returns_20d=(0.0, 0.01, 0.0, -0.01, 0.01),
            ),
            ExposurePosition(
                symbol="XLP",
                sector="Staples",
                factor_tags=("defensive", "low_beta"),
                weight=0.12,
                beta=0.5,
                volatility_20d=0.018,
                returns_20d=(-0.01, 0.0, 0.01, 0.0, -0.01),
            ),
        ]
    )

    assert result.exposure_state == "exposure_correlation_contained"
