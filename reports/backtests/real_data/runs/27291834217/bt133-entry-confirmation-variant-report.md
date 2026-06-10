# BT133 Entry Confirmation Variant Report

## Evidence Contract

- Report version: bt133.v1
- Source evidence: reports/backtests/real-data-backtest-evidence.json
- Run ID: bt131-real-data-manual
- Data source: real_data
- Is demo: False
- Input pack gate: PASSED
- Input completeness: OK
- Run health: OK
- Live trading authorized: False
- Broker execution mode: paper_only
- Total source trades: 24
- Final recommendation: PROMOTE_TO_GUARDED_EXPERIMENT

## Walk-forward Periods

| Period | Start | End |
|---|---|---|
| training | 2024-03-28 | 2024-06-24 |
| walk_forward | 2024-06-24 | 2024-09-17 |
| out_of_sample | 2024-09-17 | 2025-11-19 |

## Variant Results

### baseline_breakout_trigger

- Family: baseline
- Status: EVALUATED
- Recommendation: KEEP_BASELINE
- Parameters: `{"entry_rule": "breakout_trigger"}`
- Missing fields: none

| Period | Considered | Accepted | Skipped | False BO | Stop | T1 | T2 | Avg R | Expectancy R |
|---|---|---|---|---|---|---|---|---|---|
| training | 8 | 7 | 1 | 0.2857 | 0.5714 | 0.7143 | 0.4286 | 0.4313 | 0.4313 |
| walk_forward | 8 | 8 | 0 | 0.625 | 0.5 | 0.375 | 0.125 | 0.0453 | 0.0453 |
| out_of_sample | 8 | 8 | 0 | 0.625 | 0.5 | 0.375 | 0.25 | 0.4062 | 0.4062 |

### next_bar_close_confirmation_1bar

- Family: next_bar_close_confirmation
- Status: EVALUATED
- Recommendation: PROMOTE_TO_GUARDED_EXPERIMENT
- Parameters: `{"confirmation_delay_bars": 1, "minimum_mfe_r": 0.25}`
- Missing fields: none
- Limitation: BT131/BT136 evidence has MAE/MFE summaries, not exact intrabar path ordering; result is research proxy only.

| Period | Considered | Accepted | Skipped | False BO | Stop | T1 | T2 | Avg R | Expectancy R |
|---|---|---|---|---|---|---|---|---|---|
| training | 8 | 3 | 5 | 0.0 | 0.0 | 1.0 | 1.0 | 2.3397 | 2.3397 |
| walk_forward | 8 | 4 | 4 | 0.5 | 0.0 | 0.5 | 0.25 | 1.1507 | 1.1507 |
| out_of_sample | 8 | 4 | 4 | 0.25 | 0.0 | 0.75 | 0.5 | 1.8343 | 1.8343 |

### next_bar_close_confirmation_2bar

- Family: next_bar_close_confirmation
- Status: EVALUATED
- Recommendation: PROMOTE_TO_GUARDED_EXPERIMENT
- Parameters: `{"confirmation_delay_bars": 2, "minimum_mfe_r": 0.5}`
- Missing fields: none
- Limitation: BT131/BT136 evidence has MAE/MFE summaries, not exact intrabar path ordering; result is research proxy only.

| Period | Considered | Accepted | Skipped | False BO | Stop | T1 | T2 | Avg R | Expectancy R |
|---|---|---|---|---|---|---|---|---|---|
| training | 8 | 3 | 5 | 0.0 | 0.0 | 1.0 | 1.0 | 2.3397 | 2.3397 |
| walk_forward | 8 | 4 | 4 | 0.5 | 0.0 | 0.5 | 0.25 | 1.1507 | 1.1507 |
| out_of_sample | 8 | 4 | 4 | 0.25 | 0.0 | 0.75 | 0.5 | 1.8343 | 1.8343 |

### next_bar_close_confirmation_3bar

- Family: next_bar_close_confirmation
- Status: EVALUATED
- Recommendation: PROMOTE_TO_GUARDED_EXPERIMENT
- Parameters: `{"confirmation_delay_bars": 3, "minimum_mfe_r": 0.75}`
- Missing fields: none
- Limitation: BT131/BT136 evidence has MAE/MFE summaries, not exact intrabar path ordering; result is research proxy only.

| Period | Considered | Accepted | Skipped | False BO | Stop | T1 | T2 | Avg R | Expectancy R |
|---|---|---|---|---|---|---|---|---|---|
| training | 8 | 2 | 6 | 0.0 | 0.0 | 1.0 | 1.0 | 2.6401 | 2.6401 |
| walk_forward | 8 | 4 | 4 | 0.5 | 0.0 | 0.5 | 0.25 | 1.1507 | 1.1507 |
| out_of_sample | 8 | 4 | 4 | 0.25 | 0.0 | 0.75 | 0.5 | 1.8343 | 1.8343 |

### volume_confirmed_breakout_1_1x

- Family: volume_confirmed_breakout
- Status: SKIPPED_INSUFFICIENT_FIELDS
- Recommendation: NEEDS_MORE_DATA
- Parameters: `{"entry_volume_to_avg_volume_20_min": 1.1}`
- Missing fields: avg_volume_20, entry_volume
- Limitation: Variant skipped because required evidence fields are missing from all source rows.

