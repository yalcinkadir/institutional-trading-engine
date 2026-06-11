# Durable Evidence Index Contract

Status date: 2026-06-11

Issue: #181

## Purpose

The durable evidence index preserves lightweight, long-lived Paper Observation audit metadata for a 3-6 month review window.

GitHub Actions artifacts are useful review aids, but they are not the durable audit source of truth because they can expire before long-term review is complete.

## Authoritative index

The durable Paper Observation evidence index lives at:

```text
reports/daily_observation_automation/review_index.json
```

This extends the PO12 review index into a durable audit index without committing large runtime artifacts to `main`.

## Required top-level fields

The index must include:

```text
schema_version
index_path
artifact_root
retention_days
large_runtime_artifacts_committed_to_main
github_actions_artifacts_are_audit_source
durable_history_reconstructable_after_artifact_expiry
total_artifacts
status_counts
durable_status_counts
passed_count
blocked_count
review_ready_count
artifacts[]
live_trading_authorized
broker_execution_mode
```

Required safety values:

```text
large_runtime_artifacts_committed_to_main: false
github_actions_artifacts_are_audit_source: false
durable_history_reconstructable_after_artifact_expiry: true
live_trading_authorized: false
broker_execution_mode: paper_only
```

## Required artifact-entry fields

Each indexed Paper Observation run must include:

```text
observation_date
workflow_run_id
artifact_path
artifact_pointer
artifact_sha256
data_mode
degradation_flags
durable_status
automation_status
review_ready
gate_status
approved_for_review
blocker_count
error_count
total_records
accepted_count
rejected_count
needs_review_count
no_trade_valid
live_trading_authorized
broker_execution_mode
```

When metadata is not available yet, the index must expose the gap explicitly:

```text
workflow_run_id: UNKNOWN
artifact_sha256: not_available
data_mode: UNKNOWN
```

Silent omission is not acceptable for long-term auditability.

## Durable statuses

The durable index distinguishes:

```text
SUCCESS
BLOCKED
DEGRADED
FAILED
NO_TRADE_VALID
```

Meaning:

- `SUCCESS`: automation passed and no degradation/error state is recorded.
- `BLOCKED`: the run was blocked by the observation gate or automation status.
- `DEGRADED`: the run completed with degraded data or explicit degradation flags.
- `FAILED`: the run carries runtime/artifact errors.
- `NO_TRADE_VALID`: the run is valid/review-approved but has no review-ready actionable trade evidence.

## Large artifact boundary

Large runtime artifacts must not be committed to `main` unless a separate explicit policy allows that path.

The durable index stores pointers and checksums only. It does not store heavy runtime payloads.

## Review reconstruction rule

The review process must be able to reconstruct observation continuity from the durable index after GitHub artifact expiry.

The index must therefore preserve:

- observation date
- workflow run id when available
- durable status
- artifact pointer
- checksum when available
- data mode
- degradation flags
- paper-only/live-trading boundary

## Safety boundary

A valid durable evidence index does not mean:

```text
live trading is approved
broker execution is approved
production deployment is approved
capital allocation is approved
```

Live trading remains blocked until long-running forward evidence, drift monitoring, regime-change monitoring, execution-quality review, capacity/turnover realism, risk attribution and explicit manual approval exist.
