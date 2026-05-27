# Daily Observation Cadence Review

B15 starts the operational discipline for real daily paper observation data capture.

## Purpose

The Daily Evidence pipeline can now run in two observation-only modes:

1. bootstrap observation-only mode for Day-0 pipeline checks
2. real paper observation mode for daily paper evidence capture

The cadence review checks whether a real paper observation day has the required raw files and the expected evidence artifacts.

## Raw source files

A real paper observation day should provide these raw files:

```text
reports/daily_paper_observation_raw/paper_observations.json
reports/daily_paper_observation_raw/backtest_results.json
reports/daily_paper_observation_raw/regime_observations.json
reports/daily_paper_observation_raw/position_snapshots.json
```

These records are transformed into feed-compatible incoming sources before the persisted feed, input builder, validator, component reports and daily evidence report run.

## Cadence review CLI

```bash
python scripts/review_daily_observation_cadence.py \
  --report-date 2026-05-27 \
  --raw-source-dir reports/daily_paper_observation_raw \
  --artifact-root reports \
  --output-dir reports/daily_observation_cadence
```

The CLI writes:

```text
reports/daily_observation_cadence/daily_observation_cadence_review.json
reports/daily_observation_cadence/daily_observation_cadence_review.md
reports/daily_observation_cadence/cadence_exit_code.txt
```

## Gates

The review checks:

```text
raw_source_files_complete
raw_source_records_present
persisted_feed_present
input_validation_present
component_reports_complete
daily_evidence_report_present
diagnostic_exit_codes_present
```

## Workflow behavior

When the Daily Evidence workflow is run with:

```text
use_real_paper_observation_source = true
bootstrap_observation_only_sources = false
```

it runs the real paper observation source builder and then the cadence review.

If the cadence review fails, the workflow uploads the diagnostic artifact first and then fails the workflow. This keeps the system auditable.

## Hard rule

Cadence review success proves capture discipline and artifact completeness. It does not prove trading edge.

```text
B15 green = daily observation process works
B15 green != statistically proven edge
B15 green != live capital authorization
```

Live capital remains blocked until the full forward observation window is complete and reviewed.