| Period | Considered | Accepted | Skipped | False BO | Stop | T1 | T2 | Avg R | Expectancy R |
|---|---|---|---|---|---|---|---|---|---|
| training | 8 | 0 | 8 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| walk_forward | 8 | 0 | 8 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| out_of_sample | 8 | 0 | 8 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |

### volume_confirmed_breakout_1_25x

- Family: volume_confirmed_breakout
- Status: SKIPPED_INSUFFICIENT_FIELDS
- Recommendation: NEEDS_MORE_DATA
- Parameters: `{"entry_volume_to_avg_volume_20_min": 1.25}`
- Missing fields: avg_volume_20, entry_volume
- Limitation: Variant skipped because required evidence fields are missing from all source rows.

| Period | Considered | Accepted | Skipped | False BO | Stop | T1 | T2 | Avg R | Expectancy R |
|---|---|---|---|---|---|---|---|---|---|
| training | 8 | 0 | 8 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| walk_forward | 8 | 0 | 8 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| out_of_sample | 8 | 0 | 8 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |

### volume_confirmed_breakout_1_5x

- Family: volume_confirmed_breakout
- Status: SKIPPED_INSUFFICIENT_FIELDS
- Recommendation: NEEDS_MORE_DATA
- Parameters: `{"entry_volume_to_avg_volume_20_min": 1.5}`
- Missing fields: avg_volume_20, entry_volume
- Limitation: Variant skipped because required evidence fields are missing from all source rows.

| Period | Considered | Accepted | Skipped | False BO | Stop | T1 | T2 | Avg R | Expectancy R |
|---|---|---|---|---|---|---|---|---|---|
| training | 8 | 0 | 8 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| walk_forward | 8 | 0 | 8 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| out_of_sample | 8 | 0 | 8 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |

### volatility_adjusted_confirmation_conservative

- Family: volatility_adjusted_confirmation
- Status: EVALUATED
- Recommendation: PROMOTE_TO_GUARDED_EXPERIMENT
- Parameters: `{"max_adverse_excursion_r_allowed": -0.95, "minimum_mfe_r": 0.25}`
- Missing fields: none
- Limitation: BT131/BT136 evidence has MAE/MFE summaries, not exact intrabar path ordering; result is research proxy only.

| Period | Considered | Accepted | Skipped | False BO | Stop | T1 | T2 | Avg R | Expectancy R |
|---|---|---|---|---|---|---|---|---|---|
| training | 8 | 3 | 5 | 0.0 | 0.0 | 1.0 | 1.0 | 2.3397 | 2.3397 |
| walk_forward | 8 | 4 | 4 | 0.5 | 0.0 | 0.5 | 0.25 | 1.1507 | 1.1507 |
| out_of_sample | 8 | 4 | 4 | 0.25 | 0.0 | 0.75 | 0.5 | 1.8343 | 1.8343 |

### volatility_adjusted_confirmation_medium

- Family: volatility_adjusted_confirmation
- Status: EVALUATED
- Recommendation: PROMOTE_TO_GUARDED_EXPERIMENT
- Parameters: `{"max_adverse_excursion_r_allowed": -0.75, "minimum_mfe_r": 0.5}`
- Missing fields: none
- Limitation: BT131/BT136 evidence has MAE/MFE summaries, not exact intrabar path ordering; result is research proxy only.

| Period | Considered | Accepted | Skipped | False BO | Stop | T1 | T2 | Avg R | Expectancy R |
|---|---|---|---|---|---|---|---|---|---|
| training | 8 | 2 | 6 | 0.0 | 0.0 | 1.0 | 1.0 | 2.6401 | 2.6401 |
| walk_forward | 8 | 3 | 5 | 0.3333 | 0.0 | 0.6667 | 0.3333 | 1.0984 | 1.0984 |
| out_of_sample | 8 | 2 | 6 | 0.5 | 0.0 | 0.5 | 0.5 | 2.0997 | 2.0997 |

### volatility_adjusted_confirmation_strict

- Family: volatility_adjusted_confirmation
- Status: EVALUATED
- Recommendation: NEEDS_MORE_DATA
- Parameters: `{"max_adverse_excursion_r_allowed": -0.5, "minimum_mfe_r": 0.75}`
- Missing fields: none
- Limitation: BT131/BT136 evidence has MAE/MFE summaries, not exact intrabar path ordering; result is research proxy only.

| Period | Considered | Accepted | Skipped | False BO | Stop | T1 | T2 | Avg R | Expectancy R |
|---|---|---|---|---|---|---|---|---|---|
| training | 8 | 2 | 6 | 0.0 | 0.0 | 1.0 | 1.0 | 2.6401 | 2.6401 |
| walk_forward | 8 | 2 | 6 | 0.5 | 0.0 | 0.5 | 0.5 | 1.5463 | 1.5463 |
| out_of_sample | 8 | 1 | 7 | 0.0 | 0.0 | 1.0 | 1.0 | 3.0 | 3.0 |

## Safety Notes

- Research only. No production entry rule change.
- No live trading authorization.
- broker_execution_mode remains paper_only.
- Promotion requires a separate guarded issue with before/after evidence.
