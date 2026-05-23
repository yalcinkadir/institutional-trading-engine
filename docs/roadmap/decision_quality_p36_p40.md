# Decision Quality Roadmap P36-P40

This roadmap focuses on mathematical and logical quality improvements in the decision layer.

## P36 Confidence Score Double Counting Fix

Status: implemented, verification pending.

Goal:

```text
Remove structural double counting in confidence scoring.
```

Target structure:

```text
asset setup score      weight 0.45
market health score   weight 0.35
regime alignment      weight 0.20
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

Goal:

```text
Convert bullish, bearish and neutral outputs into a valid probability distribution.
```

Acceptance:

```text
bullish + bearish + neutral = 100
no negative probabilities
classification follows the dominant probability
```

## P38 Regime Similarity Weighted Distance

Goal:

```text
Replace unweighted similarity with weighted distance and cosine similarity.
```

Planned weights:

```text
volatility 0.40
health     0.25
breadth    0.20
momentum   0.15
```

## P39 Adaptive Feedback Decay

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

## Boundary

These tasks improve decision-support quality only.

They do not add broker connectivity or order execution.
