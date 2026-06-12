# Broad Exception Handling Policy

Status date: 2026-06-12

Issue: #198

## Purpose

Broad exception handlers are allowed only when their behavior is explicit, reviewable and safe.

A broad handler is any handler equivalent to:

```text
except Exception
except BaseException
bare except
```

## Required behavior

Every active broad handler must do at least one of the following:

```text
re-raise / fail closed
return a structured degraded result
write or expose structured audit metadata
be listed in the broad exception allowlist with explicit rationale
```

## Required metadata

Structured exception audit metadata must include:

```text
stage
error_class
error_message
behavior
trace_id
timestamp_utc
component
rationale
policy
severity
```

## Allowlist

The active-path allowlist is stored in:

```text
docs/architecture/broad_exception_allowlist.json
```

Each entry must include:

```text
path
function
behavior
rationale
evidence
```

## Checker

The lightweight checker is:

```text
scripts/check_broad_exception_policy.py
```

It scans the active paths named in the #198 audit scope and fails if a broad handler is not listed in the allowlist.

## Guard tests

```text
tests/test_198_broad_exception_policy.py
```

The tests verify:

```text
structured audit event metadata
safe_call degraded result metadata
outcome read degraded result audit metadata
runtime loop structured logging and fail-closed threshold
active broad exception allowlist coverage
```

## Rule

A new broad exception handler in an active path must either be removed, narrowed to specific exception types, or added to the allowlist with explicit behavior, rationale and evidence.
