# P40: MultiFactorFusion Recalibration

## Purpose

P40 recalibrates the multi-factor fusion layer by separating opportunity from risk.

The old formula mixed positive and negative terms in one expression. The new model makes the positive opportunity score and the negative risk penalty visible independently.

## Opportunity Score

Opportunity weights sum to exactly `1.0`:

```text
regime_score          0.30
feature_alpha_score   0.30
execution_confidence  0.20
liquidity_score       0.20
```

```text
opportunity_score =
  regime_score * 0.30
+ feature_alpha_score * 0.30
+ execution_confidence * 0.20
+ liquidity_score * 0.20
```

The implementation returns `opportunity_score` on a 0..1 scale and `opportunity_points` on a 0..100 scale.

## Risk Penalty

Risk is handled separately:

```text
tail_risk_score      * 0.20
portfolio_risk_score * 0.10
```

The risk penalty is capped at 30 points.

```text
risk_penalty = min(30, tail_risk_score * 0.20 + portfolio_risk_score * 0.10)
```

## Final Fusion Score

```text
fusion_score = clamp(opportunity_points - risk_penalty, 0, 100)
```

## Regime Gate

Weak regime context caps the score:

```text
if regime_score < 20:
    fusion_score = min(fusion_score, 40)
```

This prevents strong asset-level or execution inputs from hiding a poor regime backdrop.

## Diagnostics

`FusionDecision` includes:

```text
fusion_score
confidence
classification
reasoning
opportunity_score
opportunity_points
risk_penalty
regime_gate_applied
regime_gate_cap
normalized_inputs
```

## Tests

```bash
pytest tests/test_multi_factor_fusion.py
```

## Guardrails

This module is for decision-support scoring only.

It does not:

- place orders
- connect to a broker
- authorize live trading
- prove an edge by itself
