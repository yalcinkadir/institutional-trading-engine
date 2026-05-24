# Polygon Edge Data Pipeline

This document defines the next step for the edge-evidence phase: building a broad runtime dataset for universe coverage and historical bar analysis.

## Goal

The pipeline creates runtime artifacts, not large Git commits:

```text
data/universe/survivorship_universe.csv
data/historical_bars/<SYMBOL>.csv
reports/edge_evidence_data/polygon-data-manifest.md
```

## Scope

- Build a broad active market universe from all active symbols returned by the Polygon reference ticker endpoint.
- Write the output in the existing survivorship-universe schema.
- Treat 500 symbols as the minimum acceptance gate, not the target size.
- Pull daily OHLCV bars for the full generated universe by default.
- Use `--max-symbols` only for local smoke tests, rate-limit control, or cost-controlled trial runs.
- Upload generated data as workflow artifacts or store it outside normal source control.
- Keep the survivorship warning: active tickers alone are not a full point-in-time historical universe.

## Local all-assets run

Build the full active universe:

```bash
POLYGON_API_KEY=... python scripts/build_polygon_universe.py \
  --output data/universe/survivorship_universe.csv \
  --active-from 2026-05-24
```

Download daily bars for all symbols in that universe:

```bash
POLYGON_API_KEY=... python scripts/download_polygon_daily_bars.py \
  --universe data/universe/survivorship_universe.csv \
  --output-dir data/historical_bars \
  --from-date 2016-01-01 \
  --to-date 2026-05-24 \
  --min-bars 120
```

Optional smoke-test cap:

```bash
POLYGON_API_KEY=... python scripts/build_polygon_universe.py --max-symbols 25
POLYGON_API_KEY=... python scripts/download_polygon_daily_bars.py --max-symbols 25
```

## Expected workflow

```text
Actions -> Polygon Edge Data Pipeline -> Run workflow
```

The first serious run should use all active Polygon symbols and a multi-year bar window. A later production-grade run should enrich this dataset with delisted ticker lifecycles and historical membership from a vetted second source.

## Limitations

Polygon active tickers plus OHLCV bars are useful for broad evidence collection, but they are not final survivorship-safe 10+ year evidence without delisted ticker lifecycles and point-in-time membership.
