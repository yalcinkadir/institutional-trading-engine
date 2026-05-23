# P39: Adaptive Feedback Decay

## Purpose

P39 adds time-weighted feedback for adaptive decision-support metrics.

Older trades should not have the same influence as recent trades, especially after regime changes. This module introduces exponential decay with configurable half-life settings.

## Constants

```text
DECAY_HALF_LIFE_STABLE = 30
DECAY_HALF_LIFE_REGIME_SHIFT = 10
REGIME_SHIFT_RECOVERY_DAYS = 5
MIN_WEIGHT_FLOOR = 0.05
```

## Decay Formula

```text
weight_i = decay_factor ^ (age_in_days_i / half_life_days)
```

Default:

```text
decay_factor = 0.5
```

Meaning in stable mode:

```text
0 days old   -> 100%
30 days old  -> about 50%
60 days old  -> about 25%
very old     -> never below 5%
```

## Regime-Shift Mode

If a regime shift is active, the half-life is reduced from 30 days to 10 days.

```text
stable mode:       half_life = 30 days
regime-shift mode: half_life = 10 days
```

After `REGIME_SHIFT_RECOVERY_DAYS`, the mode returns to stable half-life.

## Weighted Performance

Weighted performance is calculated as:

```text
weighted_sum = sum(result_i * weight_i)
total_weight = sum(weight_i)
adjusted_performance = weighted_sum / total_weight
```

The default result field is:

```text
result_r
```

The default timestamp field is:

```text
closed_at
```

## Example

```python
from src.feedback.adaptive_feedback_decay import calculate_weighted_performance

records = [
    {"closed_at": "2026-01-31", "result_r": 1.0},
    {"closed_at": "2025-12-03", "result_r": -1.0},
]

performance = calculate_weighted_performance(records, as_of="2026-02-01")
```

## Tests

```bash
pytest tests/test_adaptive_feedback_decay.py
```

## Guardrails

This module is for feedback weighting and decision-support analysis only.

It does not:

- place orders
- connect to a broker
- authorize live trading
- prove an edge by itself
