# Daily Paper Observation Source

B13 replaces bootstrap incoming records with real persisted daily paper observation source records.

## Purpose

The observation-only bootstrap proves that the Daily Evidence pipeline works end-to-end. It does not prove trading edge.

The daily paper observation source builder converts real daily paper observation files into feed-compatible source files for the existing persisted observation feed.

## Required raw source files

The source directory must contain:

```text
paper_observations.json
backtest_results.json
regime_observations.json
position_snapshots.json
```

The builder derives:

```text
forward_results.json
```

from `paper_observations.json` by using the observed paper result R values.

## Output files

The output directory contains the five files required by the persisted feed:

```text
paper_observations.json
backtest_results.json
forward_results.json
regime_observations.json
position_snapshots.json
```

Each generated record is marked with:

```text
source = daily_paper_observation_source
source_version = 2026.05.26-v1
```

## Bootstrap rejection

Records with this source are rejected:

```text
source = observation_only_bootstrap
```

This prevents accidentally mixing Day-0 bootstrap records into the real forward observation source feed.

## CLI

```bash
python scripts/build_daily_paper_observation_sources.py \
  --source-dir reports/daily_paper_observation_raw \
  --output-dir reports/daily_observation_incoming \
  --report-dir reports/daily_paper_observation_source
```

Then the existing persisted-feed pipeline can continue:

```bash
python scripts/persist_daily_observation_sources.py \
  --incoming-dir reports/daily_observation_incoming \
  --feed-dir reports/daily_observation_feed \
  --report-dir reports/daily_observation_source_feed \
  --report-date 2026-05-26
```

## Hard rule

This is still observation-only paper evidence. It does not authorize live capital.

Live capital remains blocked until the 3-6 month observation period produces credible evidence and the relevant drift, regime, attribution and robustness gates support it.
