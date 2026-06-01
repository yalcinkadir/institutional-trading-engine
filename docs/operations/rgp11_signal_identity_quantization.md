# RGP11 Signal Identity Quantization

Status date: 2026-06-01

## Purpose

RGP11 prevents signal identity drift caused by float/string representation noise in price-like identity fields.

Examples that should produce the same identity:

```text
101
101.0
101.00000001
```

## Implemented guard

Signal identity price fields are normalized only inside the identity payload before hashing.

Affected identity fields:

```text
entry_trigger
stop_loss
target_1
target_2
```

The original signal payload is not mutated.

## Updated code

```text
src/signals/signal_identity.py
```

## Regression coverage

```text
tests/test_rgp11_signal_identity_quantization.py
```

Coverage includes:

- equivalent numeric/string price representations generate the same signal id
- material price changes still generate different signal ids
- source signal values are not mutated by identity normalization
- symbol/action case is normalized for identity stability

## Live trading authorization

RGP11 does not authorize live trading. It only hardens research/paper lifecycle identity stability.
