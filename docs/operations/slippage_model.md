# Square-Root Slippage Model

The execution cost model now separates spread cost from market impact and uses a regime-aware square-root impact estimate.

## Implementation

```text
src/execution/slippage_model.py
src/validation/execution_realism.py
tests/test_slippage_model.py
tests/test_execution_realism.py
```

## Model

Inputs and outputs are percentages, not decimals.

```text
spread_cost = spread_percent / 2 * spread_multiplier
raw_impact = volatility_percent * sqrt(order_size_percent_adv / 100) * impact_coefficient
market_impact = raw_impact * regime_multiplier
total_slippage = spread_cost + market_impact
```

The default model version is:

```text
sqrt-impact-v1
```

## Why this exists

The previous model was a linear heuristic. A linear model underestimates execution pain when order size grows relative to average daily volume and when markets enter stressed regimes.

The new model is still conservative and intentionally simple, but it captures three critical realities:

1. order-size impact is non-linear
2. panic/risk-off regimes amplify market impact
3. spread cost and impact cost are different components

## Default regime multipliers

| Regime | Multiplier |
|---|---:|
| low_vol_bull | 1.0 |
| normal | 1.0 |
| neutral | 1.1 |
| high_vol | 1.4 |
| high_vol_transition | 1.5 |
| volatile | 1.6 |
| risk_off | 2.0 |
| panic | 3.0 |
| panic_dislocation | 3.5 |

Unknown regimes fall back to the neutral multiplier.

## Quality buckets

| Bucket | Total slippage percent |
|---|---:|
| excellent | <= 0.05 |
| acceptable | <= 0.20 |
| poor | <= 0.50 |
| prohibitive | > 0.50 |

## Execution realism integration

`apply_execution_realism` and `adjust_execution_record` now record:

```text
slippage_model_version
slippage_quality
market_impact_pct
spread_cost_pct
slippage_pct
execution_cost_r
```

Records can provide market-specific inputs:

```text
volatility_percent / daily_volatility_percent / atr_percent
spread_percent / bid_ask_spread_percent
order_size_percent_adv / order_size_pct_adv / percent_adv
```

If those fields are missing, conservative defaults are used.

## Operational rule

If a trade becomes `poor` or `prohibitive` under the slippage model, it should be reviewed before being treated as executable edge.

Future work should connect this model to real fill-quality reports once broker paper execution is introduced.
