# BT176 Guarded Entry Confirmation Experiment

## Evidence Contract

- Report version: bt176.v1
- Source evidence: reports/backtests/real-data-backtest-evidence.json
- Source variant report: reports/backtests/bt133-entry-confirmation-variant-report.json
- Run ID: bt131-real-data-manual
- Candidate variant: next_bar_close_confirmation_1bar
- Candidate family: next_bar_close_confirmation
- Candidate parameters: `{"confirmation_delay_bars": 1, "minimum_mfe_r": 0.25}`
- Guard status: READY_FOR_PAPER_SHADOW
- Experiment scope: paper_observation_shadow_only
- Production rule change allowed: False
- Live trading authorized: False
- Broker execution mode: paper_only

## Baseline vs Guarded Experiment

| Mode | Considered | Accepted | Filtered | False BO | Stop | T1 | T2 | Avg R | Expectancy R |
|---|---|---|---|---|---|---|---|---|---|
| baseline | 24 | 23 | 1 | 0.5217 | 0.5217 | 0.4783 | 0.2609 | 0.2883 | 0.2883 |
| guarded_experiment | 24 | 11 | 13 | 0.2727 | 0.0 | 0.7273 | 0.5455 | 1.7235 | 1.7235 |

## Guard Reasons

- none

## Acceptance Criteria

- BT133 source recommendation remains PROMOTE_TO_GUARDED_EXPERIMENT.
- Candidate variant is evaluated, promoted and has no missing fields.
- Guarded experiment expectancy is not below baseline on the current evidence pack.
- Guarded experiment does not worsen false-breakout or stop-hit rate.
- At least two accepted trades remain after confirmation filtering.
- Experiment remains paper-observation shadow-only and cannot change production entry rules.

## Safety Notes

- Research only. No production entry rule change.
- No live trading authorization.
- broker_execution_mode remains paper_only.
- Promotion to production requires a separate issue, fresh forward evidence and explicit approval.
