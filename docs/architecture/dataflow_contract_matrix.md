# Dataflow Contract Matrix — Scanner → Signals → Quality → Validator → Watcher → Evidence

Issue #161. This document defines the minimum field contract across the active trading pipeline.

## Canonical ATR rule

`atr14` is the canonical external field name. Internal functions may accept `atr`, but persisted scanner, signal, watcher and evidence payloads must prefer `atr14`. Consumers may accept `atr` only as a compatibility alias at the boundary.

## Required contract table

| Field | Canonical name | Required | Producer | Consumer | Fail-closed behavior |
|---|---|---:|---|---|---|
| `symbol` | `symbol` | yes | scanner metrics pipeline | signals, validator, watcher, evidence | reject/block if missing |
| `close` | `close` | yes | scanner metrics pipeline | signal generation, quality engines | `data_status=BLOCKED` if missing |
| `atr14` | `atr14` | yes | scanner metrics pipeline | stop quality, trade-plan validator, watcher | reject/block if missing |
| `source` | `source` | yes | market-data provider layer | DATA1/data-quality gates | block if missing |
| `source_timestamp` | `source_timestamp` | yes | market-data provider layer | DATA1/data-quality gates | block if invalid/stale |
| `data_status` | `data_status` | yes | DATA1/scanner normalization | all downstream layers | block on `BLOCKED` |
| `signal_id` | `signal_id` | yes | signal identity | watcher/evidence | deterministic generation or reject |
| `entry_trigger` | `entry_trigger` | yes | signal generator | validator/watcher/backtest | reject if missing |
| `stop_loss` | `stop_loss` | yes | stop-loss quality | validator/watcher/backtest | reject if missing |
| `target_1` | `target_1` | yes | exit target quality | validator/watcher/backtest | reject if missing |
| `run_health_status` | `run_health_status` | yes | report/evidence layer | docs/CI/status gates | distinguish OK, degraded, empty, blocked |
| `input_plan_count` | `input_plan_count` | yes | backtest/evidence | evidence gate | count input before filtering |
| `accepted_plan_count` | `accepted_plan_count` | yes | validator/backtest | evidence gate | zero accepted real-data plans fail closed |
| `rejected_plan_count` | `rejected_plan_count` | yes | validator/backtest | evidence gate | explicit rejection reasons required |

## Runtime boundary

A module may consume this contract only if it either:

1. validates all required fields before use, or
2. receives payloads from an upstream gate that has already validated the same fields.

## Evidence boundary

Backtesting and Paper Observation must not report success when required input fields are missing. They must produce one of:

- `OK`
- `NO_TRADE_VALID`
- `DEGRADED_DATA`
- `EMPTY_INPUT`
- `BLOCKED_MISSING_INPUTS`
- `FAILED`

## CI guard

The contract is guarded by `tests/test_p161_dataflow_contract_matrix.py`.
