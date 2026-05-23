# Probabilistic Softmax Normalization

P37 replaces independent bullish, bearish and neutral scales with a normalized probability distribution.

## Problem

The previous model calculated bullish, bearish and neutral values independently.
In high-risk scenarios, bullish plus bearish could exceed 100 and neutral was clamped to zero.
That created pseudo-probabilities rather than a real distribution.

## New Logits

```text
raw_bullish = signal_score * 0.5 + regime_confidence * 0.3 - risk_score * 0.1
raw_bearish = risk_score * 0.6 + max(0, 50 - regime_confidence) * 0.2
raw_neutral = 50 - abs(raw_bullish - raw_bearish) * 0.3
```

Inputs are clamped to the 0..100 range before logits are calculated.

## Softmax

The logits are divided by temperature 20 and normalized with numerically stable softmax.

```text
max_logit = max(scaled_logits)
exp_i = exp(scaled_logit_i - max_logit)
prob_i = exp_i / sum(exp_values) * 100
```

This avoids overflow and guarantees a valid probability distribution.

## Invariants

```text
bullish_probability >= 0
bearish_probability >= 0
neutral_probability >= 0
bullish + bearish + neutral = 100
classification follows the highest probability
```

## Implementation

```text
src/decision/probabilistic_decision_engine.py
tests/test_probabilistic_decisions.py
```

## Test Command

```bash
pytest tests/test_probabilistic_decisions.py
```

## Boundary

P37 improves decision-support probability consistency only.
It does not add broker connectivity or order execution.
