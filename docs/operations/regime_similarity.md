# P38: Regime Similarity Weighted Distance + Cosine Similarity

## Purpose

P38 replaces the previous unweighted regime similarity calculation with a weighted, normalized distance model plus a directional cosine similarity component.

The goal is to make regime comparisons more realistic for decision-support workflows. Volatility/VIX-style changes should have stronger impact than equally sized breadth or momentum changes.

## Inputs

A regime vector uses four fields:

```text
market_health_score  0..100
volatility           VIX-style value, capped at 80
breadth              0..100
momentum             -100..100
```

## Normalization

```text
health_norm     = clamp(market_health_score, 0, 100) / 100
volatility_norm = clamp(volatility, 0, 80) / 80
breadth_norm    = clamp(breadth, 0, 100) / 100
momentum_norm   = (clamp(momentum, -100, 100) + 100) / 200
```

## Weighted Distance

```text
volatility  0.40
health      0.25
breadth     0.20
momentum    0.15
```

```text
weighted_distance = sqrt(
  w_volatility * (current_volatility - historical_volatility)^2
+ w_health     * (current_health - historical_health)^2
+ w_breadth    * (current_breadth - historical_breadth)^2
+ w_momentum   * (current_momentum - historical_momentum)^2
)
```

## Distance Similarity

```text
distance_similarity = max(0, 100 - weighted_distance * sqrt(2) * 100)
```

## Cosine Similarity

Cosine similarity measures whether two regime vectors point in a similar direction. It is used as a secondary component, not as the main metric.

```text
cosine_similarity = dot(current, historical) / (|current| * |historical|)
```

Zero-vector cases return `0.0` instead of raising or producing invalid output.

## Final Score

```text
similarity_score = distance_similarity * 0.70 + cosine_similarity * 0.30
similarity_score = clamp(similarity_score, 0, 100)
```

## Output

The public `similarity_score` remains compatible with existing consumers.

Additional diagnostic fields are included:

```text
distance_similarity_score
cosine_similarity_score
weighted_distance
```

## Tests

```bash
pytest tests/test_regime_similarity_engine.py
```

## Guardrails

This module is for decision-support analysis only.

It does not:

- place orders
- connect to a broker
- authorize live trading
- prove a trading edge by itself
