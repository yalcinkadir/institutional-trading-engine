# Decision Quality and Validation Roadmap P36-P47

This roadmap has two stages:

```text
P36-P40: make the decision layer mathematically cleaner
P41-P47: prove or reject the trading edge before any live-capital decision
```

## P36 Confidence Score Double Counting Fix

Status: completed.

Formula:

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

Status: implemented, verification pending.

Goal:

```text
Measure whether a positive historical edge exists after costs and risk constraints.
```

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

Default gates:

```text
MIN_TOTAL_TRADES     = 300
MIN_PROFIT_FACTOR    = 1.4
MIN_EXPECTANCY_R     = 0.5
MAX_DRAWDOWN_LIMIT   = 0.25
MIN_SHARPE_RATIO     = 0.8
```

## P42 Regime-Phase Backtest Matrix

Status: planned.

Goal:

```text
Evaluate the system across multiple market phases instead of one blended period.
```

Required phases:

```text
Low-Vol Bull       2019-01 to 2020-02
Panic/Dislocation  2020-03 to 2020-04
Recovery           2020-05 to 2021-12
High-Vol Regime    2022-01 to 2022-12
Neutral/Transition 2023-01 to 2024-06
```

## P43 Walk-Forward Validation

Status: planned.

Target structure:

```text
training window 18 months
test window      6 months
step size        3 months
minimum cycles   6
```

## P44 Execution Realism Layer

Status: planned.

Initial assumptions:

```text
spread cost normal regime: 0.05%
slippage normal regime:    0.10%
slippage volatile regime:  0.30%
```

## P45 Out-of-Sample Validation Lockbox

Status: planned.

Target split:

```text
in-sample:      before 2024-01
out-of-sample:  2024-01 onward
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
