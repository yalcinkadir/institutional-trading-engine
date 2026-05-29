# EV3-EV6 Backtest Fidelity CI-Green Completion

Status date: 2026-05-29

## Result

EV3-EV6 backtest-fidelity remediation is confirmed CI-green.

```text
EV3 declared stop_model / exit_model handling: implemented
EV4 breakeven-after-T1 handling: implemented
EV5 gap-through-stop fill modeling: implemented
EV6 Target-1-only exit-date correction: implemented
Targeted EV3-EV6 tests: passed
Full regression suite: passed
Main CI: green
Live trading authorization: unchanged; not granted by code
```

## Completed scope

### EV3 — Declared model handling

Historical plan simulation now validates declared stop and exit models before running. Unsupported models fail closed instead of silently falling back to an implicit behavior.

Supported stop models:

```text
None
fixed
percentage_stop
breakeven_after_t1
```

Supported exit models:

```text
None
t1_t2
r_multiple_targets
t1_only
```

### EV4 — Breakeven after Target 1

When `stop_model="breakeven_after_t1"`, a stop after Target 1 exits at the entry price and records `0.0R` instead of a false full `-1R` loss.

### EV5 — Gap-through-stop realism

When a bar opens below the configured stop, the simulator can fill at the open instead of pretending the stop filled exactly at the stop-loss level.

### EV6 — Target-1-only exit date

Target-1-only exits now use the actual Target 1 hit bar as `exit_date`, preserving better chronology for out-of-sample and walk-forward segmentation.

## Regression coverage

```text
tests/test_backtest_fidelity_ev3_ev6.py
```

## CI coverage

The main CI workflow includes a dedicated EV3-EV6 regression step:

```text
pytest tests/test_backtest_fidelity_ev3_ev6.py -q
```

The full regression suite is also green after adding model aliases used by OOS reconstruction:

```text
percentage_stop
r_multiple_targets
```

## Operational boundary

This fix improves backtest-fidelity and chronology integrity. It does not prove trading edge, enable broker execution, authorize live trading, replace the 3-6 month paper-observation period, or approve real-money deployment.

## Next block

The next recommended remediation is one of:

```text
EV7 Decision Engine WATCH / REDUCED_SIZE ordering
EV10 profit_factor=inf degradation handling
EV11 conservative missing-indicator scoring fallbacks
```
