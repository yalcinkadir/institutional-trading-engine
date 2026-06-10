# BT134 Stop-Loss Variant Report

## Evidence Contract

- Report version: bt134.v1
- Source evidence: reports/backtests/real-data-backtest-evidence.json
- Run ID: bt131-real-data-manual
- Data source: real_data
- Is demo: False
- Input pack gate: PASSED
- Input completeness: OK
- Run health: OK
- Live trading authorized: False
- Broker execution mode: paper_only
- Production rule change allowed: False
- Total source trades: 24
- Final recommendation: OVERFIT_RISK

## Walk-forward Periods

| Period | Start | End |
|---|---|---|
| training | 2024-03-28 | 2024-06-24 |
| walk_forward | 2024-06-24 | 2024-09-17 |
| out_of_sample | 2024-09-17 | 2025-11-19 |

## Variant Results

### baseline_fixed_stop

- Family: baseline
- Status: EVALUATED
- Recommendation: KEEP_BASELINE
- Parameters: `{"stop_model": "fixed"}`
- Missing fields: none

| Period | Considered | Accepted | Skipped | Blocked | Same-bar | Stop | T1 | T2 | Avg R | Expectancy R |
|---|---|---|---|---|---|---|---|---|---|---|
| training | 8 | 7 | 1 | 0 | 0 | 0.5714 | 0.7143 | 0.4286 | 0.4313 | 0.4313 |
| walk_forward | 8 | 8 | 0 | 0 | 0 | 0.5 | 0.375 | 0.125 | 0.0453 | 0.0453 |
| out_of_sample | 8 | 8 | 0 | 0 | 0 | 0.5 | 0.375 | 0.25 | 0.4062 | 0.4062 |

### wider_fixed_stop_1_0x

- Family: wider_fixed_stop
- Status: EVALUATED
- Recommendation: KEEP_BASELINE
- Parameters: `{"stop_risk_multiplier": 1.0}`
- Missing fields: none
- Limitation: BT134 uses BT136 MAE/MFE summaries, not exact intrabar path ordering; result is a research proxy only.

| Period | Considered | Accepted | Skipped | Blocked | Same-bar | Stop | T1 | T2 | Avg R | Expectancy R |
|---|---|---|---|---|---|---|---|---|---|---|
| training | 8 | 7 | 1 | 0 | 0 | 0.5714 | 0.4286 | 0.4286 | 0.2857 | 0.2857 |
| walk_forward | 8 | 8 | 0 | 0 | 0 | 0.5 | 0.5 | 0.25 | 0.1366 | 0.1366 |
| out_of_sample | 8 | 8 | 0 | 0 | 0 | 0.5 | 0.5 | 0.375 | 0.375 | 0.375 |

### wider_fixed_stop_1_25x

- Family: wider_fixed_stop
- Status: EVALUATED
- Recommendation: OVERFIT_RISK
- Parameters: `{"stop_risk_multiplier": 1.25}`
- Missing fields: none
- Overfit warning: In-sample improves while out-of-sample is degraded or negative.
- Limitation: BT134 uses BT136 MAE/MFE summaries, not exact intrabar path ordering; result is a research proxy only.

| Period | Considered | Accepted | Skipped | Blocked | Same-bar | Stop | T1 | T2 | Avg R | Expectancy R |
|---|---|---|---|---|---|---|---|---|---|---|
| training | 8 | 7 | 1 | 0 | 0 | 0.2857 | 0.5714 | 0.5714 | 0.8146 | 0.8146 |
| walk_forward | 8 | 8 | 0 | 0 | 0 | 0.25 | 0.625 | 0.25 | 0.4518 | 0.4518 |
| out_of_sample | 8 | 8 | 0 | 0 | 0 | 0.5 | 0.5 | 0.375 | 0.25 | 0.25 |

### wider_fixed_stop_1_5x

- Family: wider_fixed_stop
- Status: EVALUATED
- Recommendation: OVERFIT_RISK
- Parameters: `{"stop_risk_multiplier": 1.5}`
- Missing fields: none
- Overfit warning: In-sample improves while out-of-sample is degraded or negative.
- Limitation: BT134 uses BT136 MAE/MFE summaries, not exact intrabar path ordering; result is a research proxy only.

| Period | Considered | Accepted | Skipped | Blocked | Same-bar | Stop | T1 | T2 | Avg R | Expectancy R |
|---|---|---|---|---|---|---|---|---|---|---|
| training | 8 | 7 | 1 | 0 | 0 | 0.1429 | 0.5714 | 0.5714 | 1.0329 | 1.0329 |
| walk_forward | 8 | 8 | 0 | 0 | 0 | 0.0 | 0.75 | 0.25 | 0.9559 | 0.9559 |
| out_of_sample | 8 | 8 | 0 | 0 | 0 | 0.375 | 0.5 | 0.375 | 0.3171 | 0.3171 |

### atr_stop_1_0x

- Family: atr_stop
- Status: SKIPPED_INSUFFICIENT_FIELDS
- Recommendation: NEEDS_MORE_DATA
- Parameters: `{"atr_multiple": 1.0}`
- Missing fields: atr14_at_signal
- Limitation: BT134 uses BT136 MAE/MFE summaries, not exact intrabar path ordering; result is a research proxy only.
- Limitation: ATR variant skipped unless atr14_at_signal is present in real-data evidence.
- Limitation: Variant skipped because required evidence fields are missing from all source rows.

