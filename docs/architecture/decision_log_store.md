# Decision Log Store

## Purpose

The Decision Log Store introduces persistent institutional memory.

Every orchestrator decision can now be stored and replayed.

This is foundational for:

- auditability
- reproducibility
- explainability
- regime learning
- adaptive intelligence

## Storage Format

Current implementation:

```text
JSONL
```

Future target:

```text
Postgres-backed persistence
```

## Stored Fields

- decision_id
- created_at
- payload

## Institutional Importance

Institutional systems require:

- decision traceability
- historical replay
- persistent runtime memory
- post-trade analysis

The Decision Log Store creates the first persistent runtime audit layer.

## Operational Notes

- deterministic append-only structure
- human-readable storage
- easy migration path to Postgres
- test-friendly persistence
