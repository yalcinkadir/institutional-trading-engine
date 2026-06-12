# Exception Audit Policy

Status date: 2026-06-12

Issue: #198

## Purpose

Broad exception handling is allowed only when the behavior is explicit and auditable.

A broad handler must do one of the following:

```text
fail_closed
structured_degraded_result
audit_then_continue
```

## Required metadata

Any structured exception audit event must include:

```text
policy
stage
component
trace_id
severity
error_class
error_message
timestamp_utc
behavior
```

## Central helper

Use:

```text
src.exception_audit.build_exception_audit_event
src.exception_audit.safe_call
```

## Active path rule

Active runtime, report and evidence-producing paths must not silently swallow broad exceptions.

Allowed broad handlers must include one of:

```text
#198
EXPLICIT_EXCEPTION_AUDIT
noqa: BLE001
```

The marker is not enough by itself. The handler must also expose structured error metadata, fail closed or produce an explicitly degraded result.

## Guard test

```text
tests/test_198_exception_audit_contract.py
```

The guard covers:

```text
src/runtime/runtime_loop.py
src/reporting/market_regime.py
src/outcome_tracking.py
```
