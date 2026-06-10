# BT134 Stop-Loss Variant Test

## Purpose

BT134 is a research-only stop-loss variant comparison built on the BT131/BT136 real-data evidence family. It does not change production stop rules.

The goal is to compare the current fixed stop baseline with alternative stop-loss variants and report whether any variant deserves later guarded investigation. A promotion decision is not authorized by BT134 alone.

## Source evidence

BT134 reads:

```text
reports/backtests/real_data/latest/real-data-backtest-evidence.json
```

Required evidence contract:

- `data_source=real_data`
- `is_demo=false`
- `input_pack_gate_status=PASSED`
- `run_health_status=OK`
- `live_trading_authorized=false`
- `broker_execution_mode=paper_only`
- non-empty `results`

If these gates are not satisfied, the analyzer exits fail-closed.

## Variants

BT134 compares:

1. `baseline_fixed_stop`
2. wider fixed stop sensitivity:
   - `wider_fixed_stop_1_0x`
   - `wider_fixed_stop_1_25x`
   - `wider_fixed_stop_1_5x`
3. ATR stop sensitivity:
   - `atr_stop_1_0x`
   - `atr_stop_1_5x`
   - `atr_stop_2_0x`
4. same-bar handling sensitivity:
   - `same_bar_handling_stop_first`
   - `same_bar_handling_target_first`
   - `same_bar_handling_conservative_blocked`

ATR variants require `atr14_at_signal`. If that field is unavailable in the real-data evidence, ATR variants are reported as `SKIPPED_INSUFFICIENT_FIELDS`; the analyzer does not guess ATR.

## Walk-forward requirement

Rows are sorted by `signal_date` and split into:

```text
training
walk_forward
out_of_sample
```

Each variant reports per-period:

- total trades considered
- accepted trades
- skipped trades
- blocked trades
- same-bar ambiguous trades
- stop-hit rate
- target-1 hit rate
- target-2 hit rate
- average R
- expectancy R

## Recommendation rules

Recommendations are one of:

- `KEEP_BASELINE`
- `PROMOTE_TO_GUARDED_EXPERIMENT`
- `NEEDS_MORE_DATA`
- `REJECT_VARIANT`
- `OVERFIT_RISK`

A variant is marked `OVERFIT_RISK` if it improves in-sample but out-of-sample evidence degrades or remains negative.

A variant is promoted only when out-of-sample expectancy improves and stop-hit rate does not materially worsen.

## Outputs

Workflow output paths:

```text
reports/backtests/real_data/latest/bt134-stop-loss-variant-report.json
reports/backtests/real_data/latest/bt134-stop-loss-variant-report.md
reports/backtests/real_data/runs/<github_run_id>/bt134-stop-loss-variant-report.json
reports/backtests/real_data/runs/<github_run_id>/bt134-stop-loss-variant-report.md
```

Index fields:

```text
bt134_final_recommendation
bt134_variant_count
bt134_production_rule_change_allowed
```

## Safety boundary

BT134 always reports:

```json
"production_rule_change_allowed": false
```

No live trading is authorized. No broker secrets are used. No Telegram notification is sent. Any later production stop-rule change requires a separate issue, fresh evidence, and explicit approval.
