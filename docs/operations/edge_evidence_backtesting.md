# Edge-Evidence Backtesting

This document describes how to run the gated backtesting pipeline for the 3-6 month edge-evidence phase.

## Goal

The goal is not to prove that the code is well structured. The goal is to collect evidence that the generated setups have measurable edge after universe, liquidity, survivorship, walk-forward and out-of-sample controls.

## Required inputs

```text
data/universe/survivorship_universe.csv
data/trade_plans/historical_trade_plans.json
data/historical_bars/<SYMBOL>.csv
```

Historical bars must use this schema:

```text
date,open,high,low,close,volume
```

Trade plans must contain at least:

```text
signal_id
symbol
signal_date
entry_trigger
stop_loss
target_1
```

## Build active 500+ starter universe

```bash
python scripts/build_sp500_plus_universe.py \
  --output data/universe/survivorship_universe.csv
```

This creates a current active starter universe from S&P 500 constituents plus sector, industry, factor, credit, commodity and volatility ETFs.

Important: this is not enough for 10+ year survivorship-safe backtesting. It must be enriched with historical members and delisted ticker lifecycles.

## Validate universe coverage

```bash
python scripts/validate_universe_coverage.py \
  --universe data/universe/survivorship_universe.csv \
  --as-of 2026-05-24 \
  --minimum 500
```

A serious backtest must fail if fewer than 500 symbols are tradeable on the point-in-time date.

## Run gated backtest locally

```bash
python scripts/run_edge_evidence_backtest.py \
  --universe data/universe/survivorship_universe.csv \
  --plans data/trade_plans/historical_trade_plans.json \
  --bars-root data/historical_bars \
  --as-of 2026-05-24 \
  --minimum-assets 500 \
  --oos-split-date 2024-01-01
```

Reports are written to:

```text
reports/edge_evidence/
```

## Run from GitHub Actions

Use:

```text
Actions → Edge Evidence Backtest → Run workflow
```

The workflow uploads `reports/edge_evidence/` as an artifact.

## Fail-closed reasons

The pipeline returns exit code `1` when any critical gate fails:

```text
universe_coverage_below_minimum
survivorship_audit_failed
no_trade_plans_loaded
walk_forward_failed
out_of_sample_lockbox_failed
```

This is intentional. Do not weaken these gates to make a report green.

## OOS Lockbox rule

The out-of-sample lockbox should be opened once for a prepared validation run, written to reports, and then treated as consumed. Repeated tuning against the lockbox invalidates its purpose.

## Evidence period

For the first 3-6 months:

- keep the system decision-support only
- collect generated signals
- track forward outcomes
- compare paper/live observation to backtest expectation
- do not add capital-risk authorization until P41-P47 and manual review pass

## Data-quality warning

Polygon historical OHLCV bars are useful, but they do not by themselves solve survivorship bias. Delisted ticker lifecycles and point-in-time index membership must come from a vetted second source such as Norgate, CRSP, Sharadar, or an equivalent manually audited dataset.
