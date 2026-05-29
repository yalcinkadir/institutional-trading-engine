# CL4 ATR Governance

CL4 makes ATR semantics explicit, versioned and regression-tested before any ATR migration is trusted by reports, ranking, backtests, paper execution or evidence gates.

## Purpose

ATR is not just an indicator detail. If ATR changes, downstream stop distance, volatility classification, position sizing, setup readiness and backtest comparability can change. A silent migration from simple rolling ATR to Wilder-smoothed ATR would invalidate prior ATR-dependent evidence.

## Implemented safeguards

```text
src/validation/atr_governance.py
tests/test_atr_governance.py
src/config/thresholds.py
```

Safeguards:

- True range explicitly includes previous-close gap risk.
- Supported ATR methods are explicit: `simple` and `wilder`.
- Wilder ATR is seeded by the first simple average and then recursively smoothed.
- ATR calculation version is exposed through `ATR_CALCULATION_VERSION`.
- Public-demo threshold version was bumped to mark the ATR governance change.
- Method changes produce an evidence-invalidation requirement instead of silently reusing older evidence.
- Insufficient ATR history blocks migration approval.

## Test command

```bash
pytest tests/test_atr_governance.py -q
```

## Operational rule

Any ATR method migration must be treated as evidence-affecting. Backtests, walk-forward runs, lockbox results, paper-observation baselines and reports that depend on ATR must not be compared against old artifacts without the version boundary being acknowledged.

## Safety note

CL4 improves calculation governance only. It does not prove edge and does not authorize live trading.
