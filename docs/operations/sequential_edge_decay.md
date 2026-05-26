# Sequential Edge Decay Test

Phase B3 adds a sequential edge-decay check for forward paper observations.

The goal is to detect whether the observed forward stream is still compatible with the baseline edge or whether the degraded-edge hypothesis should be accepted.

## Method

The module uses a Sequential Probability Ratio Test style log-likelihood ratio on win/loss outcomes.

Configured hypotheses:

```text
baseline_win_rate = 0.55
degraded_win_rate = 0.45
alpha = 0.05
beta = 0.20
```

Interpretation:

```text
accept_baseline_edge       forward stream is compatible with baseline
accept_degraded_edge       degraded-edge hypothesis accepted
continue_observation       more observations are needed
inconclusive_max_observations reached max sample without a conclusion
```

## Inputs

The detector accepts numeric R values or dictionaries containing:

```text
result_r
r_multiple
paper_r
```

Positive R values count as wins. Negative R values count as losses. Zero values are treated as breakeven and do not affect the win/loss likelihood ratio.

## Gates

Default gates:

```text
min_observations = 20
require_positive_expectancy = true
no_degraded_edge_decision
```

The report fails if the degraded-edge hypothesis is accepted.

## Outputs

The module can write:

```text
sequential_edge_decay.json
sequential_edge_decay.md
```

## Operational Rule

This is an evidence-quality gate only. A pass does not approve live capital. A degraded-edge decision means observation should continue under review and escalation must be blocked.
