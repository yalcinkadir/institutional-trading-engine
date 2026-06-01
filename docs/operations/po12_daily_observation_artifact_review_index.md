# PO12 Daily Observation Artifact Retention & Review Index

Status date: 2026-06-01  
Status: Done / CI-green

## Purpose

PO12 makes generated PO10/PO11 daily observation automation artifacts reviewable as an indexed evidence set.

It does not generate trading signals, place orders, authorize broker execution or approve live trading.

## Review index file

```text
reports/daily_observation_automation/review_index.json
```

## Implementation file

```text
src/operations/daily_observation_artifact_review_index.py
```

## Test file

```text
tests/test_po12_daily_observation_artifact_review_index.py
```

## Default retention metadata

```text
retention_days: 180
```

The retention value is metadata for review discipline. It does not delete files by itself.

## Review index fields

```text
index_path
artifact_root
retention_days
total_artifacts
status_counts
passed_count
blocked_count
review_ready_count
artifacts[]
live_trading_authorized: false
broker_execution_mode: paper_only
```

Each artifact entry contains:

```text
observation_date
artifact_path
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
live_trading_authorized: false
broker_execution_mode: paper_only
```

## Valid automation statuses

```text
PASSED
BLOCKED
```

## Guarded failure cases

PO12 rejects or surfaces:

```text
retention_days_must_be_positive
duplicate_artifact_date:<date>
artifact_missing_observation_date
artifact:<date>:invalid_automation_status
artifact:<date>:live_trading_must_remain_false
artifact:<date>:broker_execution_mode_must_be_paper_only
artifact:<date>:gate_live_trading_must_remain_false
artifact:<date>:gate_broker_execution_mode_must_be_paper_only
artifact:<date>:artifact_path_must_be_canonical
review_index_path_must_be_canonical
```

## Canonical paths

Artifact root:

```text
reports/daily_observation_automation
```

Artifact path:

```text
reports/daily_observation_automation/YYYY-MM-DD.json
```

Review index path:

```text
reports/daily_observation_automation/review_index.json
```

## Test command

```bash
pytest tests/test_po12_daily_observation_artifact_review_index.py -q
```

## Safety boundary

PO12 preserves:

```text
live_trading_authorized: false
broker_execution_mode: paper_only
```

A valid PO12 review index means the generated daily observation automation artifacts are structured for review.

It does not mean:

```text
live trading is approved
broker execution is approved
production deployment is approved
capital allocation is approved
```

Live trading remains blocked until long-running forward evidence, drift monitoring, regime-change monitoring, execution-quality review, capacity/turnover realism, risk attribution and explicit manual approval exist.
