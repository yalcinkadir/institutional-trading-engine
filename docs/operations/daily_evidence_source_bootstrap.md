# Daily Evidence Source Bootstrap

B11.3 adds an explicit observation-only Day-0 bootstrap for the Daily Evidence workflow.

## Purpose

The Daily Evidence workflow now requires source files before it can build validated inputs and B1-B6 evidence component reports.

The bootstrap exists only to activate the workflow path for observation-only operation when no real source feed is available yet. It must not be treated as statistically meaningful forward evidence.

## Workflow input

Manual workflow dispatch supports:

```text
bootstrap_observation_only_sources=true
```

When enabled, the workflow writes source files into:

```text
reports/daily_evidence_sources/
```

and then continues through:

```text
Build daily evidence inputs
Validate daily evidence inputs
Generate B1-B6 evidence component reports
Build daily evidence report
Upload artifacts
```

## Generated source files

```text
paper_observations.json
backtest_results.json
forward_results.json
regime_observations.json
position_snapshots.json
```

Each record is marked with:

```text
source = observation_only_bootstrap
```

## CLI

```bash
python scripts/bootstrap_daily_evidence_sources.py \
  --output-dir reports/daily_evidence_sources \
  --report-dir reports/daily_evidence_source_bootstrap \
  --report-date 2026-05-26
```

## Hard rule

This is not live evidence. It is only an operational seed for the Day-0 observation workflow.

A real 3-6 month forward observation period is still required before live capital can be considered.
