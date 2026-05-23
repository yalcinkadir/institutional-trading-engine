# Decision Quality and Validation Roadmap P36-P47

This roadmap has two stages:

```text
P36-P40: make the decision layer mathematically cleaner
P41-P47: prove or reject the trading edge before any live-capital decision
```

## P36 Confidence Score Double Counting Fix

Status: completed.

```text
confidence = setup_score * 0.45 + market_health_score * 0.35 + regime_alignment_score * 0.20
```

## P37 Probabilistic Engine Softmax Normalization

Status: completed.

```text
bullish + bearish + neutral = 100
classification follows the dominant probability
```

## P38 Regime Similarity Weighted Distance + Cosine Similarity

Status: completed.

```text
similarity_score = distance_similarity * 0.70 + cosine_similarity * 0.30
```

## P39 Adaptive Feedback Decay

Status: completed.

```text
DECAY_HALF_LIFE_STABLE = 30
DECAY_HALF_LIFE_REGIME_SHIFT = 10
REGIME_SHIFT_RECOVERY_DAYS = 5
MIN_WEIGHT_FLOOR = 0.05
```

## P40 MultiFactorFusion Recalibration

Status: completed.

```text
fusion_score = clamp(opportunity_points - risk_penalty, 0, 100)
```

---

# Validation Roadmap After P40

## P41 Historical Edge Validation Framework

Status: completed.

Implemented metrics:

```text
total_trades
win_rate
expectancy_r
profit_factor
max_drawdown
sharpe_ratio
max_consecutive_losses
recovery_time_trades
cumulative_r
```

## P42 Regime-Phase Backtest Matrix

Status: completed.

Implemented phases:

```text
Low-Vol Bull       2019-01-01 to 2020-02-29
Panic/Dislocation  2020-03-01 to 2020-04-30
Recovery           2020-05-01 to 2021-12-31
High-Vol Regime    2022-01-01 to 2022-12-31
Neutral/Transition 2023-01-01 to 2024-06-30
```

## P43 Walk-Forward Validation

Status: completed.

Target structure:

```text
training window 18 months
test window      6 months
step size        3 months
minimum cycles   6
```

## P44 Execution Realism Layer

Status: completed.

Initial assumptions:

```text
spread cost per trade:      0.05%
slippage normal regime:     0.10%
slippage volatile regime:   0.30%
```

Cost conversion:

```text
execution_cost_r = entry_price * (spread_cost_pct + slippage_pct) / abs(entry_price - stop_loss)
adjusted_r = original_r - execution_cost_r
```

## P45 Out-of-Sample Validation Lockbox

Status: implemented, verification pending.

Target split:

```text
in-sample:      before 2024-01-01
out-of-sample:  2024-01-01 onward
```

Degradation gate:

```text
OOS degradation must not exceed 20% for core metrics
```

Compared metrics:

```text
expectancy_r
profit_factor
sharpe_ratio
max_drawdown
```

## P46 Paper Trading Journal / Live Observation v2

Status: planned.

Minimum duration:

```text
3 months absolute minimum
6 months if no meaningful regime shift occurs
```

## P47 Final Live Readiness Gate

Status: planned.

Non-negotiable gates:

```text
validated edge
OOS robustness
paper trading stability
execution cost realism
manual review
kill-switch rules
capital-at-risk limits
```

## Boundary

These tasks improve decision-support and validation quality only.

They do not add broker connectivity or order execution.