| Period | Considered | Accepted | Skipped | Blocked | Same-bar | Stop | T1 | T2 | Avg R | Expectancy R |
|---|---|---|---|---|---|---|---|---|---|---|
| training | 8 | 0 | 8 | 0 | 0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| walk_forward | 8 | 0 | 8 | 0 | 0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| out_of_sample | 8 | 0 | 8 | 0 | 0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |

### atr_stop_1_5x

- Family: atr_stop
- Status: SKIPPED_INSUFFICIENT_FIELDS
- Recommendation: NEEDS_MORE_DATA
- Parameters: `{"atr_multiple": 1.5}`
- Missing fields: atr14_at_signal
- Limitation: BT134 uses BT136 MAE/MFE summaries, not exact intrabar path ordering; result is a research proxy only.
- Limitation: ATR variant skipped unless atr14_at_signal is present in real-data evidence.
- Limitation: Variant skipped because required evidence fields are missing from all source rows.

| Period | Considered | Accepted | Skipped | Blocked | Same-bar | Stop | T1 | T2 | Avg R | Expectancy R |
|---|---|---|---|---|---|---|---|---|---|---|
| training | 8 | 0 | 8 | 0 | 0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| walk_forward | 8 | 0 | 8 | 0 | 0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| out_of_sample | 8 | 0 | 8 | 0 | 0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |

### atr_stop_2_0x

- Family: atr_stop
- Status: SKIPPED_INSUFFICIENT_FIELDS
- Recommendation: NEEDS_MORE_DATA
- Parameters: `{"atr_multiple": 2.0}`
- Missing fields: atr14_at_signal
- Limitation: BT134 uses BT136 MAE/MFE summaries, not exact intrabar path ordering; result is a research proxy only.
- Limitation: ATR variant skipped unless atr14_at_signal is present in real-data evidence.
- Limitation: Variant skipped because required evidence fields are missing from all source rows.

| Period | Considered | Accepted | Skipped | Blocked | Same-bar | Stop | T1 | T2 | Avg R | Expectancy R |
|---|---|---|---|---|---|---|---|---|---|---|
| training | 8 | 0 | 8 | 0 | 0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| walk_forward | 8 | 0 | 8 | 0 | 0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| out_of_sample | 8 | 0 | 8 | 0 | 0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |

### same_bar_handling_stop_first

- Family: same_bar_handling
- Status: EVALUATED
- Recommendation: KEEP_BASELINE
- Parameters: `{"same_bar_mode": "stop_first"}`
- Missing fields: none
- Limitation: Same-bar sensitivity is only active for rows marked same_bar_ambiguous=true.

| Period | Considered | Accepted | Skipped | Blocked | Same-bar | Stop | T1 | T2 | Avg R | Expectancy R |
|---|---|---|---|---|---|---|---|---|---|---|
| training | 8 | 7 | 1 | 0 | 0 | 0.5714 | 0.7143 | 0.4286 | 0.4313 | 0.4313 |
| walk_forward | 8 | 8 | 0 | 0 | 0 | 0.5 | 0.375 | 0.125 | 0.0453 | 0.0453 |
| out_of_sample | 8 | 8 | 0 | 0 | 0 | 0.5 | 0.375 | 0.25 | 0.4062 | 0.4062 |

### same_bar_handling_target_first

- Family: same_bar_handling
- Status: EVALUATED
- Recommendation: KEEP_BASELINE
- Parameters: `{"same_bar_mode": "target_first"}`
- Missing fields: none
- Limitation: Same-bar sensitivity is only active for rows marked same_bar_ambiguous=true.

| Period | Considered | Accepted | Skipped | Blocked | Same-bar | Stop | T1 | T2 | Avg R | Expectancy R |
|---|---|---|---|---|---|---|---|---|---|---|
| training | 8 | 7 | 1 | 0 | 0 | 0.5714 | 0.7143 | 0.4286 | 0.4313 | 0.4313 |
| walk_forward | 8 | 8 | 0 | 0 | 0 | 0.5 | 0.375 | 0.125 | 0.0453 | 0.0453 |
| out_of_sample | 8 | 8 | 0 | 0 | 0 | 0.5 | 0.375 | 0.25 | 0.4062 | 0.4062 |

### same_bar_handling_conservative_blocked

- Family: same_bar_handling
- Status: EVALUATED
- Recommendation: KEEP_BASELINE
- Parameters: `{"same_bar_mode": "conservative_blocked"}`
- Missing fields: none
- Limitation: Same-bar sensitivity is only active for rows marked same_bar_ambiguous=true.

| Period | Considered | Accepted | Skipped | Blocked | Same-bar | Stop | T1 | T2 | Avg R | Expectancy R |
|---|---|---|---|---|---|---|---|---|---|---|
| training | 8 | 7 | 1 | 0 | 0 | 0.5714 | 0.7143 | 0.4286 | 0.4313 | 0.4313 |
| walk_forward | 8 | 8 | 0 | 0 | 0 | 0.5 | 0.375 | 0.125 | 0.0453 | 0.0453 |
| out_of_sample | 8 | 8 | 0 | 0 | 0 | 0.5 | 0.375 | 0.25 | 0.4062 | 0.4062 |

## Safety Notes

- Research only. No production stop rule change.
- No live trading authorization.
- broker_execution_mode remains paper_only.
- Promotion requires a separate guarded issue with before/after evidence.
