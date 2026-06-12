# Numeric Coercion Contract #199

Status date: 2026-06-12

## Purpose

Numeric conversion must be consistent across active scoring, validation and signal-normalization paths.

## Canonical helpers

The canonical helpers live in:

```text
src/validation/historical_edge_validation.py
```

Public helpers:

```text
coerce_finite_float(value, strict=False)
coerce_finite_float_or_default(value, default)
json_safe_number(value, fallback=None)
NumericCoercionResult
```

## Semantics

```text
None -> missing
empty string -> missing
numeric string -> finite float
invalid string -> invalid_float
NaN -> non_finite
Inf -> non_finite
-Inf -> non_finite
Decimal-like values -> finite float when convertible
```

## Active migrated paths

```text
src/validation/historical_edge_validation.py
src/signals/scanner_metrics_pipeline.py
src/scoring/setup_score_engine.py
```

## Guard tests

```text
tests/test_199_numeric_coercion_contract.py
```
