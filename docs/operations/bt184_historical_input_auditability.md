# BT184 Historical Input Auditability Contract

Status date: 2026-06-11

BT184 defines the audit source-of-truth contract for real-data historical backtests.

## Problem

A real-data backtest is not reproducible when the evidence artifact references source data that only existed inside a GitHub Actions runner or an expiring Actions artifact.

GitHub Actions artifacts are review aids. They are not the durable audit source of truth.

## Source-of-truth strategy

The repository is the durable source of truth for accepted BT131 real-data backtest inputs and evidence.

A BT131 run can be treated as accepted real-data backtest evidence only when all of the following are true:

1. BT9 passes.
2. P121/BT130 evidence validation passes.
3. The evidence artifact contains non-empty `input_checksums`.
4. The coverage manifest contains `symbols[].output_path` and `symbols[].output_sha256` entries.
5. The referenced CSV bars exist under `data/historical/bars/1day/*.csv` or an explicitly documented permanent equivalent.
6. The workflow persists reports and source inputs back to the repository under reviewable paths.

## Required persisted paths

Accepted BT131 evidence must persist these inputs or a documented permanent equivalent:

- `data/historical/bars/1day/*.csv`
- `data/historical/metadata/coverage_manifest.json`
- `data/historical/metadata/ingestion_status.json`
- `data/historical/metadata/bt131_runtime_universe.csv`
- `data/trade_plans/historical_trade_plans.json`
- `data/trade_plans/historical_trade_plans_manifest.json`

Accepted BT131 evidence must persist these reports:

- `reports/backtests/real_data/runs/<github_run_id>/real-data-backtest-evidence.json`
- `reports/backtests/real_data/runs/<github_run_id>/bt9-real-historical-input-pack-gate.json`
- `reports/backtests/real_data/latest/real-data-backtest-evidence.json`
- `reports/backtests/real_data/index.json`

## Fail-closed rules

BT9 must fail closed when:

- the coverage manifest is missing,
- referenced source CSV files are missing,
- a source-data checksum does not match the coverage manifest,
- trade plans are missing canonical #177 pipeline metadata,
- trade plans come from observation/demo/deterministic generators instead of the canonical runtime pipeline.

The real-data evidence gate must fail when an accepted evidence artifact does not contain non-empty `input_checksums`.

## Boundary

This contract does not authorize live trading, broker execution or production rule changes.

The system remains research / decision-support / paper-observation only. Live trading authorization is not granted by code.
