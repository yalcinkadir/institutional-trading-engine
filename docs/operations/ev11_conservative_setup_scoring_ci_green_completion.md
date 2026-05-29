# EV11 Conservative Setup Scoring CI-Green Completion

Status date: 2026-05-29

## Result

EV11 conservative missing-indicator setup scoring remediation is confirmed CI-green.

```text
Conservative long-horizon trend fallback: implemented
Conservative long-horizon asymmetry fallback: implemented
Invalid close data audit note: implemented
Targeted EV11 regression tests: passed
Main CI: green
Live trading authorization: unchanged; not granted by code
```

## Completed scope

### EV11 — Missing indicator fallbacks must not be optimistic

Before EV11, setups with partial but insufficient long-horizon history could receive optimistic fallback component scores:

```text
trend_quality = 0.3
asymmetry = 0.4
```

EV11 changes this to conservative scoring:

```text
trend_quality = 0.0
asymmetry_score = 0.0
data_confidence <= 0.5
```

### Audit notes

When long-horizon inputs are missing, setup scoring now records explicit audit notes:

```text
conservative_missing_long_horizon_trend
conservative_missing_long_horizon_asymmetry
missing_or_invalid_close_data
```

## Regression coverage

```text
tests/test_setup_scoring.py
```

Added EV11 regression cases:

```text
test_ev11_missing_long_horizon_indicators_are_conservative_not_optimistic
test_ev11_invalid_close_values_do_not_create_optimistic_scores
```

## CI coverage

The main CI workflow includes a dedicated EV11 regression step:

```text
pytest tests/test_setup_scoring.py -q
```

## Operational boundary

This fix improves scoring conservatism and auditability. It does not prove trading edge, enable broker execution, authorize live trading, replace the 3-6 month paper-observation period, or approve real-money deployment.

## Next block

The next recommended remediation is one of:

```text
EV8 walk-forward naming / train-test semantics clarification
EV12 drawdown-source magnitude validation
```
