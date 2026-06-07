# P131 Watcher Missing-Market-Data Health Gate

Status: Implemented / CI-pending
Date: 2026-06-07

## Purpose

The Entry/Exit Watcher must not silently preserve actionable or open signal state when no current market bar is available for a symbol that still needs lifecycle evaluation.

## Implemented behavior

The watcher now creates a market-data health payload with one of three statuses:

- `PASSED`: every actionable open signal had price-bar coverage.
- `DEGRADED`: a pending actionable signal had no price bar, but no active stop or exit risk was open.
- `BLOCKED`: an already-triggered or target-1 runner signal had no price bar, meaning stop or exit risk could not be checked.

The runtime runner writes the health artifact to:

```text
reports/runtime/entry_exit_watcher_market_data_health.json
```

When the status is `BLOCKED`, the runner exits with code `3` so the runtime cycle cannot be treated as a clean no-event cycle.

## Files changed

- `src/watchers/market_data_health.py`
- `scripts/run_entry_exit_watcher.py`
- `tests/test_watcher_missing_market_data_health_gate.py`

## Test coverage

The guard tests cover:

- all actionable symbols covered by bars => `PASSED`
- pending actionable signal without bar => `DEGRADED`
- triggered signal without bar => `BLOCKED`
- target-1 runner signal without bar persists a health artifact

## Completion criteria

P131 can move from CI-pending to CI-green after:

```bash
pytest tests/test_watcher_missing_market_data_health_gate.py -q
pytest tests/test_entry_exit_watcher.py -q
pytest -q
```

all pass in CI.
