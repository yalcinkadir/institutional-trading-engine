# Scanner Market-Data Run Context

Status date: 2026-06-12

Issue: #195

## Purpose

Scanner market-data state is scoped to a run context.

## Runtime context

Use:

```text
MarketDataRunContext.from_env(run_id=...)
```

The context owns:

```text
run_id
api_key
failures
provider
```

## API key boundary

The runtime API key is read when the context is created.

This prevents import-order side effects when tests or scheduled jobs change environment variables.

## Failure boundary

Market-data failures are recorded inside the context.

A new scanner run should use a new context so failures from a prior run do not leak into the next run.

## Evidence

The context can export structured failure evidence:

```text
failure_evidence()
```

Fields:

```text
run_id
provider
failure_count
failures[]
```

Each failure includes:

```text
symbol
kind
message
provider
status_code
attempts
run_id
recorded_at
```

## Compatibility

Legacy helpers remain available, but runtime/report paths should pass an explicit context:

```text
get_daily_bars(..., context=context)
get_vix_value(..., context=context)
build_symbol_metrics(..., context=context)
build_report(context=context)
```

## Guard tests

```text
tests/test_195_scanner_runtime_state.py
```
