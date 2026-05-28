# BT1 — Deterministic Backtest Run Contract

BT1 defines a deterministic, versioned contract for every backtest run.

The goal is to make backtests reproducible before any scenario matrix or optimization work starts.

## What the contract captures

```text
strategy_id
strategy_version
universe_id
symbol list
start_date / end_date
data_source
data_source_version
threshold_version
setup_config_version
execution assumptions
benchmark_id
run_purpose
metadata
```

The generated `contract_id` is a stable SHA-256 digest prefix over the normalized public contract payload. Timestamp fields do not change the contract id.

## Why this matters

Without a run contract, a result can silently change because of data-source changes, symbol-list changes, config-version changes or execution-assumption changes.

BT1 makes these dimensions explicit.

## CLI

Use:

```bash
python scripts/create_backtest_run_contract.py --help
```

The CLI writes a JSON contract with a stable `contract_id`.

## Safety

BT1 is framework infrastructure only.

```text
No broker call
No order execution
No live trading authorization
No private edge parameters
No proprietary production thresholds
```

Public contracts should use demo identifiers or version labels. Real private-edge configuration should remain outside the public repository.
