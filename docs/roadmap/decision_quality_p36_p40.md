# Decision Quality and Validation Roadmap P36-P47

This roadmap has two stages:

```text
P36-P40: make the decision layer mathematically cleaner
P41-P47: prove or reject the trading edge before any live-capital decision
```

## P36 Confidence Score Double Counting Fix

Status: completed.

Goal:

```text
Remove structural double counting in confidence scoring.
```

Formula:

```text
confidence = setup_score * 0.45 + market_health_score * 0.35 + regime_alignment_score * 0.20
```

Regime alignment mapping:

```text
Tier 1   100
Tier 2    65
Tier 3    35
No Trade   0
```

## P37 Probabilistic Engine Softmax Normalization

Status: completed.

Goal:

```text
Convert bullish, bearish and neutral outputs into a valid probability distribution.
```

Implementation:

```text
raw_bullish = signal_score * 0.5 + regime_confidence * 0.3 - risk_score * 0.1
raw_bearish = risk_score * 0.6 + max(0, 50 - regime_confidence) * 0.2
raw_neutral = 50 - abs(raw_bullish - raw_bearish) * 0.3
```

The raw logits are normalized through numerically stable softmax with temperature 20.

Acceptance:

```text
bullish + bearish + neutral = 100
no negative probabilities
high risk dominates bearish output
high signal with low risk and strong regime dominates bullish output
classification follows the dominant probability
```

## P38 Regime Similarity Weighted Distance + Cosine Similarity

Status: implemented, verification pending.

Goal:

```text
Replace unweighted similarity with weighted normalized distance and cosine similarity.
```

Implemented weights:

```text
volatility 0.40
health     0.25
breadth    0.20
momentum   0.15
```

Final score:

```text
similarity_score = distance_similarity * 0.70 + cosine_similarity * 0.30
```

Diagnostics:

```text
distance_similarity_score
cosine_similarity_score
weighted_distance
```

## P39 Adaptive Feedback Decay

Status: planned.

Goal:

```text
Weight recent trades more strongly than old trades.
```

Planned constants:

```text
DECAY_HALF_LIFE_STABLE = 30
DECAY_HALF_LIFE_REGIME_SHIFT = 10
REGIME_SHIFT_RECOVERY_DAYS = 5
MIN_WEIGHT_FLOOR = 0.05
```

## P40 MultiFactorFusion Recalibration

Status: planned.

Goal:

```text
Separate opportunity score from risk penalty.
```

Planned opportunity weights:

```text
regime_score          0.30
feature_alpha_score   0.30
execution_confidence  0.20
liquidity_score       0.20
```

Planned risk penalty:

```text
tail_risk_score      0.20
portfolio_risk_score 0.10
```

Planned regime gate:

```text
if regime_score < 20:
    fusion_score = min(fusion_score, 40)
```

---

# Validation Roadmap After P40

## P41 Historical Edge Validation Framework

Goal:

```text
Measure whether a positive historical edge exists after costs and risk constraints.
```

Target metrics:

```text
win rate
expectancy in R
profit factor
max drawdown
Sharpe ratio
consecutive losses
recovery time from drawdown
```

## P42 Regime-Phase Backtest Matrix

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

Goal:

```text
Reduce overfitting risk by separating development windows from forward test windows.
```

Target structure:

```text
training window 18 months
test window      6 months
step size        3 months
minimum cycles   6
```

## P44 Execution Realism Layer

Goal:

```text
Apply spread, slippage and execution assumptions before validating edge.
```

Initial assumptions:

```text
spread cost normal regime: 0.05%
slippage normal regime:    0.10%
slippage volatile regime:  0.30%
```

## P45 Out-of-Sample Validation Lockbox

Goal:

```text
Protect out-of-sample data from accidental rule tuning and measure degradation honestly.
```

Target split:

```text
in-sample:      before 2024-01
out-of-sample:  2024-01 onward
```

Acceptance idea:

```text
OOS keeps at least 80% of in-sample core metrics.
```

## P46 Paper Trading Journal / Live Observation v2

Goal:

```text
Track live paper signals, theoretical fills, realistic fills, slippage and rule-following behavior.
```

Minimum duration:

```text
3 months absolute minimum
6 months if no meaningful regime shift occurs
```

## P47 Final Live Readiness Gate

Goal:

```text
Create a final decision gate before any real-capital exposure is considered.
```

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
