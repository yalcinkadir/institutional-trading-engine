# PO3 Daily Observation Run Record

Status date: 2026-06-01
Status: Done / CI-green

## Purpose

PO3 turns the PO2 Daily Observation Acceptance Gate into a concrete daily run record contract. Each Paper Observation day should produce a small, machine-readable summary that states whether the day is accepted, rejected or needs manual review.

This is an evidence-record contract only. It does not authorize live trading.

## Required record fields

```text
date
status
missing_evidence
incidents
artifact_paths
review_required
review_notes
live_trading_authorized
broker_execution_mode
created_at
```

## Status vocabulary

```text
ACCEPTED
REJECTED
NEEDS_REVIEW
```

## Field rules

```text
date: ISO-8601 observation date
status: one of ACCEPTED, REJECTED, NEEDS_REVIEW
missing_evidence: list of missing required evidence families
incidents: list of missing-data, provider-degradation, drift/regime or runtime anomaly notes
artifact_paths: list of evidence artifact paths referenced by this record
review_required: boolean
review_notes: manual review notes or empty string
live_trading_authorized: always false
broker_execution_mode: paper_only
created_at: deterministic or ISO-8601 timestamp
```

## Acceptance mapping

```text
ACCEPTED: no missing evidence, no unresolved incidents, review_required=false
REJECTED: missing required evidence or failed required generation
NEEDS_REVIEW: core evidence exists but incidents require manual review
```

## Example accepted record

```json
{
  "date": "2026-06-01",
  "status": "ACCEPTED",
  "missing_evidence": [],
  "incidents": [],
  "artifact_paths": [
    "reports/daily_evidence/2026-06-01.md",
    "reports/runtime_evidence/2026-06-01.json"
  ],
  "review_required": false,
  "review_notes": "",
  "live_trading_authorized": false,
  "broker_execution_mode": "paper_only",
  "created_at": "2026-06-01T00:00:00Z"
}
```

## CI result

```text
PO3 Daily Observation Run Record: Done / CI-green
```

## Test command

```bash
pytest tests/test_po3_daily_observation_run_record.py -q
```
