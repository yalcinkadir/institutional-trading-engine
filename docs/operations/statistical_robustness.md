# Statistical Robustness Validation

Historical edge validation now includes Deflated Sharpe probability and bootstrap confidence intervals.

## Implementation

```text
src/validation/statistical_robustness.py
src/validation/historical_edge_validation.py
tests/test_statistical_robustness.py
tests/test_historical_edge_validation.py
```

## Why this exists

A normal Sharpe ratio can be misleading when many strategy variants, setup filters or thresholds were tested. Multiple testing increases the chance of selecting a lucky backtest. Small samples also make expectancy unstable.

This layer adds two controls:

1. Deflated Sharpe probability
2. Bootstrap confidence intervals for expectancy and win rate

## Deflated Sharpe probability

The deflated Sharpe probability adjusts the observed Sharpe for:

- number of estimated trials
- number of observations
- skewness
- kurtosis

The default gate requires:

```text
min_deflated_sharpe_probability = 0.95
```

For exploratory testing this can be relaxed through `HistoricalEdgeValidationConfig`, but production evidence should keep the strict threshold.

## Bootstrap confidence intervals

The validator emits deterministic bootstrap intervals for:

```text
expectancy_r
win_rate
```

Configurable fields:

```text
bootstrap_iterations
bootstrap_confidence_level
bootstrap_seed
require_positive_expectancy_ci_lower_bound
```

When `require_positive_expectancy_ci_lower_bound=True`, the historical edge report fails unless the lower confidence bound of expectancy is above zero.

## Report output

Historical edge reports now include:

```text
statistical_robustness.deflated_sharpe_probability
statistical_robustness.estimated_trials
statistical_robustness.observations
statistical_robustness.skewness
statistical_robustness.kurtosis
statistical_robustness.expectancy_ci
statistical_robustness.win_rate_ci
```

Markdown reports include a `Statistical Robustness` section.

## Operational rule

Do not treat an apparently strong backtest as evidence if:

- deflated Sharpe probability fails
- expectancy CI lower bound is not positive under strict validation
- the sample size is small
- the number of hidden strategy trials is unknown

If the number of trials is unknown, use a conservative estimate rather than pretending only one strategy was tested.
