# RGP9 Signal Status Source of Truth

Status date: 2026-06-01

## Purpose

RGP9 centralizes signal lifecycle statuses and event types so runtime watcher, regime invalidation, runner management, reports and evidence flows cannot drift through duplicated string definitions.

## Implemented source of truth

```text
src/signals/signal_status.py
```

The module defines:

- `SignalStatus`
- `SignalEventType`
- `RunnerStatus`
- `ACTIONABLE_SIGNAL_ACTIONS`
- `OPEN_SIGNAL_STATUSES`
- `TERMINAL_SIGNAL_STATUSES`
- `REGIME_INVALIDATION_ELIGIBLE_STATUSES`
- status helper functions for normalization and classification

## Updated consumers

```text
src/watchers/entry_exit_watcher.py
src/watchers/regime_invalidation.py
src/watchers/trailing_stop_manager.py
scripts/run_entry_exit_watcher.py
```

## Regression coverage

```text
tests/test_rgp9_signal_status_source_of_truth.py
```

The tests prove:

- terminal statuses are sourced from one shared constant
- open and regime-invalidation eligible statuses are aligned
- status helper normalization is conservative and case-insensitive
- watcher lifecycle transitions still emit the expected event/status values
- terminal statuses cannot re-trigger
- runner management uses the shared partial-exit event and runner status values

## Live trading authorization

RGP9 does not authorize live trading. It only hardens research/paper lifecycle-state semantics.
