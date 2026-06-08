# P151 Real-Data Backtest Evidence Pack Boundary

P151 defines the first orchestrated real-data historical backtest evidence path.

The goal is not to produce optimistic backtest performance numbers. The goal is to prove whether a backtest result is evidence-grade or blocked.

## Evidence rule

Demo, synthetic, placeholder or public-safe datasets are not trading-edge evidence.

A backtest result can be treated as real historical evidence only when all of the following are true:

- historical bars come from an approved/licensed source
- survivorship universe validation passes
- coverage manifest exists
- trade plans are validated and not fully rejected
- `data_source=real_data`
- `is_demo=false`
- BT9 input-pack gate passes
- BT130 real-data evidence gate passes
- live trading remains disabled
- broker execution mode remains `paper_only`

## Approved data source

Current approved source:

- Polygon historical aggregate bars, via `POLYGON_API_KEY`

If `POLYGON_API_KEY` is missing and ingestion is not explicitly skipped for prepared test fixtures, the package builder writes a `BLOCKED` package and does not produce a valid real-data evidence artifact.

## Builder

Canonical command:

```bash
python scripts/build_real_data_backtest_evidence_pack.py \
  --symbols SPY,QQQ,AAPL \
  --start-date 2024-01-01 \
  --end-date 2026-01-01 \
  --run-id real-bt-manual-001 \
  --plans-file data/trade_plans/historical_trade_plans.json \
  --bars-root data/historical/bars/1day \
  --universe data/universe/survivorship_universe.csv \
  --coverage-manifest data/historical/metadata/coverage_manifest.json \
  --output-dir reports/backtests/real-data-evidence-pack
```

Outputs:

- `reports/backtests/real-data-evidence-pack/real-data-backtest-evidence-package.json`
- `reports/backtests/real-data-evidence-pack/real-data-backtest-evidence.json`
- `reports/backtests/real-data-evidence-pack/real-data-backtest-evidence.md`

Generated evidence artifacts must not be committed to the public repository unless explicitly sanitized and approved.

## Status outcomes

### `BLOCKED`

The package is not evidence-grade. Common reasons:

- missing `POLYGON_API_KEY`
- unapproved data source
- historical ingestion failure
- missing bars, universe or trade-plan file
- missing coverage manifest
- all trade plans rejected

### `VALID`

The package passed the real-data path and BT130 evidence gate.

### `FAILED`

The backtest ran but the generated evidence artifact failed the BT130 gate.

## Manual versus scheduled execution

P151 supports manual execution first. Scheduling is intentionally deferred until the data license, universe scope, retention policy and artifact handling are fully governed.

## Safety boundary

P151 does not authorize live trading, broker execution, capital allocation or production deployment.
