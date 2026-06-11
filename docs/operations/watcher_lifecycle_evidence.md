# Watcher Lifecycle Evidence Contract

Status date: 2026-06-11

Issue: #193

## Purpose

Watcher lifecycle evidence makes signal-level forward behaviour repo-visible and reviewable after local runtime files or GitHub Actions artifacts expire.

The watcher must prove whether each signal was observed, watched, triggered, skipped, expired, blocked or left without an event during a watcher cycle.

## Authoritative artifact

The authoritative lightweight lifecycle summary is:

- `reports/watchers/lifecycle/YYYY-MM-DD.json`
- `reports/watchers/lifecycle/latest.json`

`data/signal_lifecycle.jsonl` remains a mutable runtime/event log for detailed lifecycle event history. It is not the primary repo-visible lifecycle summary.

## Required summary fields

Each summary must include:

- `schema_version`
- `generated_at`
- `summary_date`
- `run_id`
- `cycle_id`
- `status`
- `signal_file_path`
- `signal_file_sha256`
- `signal_count`
- `actionable_open_count`
- `lifecycle_event_count`
- `data_completeness_status`
- `market_data_health`
- `records[]`

Each record must include:

- `signal_id`
- `signal_batch_date`
- `symbol`
- `initial_action`
- `initial_status`
- `watcher_status`
- `event_type`
- `previous_status`
- `new_status`
- `trigger_expiry_block_reason`
- `data_completeness_status`
- `signal_file_path`
- `signal_file_sha256`

## Empty / no-actionable runs

A watcher cycle with zero actionable open signals must still write a dated lifecycle summary.

Such runs must be marked as:

- `status = NO_ACTIONABLE_SIGNALS`
- record-level `watcher_status = NO_ACTIONABLE_SIGNALS`
- record-level `trigger_expiry_block_reason = not_actionable_or_terminal_signal`

This prevents a silent green watcher run from being mistaken for signal-level forward evidence.

## Boundary

This contract does not authorize live trading, broker execution or production rule changes.

The system remains research / decision-support / paper-observation only. Live trading authorization is not granted by code.
