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

- Build a broad active market universe.
- Write a 500+ active universe CSV in the existing survivorship-universe schema.
- Pull daily OHLCV bars for selected symbols.
- Upload generated data as workflow artifacts.
- Keep the survivorship warning: active tickers alone are not a full point-in-time historical universe.

## Expected workflow

```text
Actions -> Polygon Edge Data Pipeline -> Run workflow
```

The first serious run should use at least 500 symbols and a multi-year bar window. A later production-grade run should enrich this dataset with delisted ticker lifecycles and historical membership from a vetted second source.
