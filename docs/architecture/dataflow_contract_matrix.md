# Dataflow Contract Matrix — Scanner → Signals → Quality → Validator → Watcher → Evidence

Issue #161. This document defines the minimum field contract across the active trading pipeline.

The contract exists to prevent field drift between locally validated modules. A field that is valid inside one module is not enough; every required downstream consumer must receive the canonical field name or an explicitly documented compatibility alias.

## Canonical ATR rule

`atr14` is the canonical external field name. Internal functions may accept `atr`, but persisted scanner, signal, watcher and evidence payloads must prefer `atr14`. Consumers may accept `atr` only as a compatibility alias at the boundary, and boundary adapters must normalize it back to `atr14` before persistence.

## Canonical signal execution-state rule

Issue #194 defines the exported signal state invariant.

`action` is the execution-readiness source of truth:

- `BUY_WATCH` means the signal may be consumed by watcher/outcome/backtest paths as an actionable paper-observation plan.
- `NO_TRADE` means the signal is blocked, rejected or diagnostic-only and must not be consumed as an executable plan.

`NO_TRADE` persisted records must satisfy the following boundary contract:

- `decision` must be one of `blocked`, `no_trade` or `rejected`.
- `risk_tier` must be `NO_TRADE`, `blocked` or `no_trade`.
- `position_size` must be `0.0`.
- `entry_trigger` must be `null`.

A generator may internally receive an approved decision and later downgrade it because data quality, provenance, entry/stop/target quality or trade-plan validation failed. After downgrade, the exported record must encode the downgraded execution state consistently. Downstream modules must filter by `action == "BUY_WATCH"` for executable paper plans; they must not treat `decision == "approved"` or a non-`NO_TRADE` risk tier as sufficient execution readiness.

## Required contract table

| Field | Canonical name | Required | Producer | Consumer | Allowed aliases | Fail-closed behavior | Test coverage |
|---|---|---:|---|---|---|---|---|
| `symbol` | `symbol` | yes | scanner metrics pipeline | signals, validator, watcher, evidence | none | reject/block if missing | `tests/test_p161_dataflow_contract_matrix.py` |
| `close` | `close` | yes | scanner metrics pipeline | signal generation, quality engines | none | `data_status=BLOCKED` if missing | `tests/test_p161_dataflow_contract_matrix.py` |
| `atr14` | `atr14` | yes | scanner metrics pipeline | stop quality, trade-plan validator, watcher | `atr` at boundary only | reject/block if missing | `tests/test_p161_dataflow_contract_matrix.py` |
| `source` | `source` | yes | market-data provider layer | DATA1/data-quality gates | none | block if missing | `tests/test_p161_dataflow_contract_matrix.py` |
| `source_timestamp` | `source_timestamp` | yes | market-data provider layer | DATA1/data-quality gates | none | block if invalid/stale | `tests/test_p161_dataflow_contract_matrix.py` |
| `data_status` | `data_status` | yes | DATA1/scanner normalization | all downstream layers | none | block on `BLOCKED` | `tests/test_p161_dataflow_contract_matrix.py` |
| `signal_id` | `signal_id` | yes | signal identity | watcher/evidence | none | deterministic generation or reject | `tests/test_p161_dataflow_contract_matrix.py` |
| `action` | `action` | yes | signal generator | validator/watcher/evidence | none | `NO_TRADE` is non-executable; `BUY_WATCH` requires valid plan fields | `tests/test_p161_dataflow_contract_matrix.py`, `tests/test_194_signal_state_consistency.py` |
| `decision` | `decision` | yes | decision engine / signal generator | validator/watcher/evidence | none | `NO_TRADE` exports only `blocked`, `no_trade` or `rejected` | `tests/test_p161_dataflow_contract_matrix.py`, `tests/test_194_signal_state_consistency.py` |
| `risk_tier` | `risk_tier` | yes | decision engine / signal generator | report/outcome/watcher/evidence | none | `NO_TRADE` exports only `NO_TRADE`, `blocked` or `no_trade`; actionable tiers require `BUY_WATCH` | `tests/test_194_signal_state_consistency.py` |
| `position_size` | `position_size` | yes | signal generator | watcher/backtest/portfolio evidence | none | `NO_TRADE` must export `0.0` | `tests/test_194_signal_state_consistency.py` |
| `entry_trigger` | `entry_trigger` | yes | signal generator | validator/watcher/backtest | none | null allowed only for non-executable `NO_TRADE`; actionable records reject/block if missing | `tests/test_p161_dataflow_contract_matrix.py`, `tests/test_194_signal_state_consistency.py` |
| `stop_loss` | `stop_loss` | yes | stop-loss quality | validator/watcher/backtest | none | reject/block if missing for actionable records | `tests/test_p161_dataflow_contract_matrix.py` |
| `target_1` | `target_1` | yes | exit target quality | validator/watcher/backtest | none | reject/block if missing for actionable records | `tests/test_p161_dataflow_contract_matrix.py` |
| `run_health_status` | `run_health_status` | yes | report/evidence layer | docs/CI/status gates | none | distinguish OK, degraded, empty, blocked | `tests/test_p161_dataflow_contract_matrix.py` |
| `input_plan_count` | `input_plan_count` | yes | backtest/evidence | evidence gate | none | count input before filtering | `tests/test_p161_dataflow_contract_matrix.py` |
| `accepted_plan_count` | `accepted_plan_count` | yes | validator/backtest | evidence gate | none | zero accepted real-data plans fail closed | `tests/test_p161_dataflow_contract_matrix.py` |
| `rejected_plan_count` | `rejected_plan_count` | yes | validator/backtest | evidence gate | none | explicit rejection reasons required | `tests/test_p161_dataflow_contract_matrix.py` |

## Runtime boundary

A module may consume this contract only if it either:

1. validates all required fields before use, or
2. receives payloads from an upstream gate that has already validated the same fields.

No downstream layer may silently reinterpret a missing required field as a valid `NO_TRADE` day. Missing critical fields are infrastructure/data-contract failures and must be represented as `BLOCKED_MISSING_INPUTS` or an equivalent fail-closed status.

No downstream layer may reinterpret a `NO_TRADE` row as actionable because an upstream diagnostic field looks favorable. `action == "BUY_WATCH"` is required before watcher lifecycle updates, outcome tracking, backtest export or future portfolio/broker adapters may treat the row as executable.

## Evidence boundary

Backtesting and Paper Observation must not report success when required input fields are missing. They must produce one of:

- `OK`
- `NO_TRADE_VALID`
- `DEGRADED_DATA`
- `EMPTY_INPUT`
- `BLOCKED_MISSING_INPUTS`
- `FAILED`

`NO_TRADE_VALID` is allowed only when required fields are present and strategy logic produces no eligible signal. It is not allowed when `symbol`, `close`, `atr14`, `signal_id`, `entry_trigger`, `stop_loss`, `target_1`, `action` or `decision` is missing.

## Representative payload

The CI guard builds a representative payload containing all required Scanner → Signals → Quality → Validator → Watcher → Evidence fields and asserts that every required downstream field is present.

## Negative contract

The CI guard also removes critical fields from the representative payload and proves the result is `BLOCKED_MISSING_INPUTS`, not `NO_TRADE_VALID` or an empty successful report.

## CI guard

The contract is guarded by `tests/test_p161_dataflow_contract_matrix.py` and `tests/test_194_signal_state_consistency.py`.
