# Daily Observation Source Feed

B12 introduces a persisted daily observation source feed.

## Purpose

B11 made the Daily Evidence workflow honest by replacing placeholder component files with source, input, validation and report generation steps. B12 starts replacing the Day-0 observation-only bootstrap seed with a persistent feed of daily observation source records.

The feed appends incoming source records into a durable source directory and keeps the filenames expected by the Daily Evidence input builder.

## Incoming directory

```text
reports/daily_observation_incoming/
```

Required incoming files:

```text
paper_observations.json
backtest_results.json
forward_results.json
regime_observations.json
position_snapshots.json
```

Each file must contain a non-empty JSON list of records.

## Persistent feed directory

```text
reports/daily_observation_feed/
```

The persisted feed writes the same five source files, allowing the existing builder to consume the feed as its source directory.

## CLI

```bash
python scripts/persist_daily_observation_sources.py \
  --incoming-dir reports/daily_observation_incoming \
  --feed-dir reports/daily_observation_feed \
  --report-dir reports/daily_observation_source_feed \
  --report-date 2026-05-26
```

Exit codes:

```text
0 = incoming records persisted successfully
1 = incoming source contract missing or invalid
```

## Behavior

- fails closed when any required incoming source file is missing
- fails closed when incoming files are not JSON lists
- fails closed when incoming files are empty
- annotates records with `source=daily_observation_source_feed`
- annotates records with feed version and report date
- de-duplicates records by stable content hash
- keeps output compatible with `scripts/build_daily_evidence_inputs.py`

## Evidence discipline

This feed persists observation source records. It does not authorize live capital and it does not make the evidence period complete by itself.

B1.1 remains a 3-6 month observation-only evidence period. Live capital remains unauthorized until forward evidence, drift, regime, risk and manual review gates are satisfied.
