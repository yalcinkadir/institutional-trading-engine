# EV1-EV2 Sharpe Definition CI-Green Completion

Status date: 2026-05-29

## Result

EV1-EV2 Sharpe / Deflated-Sharpe evidence-unit correction is confirmed CI-green.

```text
EV1 calculate_sharpe_ratio per-trade Sharpe: implemented
EV2 Deflated Sharpe input unit correction: implemented
EV9 historical edge drawdown gate effective-threshold audit fix: implemented
Targeted EV1-EV2 tests: passed
Main CI: green
Live trading authorization: unchanged; not granted by code
```

## Completed scope

### EV1 — Sharpe definition

`calculate_sharpe_ratio` now returns sample-size-independent per-trade Sharpe using the evaluated artifact distribution. The sample-size-scaled t-statistic is exposed separately through `calculate_sharpe_tstat`.

### EV2 — Deflated Sharpe input unit

The Deflated Sharpe calculation now receives the per-trade Sharpe unit expected by the robustness formula instead of the previous sample-size-scaled value.

### EV9 — Drawdown gate audit threshold

The historical edge drawdown gate now reports the effective absolute R threshold used by the gate, not only the raw multiplier.

## Regression coverage

```text
tests/test_sharpe_definition_regression.py
```

## CI coverage

The main CI workflow includes a dedicated EV1-EV2 regression step:

```text
pytest tests/test_sharpe_definition_regression.py -q
```

## Evidence boundary

`THRESHOLDS_VERSION` was bumped to invalidate older public-demo evidence artifacts that used the previous Sharpe semantics. Old historical edge artifacts should not be compared across this version boundary without explicit re-computation.

## Operational boundary

This fix improves evidence-math integrity. It does not prove trading edge, enable broker execution, authorize live trading, replace the 3-6 month paper-observation period, or approve real-money deployment.

## Next block

The next recommended critical block is EV3-EV6 backtest fidelity:

```text
EV3 simulate declared stop_model / exit_model or fail closed
EV4 handle breakeven-after-T1 / no false full -1R after T1
EV5 model gap-through-stop pessimistically
EV6 use actual Target-1 hit date for Target-1-only exits
```
