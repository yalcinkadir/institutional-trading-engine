# Decision Engine Consistency Contract

Status date: 2026-06-12

Issue: #200

## Engines

Canonical decision engine:

```text
src.decision_engine.evaluate_candidate
```

Probabilistic decision engine:

```text
src.decision.probabilistic_decision_engine.probabilistic_decision_engine
```

## Purpose

The two engines do not need identical internals.

They must agree at the documented output boundary when evaluated on the same canonical fixture.

## Exact match field

```text
boundary
```

## Boundary classes

```text
actionable_bullish
watch_or_neutral
defensive_or_blocked
```

## Canonical mapping

```text
approved      -> actionable_bullish
reduced_size  -> actionable_bullish
watch         -> watch_or_neutral
no_trade      -> defensive_or_blocked
blocked       -> defensive_or_blocked
```

## Probabilistic mapping

```text
bullish -> actionable_bullish
neutral -> watch_or_neutral
bearish -> defensive_or_blocked
```

## Allowed differences

The following outputs may differ because the engines have different responsibilities:

```text
confidence_score
probability_distribution
position_size_multiplier
risk_tier
```

## Runtime boundary

A report/orchestration path must not silently treat contradictory engine boundaries as equivalent.

If the canonical engine emits `defensive_or_blocked` while the probabilistic engine emits `actionable_bullish`, the divergence is undocumented and must be blocked by tests.

## Test coverage

Contract tests live in:

```text
tests/test_200_decision_engine_consistency.py
```
