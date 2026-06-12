# Broad Exception Handling Policy

Status date: 2026-06-12

Issue: #198

## Rule

A broad handler such as:

```text
except Exception
```

is allowed only when the behavior is explicit.

Allowed behaviors:

```text
fail_closed_raise
degraded_continue
degraded_empty_records
fail_closed_blocked_regime
structured_audit_continue
```

## Required metadata

A swallowed or degraded exception must expose:

```text
stage
error_class
error_message
behavior
trace_id
timestamp_utc
component
rationale
```

## Helper

Use:

```text
src.exception_audit.build_exception_audit_event
```

## CI guard

The broad exception allowlist lives in:

```text
docs/operations/broad_exception_allowlist.json
```

Guard test:

```text
tests/test_198_broad_exception_allowlist.py
```

## Outcome tracking

Outcome read failures may return an empty record set only if the caller supplies an `audit_errors` list and the exception is appended as structured metadata.

## Market regime reporting

Market-regime client construction failures must fail closed to blocked regime evidence.

Breadth failures may degrade only when the report contains explicit `exception_audit` metadata.
