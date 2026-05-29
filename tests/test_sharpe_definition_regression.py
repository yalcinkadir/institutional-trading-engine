import math

from src.validation.historical_edge_validation import (
    SHARPE_DEFINITION_VERSION,
    calculate_historical_edge_metrics,
    calculate_sharpe_ratio,
    calculate_sharpe_tstat,
)


def test_sharpe_is_sample_size_independent() -> None:
    """Doubling the same distribution must not change Sharpe."""
    base = [1.0, -1.0, 2.0, -0.5, 1.5, -1.0]
    doubled = base * 2

    s1 = calculate_sharpe_ratio(base)
    s2 = calculate_sharpe_ratio(doubled)

    assert math.isclose(s1, s2, rel_tol=1e-9), (
        f"Sharpe changed with sample size: {s1} vs {s2} — still a t-stat?"
    )


def test_per_trade_sharpe_is_in_realistic_range() -> None:
    values = [0.5, -1.0, 1.5, -1.0, 2.0, -1.0, 1.0, -0.5]

    sharpe = calculate_sharpe_ratio(values)

    assert -2.0 < sharpe < 2.0


def test_tstat_grows_with_sample_size() -> None:
    base = [1.0, -1.0, 2.0, -0.5, 1.5, -1.0]

    assert calculate_sharpe_tstat(base * 4) > calculate_sharpe_tstat(base)


def test_metrics_sharpe_matches_per_trade_definition() -> None:
    values = [0.5, -1.0, 1.5, -1.0, 2.0]

    metrics = calculate_historical_edge_metrics(values)

    assert math.isclose(metrics.sharpe_ratio, round(calculate_sharpe_ratio(values), 6))
    assert math.isclose(metrics.sharpe_tstat, round(calculate_sharpe_tstat(values), 6))
    assert metrics.sharpe_definition_version == SHARPE_DEFINITION_VERSION
