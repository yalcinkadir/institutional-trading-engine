# Daily Evidence Input Builder

B11.2 adds a normalized input builder for the Daily Evidence workflow.

## Purpose

The workflow should not require hand-written `reports/daily_evidence_inputs/*.json` files. Instead, raw observation source files are transformed into the validated input contract used by B1-B6 evidence generation.

## Source directory

```text
reports/daily_evidence_sources/
```

## Required source files

```text
paper_observations.json
backtest_results.json
forward_results.json
regime_observations.json
position_snapshots.json
```

## Generated input files

```text
reports/daily_evidence_inputs/paper_observation_records.json
reports/daily_evidence_inputs/backtest_records.json
reports/daily_evidence_inputs/forward_records.json
reports/daily_evidence_inputs/regime_records.json
reports/daily_evidence_inputs/position_records.json
```

## CLI

```bash
python scripts/build_daily_evidence_inputs.py \
  --source-dir reports/daily_evidence_sources \
  --output-dir reports/daily_evidence_inputs \
  --report-dir reports/daily_evidence_input_build
```

Exit codes:

```text
0 = input files built and passed validation
1 = source contract missing/invalid or generated inputs invalid
```

## Workflow order

```text
Build daily evidence inputs
→ Validate daily evidence inputs
→ Generate B1-B6 component reports
→ Build daily evidence report
→ Upload build, validation, component and daily report artifacts
```

## Important discipline

The builder normalizes raw observation data. It does not invent evidence. If required source files are missing, the workflow fails closed.

Live capital remains unauthorized until the 3-6 month observation-only evidence period is complete and all gates remain acceptable.
