# Monte Carlo Robustness Suite

Phase B6 adds a deterministic Monte Carlo robustness suite for evidence-quality review.

The goal is to reduce the chance that a promising result is only a lucky path, a fragile order of outcomes or an unstable small-sample artifact.

## Inputs

The robustness suite accepts numeric R values or dictionaries containing:

```text
result_r
r_multiple
paper_r
```

## Methods

The suite runs three robustness checks:

```text
Bootstrap resampling
Permutation / sign-randomization test
Shuffled-path drawdown simulation
```

Bootstrap resampling estimates confidence intervals for expectancy and total R.

Permutation testing estimates how unusual the observed total R is relative to randomized signs.

Shuffled-path drawdown simulation estimates drawdown tail risk under different ordering of the same outcomes.

## Metrics

The report calculates:

```text
observations
simulations
confidence_level
observed_expectancy_r
observed_total_r
observed_win_rate
bootstrap_expectancy_lower_r
bootstrap_expectancy_upper_r
bootstrap_total_lower_r
bootstrap_total_upper_r
permutation_p_value
drawdown_p95_r
drawdown_p99_r
```

## Gates

Default fail-closed gates:

```text
min_observations = 30
min_bootstrap_expectancy_lower_r = 0.0
max_drawdown_p95_r = 10.0
min_permutation_p_value = 0.05
require_positive_observed_expectancy = true
```

## Outputs

The module can write:

```text
monte_carlo_robustness.json
monte_carlo_robustness.md
```

## Operational Rule

Monte Carlo robustness is an evidence-quality gate. A pass does not approve live capital. A failure means the observed edge should be treated as fragile until more evidence is collected or the underlying setup is improved.
