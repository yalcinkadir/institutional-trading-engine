# Polygon Edge Data Pipeline

This document defines the edge-evidence runtime data pipeline: building a broad Polygon universe and downloading historical daily bars without committing large market-data files to Git.

## Goal

The pipeline creates runtime artifacts, not large Git commits:

```text
data/universe/survivorship_universe.csv
data/historical_bars/<SYMBOL>.csv
reports/edge_evidence_data/polygon-bars-manifest.md
```

## Scope

- Build a broad active market universe from all active symbols returned by the Polygon reference ticker endpoint.
- Write the output in the existing survivorship-universe schema.
- Treat 500 symbols as the minimum acceptance gate, not the target size.
- Pull daily OHLCV bars for the full generated universe by default.
- Use `--max-symbols` only for local smoke tests, rate-limit control, or cost-controlled trial runs.
- Upload generated data as workflow artifacts or store it outside normal source control.
- Keep the survivorship warning: active tickers alone are not a full point-in-time historical universe.

## GitHub Actions workflow

After adding the repository secret `POLYGON_API_KEY`, run:

```text
Actions -> Polygon Edge Data Pipeline -> Run workflow
```

Recommended first full-runtime inputs:

```text
from_date: 2016-01-01
to_date: 2026-05-24
min_bars: 120
max_symbols: 0
sleep_seconds: 0.0
```

Meaning:

```text
max_symbols = 0 means all available active Polygon symbols.
```

The workflow validates the runtime secret, builds the all-assets universe, validates the 500+ minimum coverage gate, downloads daily bars and uploads the generated dataset as an artifact.

Artifact name:

```text
polygon-edge-runtime-dataset
```

Artifact contents:

```text
data/universe/survivorship_universe.csv
data/historical_bars/
reports/edge_evidence_data/
```

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

## Tests

```bash
pytest tests/test_polygon_data_pipeline.py -q
pytest tests/test_polygon_edge_data_workflow.py -q
```

## Limitations

Polygon active tickers plus OHLCV bars are useful for broad evidence collection, but they are not final survivorship-safe 10+ year evidence without delisted ticker lifecycles and point-in-time membership.
