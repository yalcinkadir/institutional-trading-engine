# Runtime Loop

## Purpose

The Runtime Loop turns the orchestrator from a static callable component into a continuously executable runtime process.

This closes the gap between isolated intelligence engines and a running institutional decision system.

## Current Flow

```text
cycle_provider()
    ↓
decision generated
    ↓
runtime_state.update(decision)
    ↓
state snapshot available
    ↓
next cycle
```

## Why This Matters

The platform previously contained many strong engines, but most of them were callable only through tests or scripts.

The Runtime Loop creates:

- continuous execution
- runtime state
- cycle history
- deterministic orchestration
- future persistence integration

## Runtime State

Stored in:

```text
src/runtime/runtime_state.py
```

Tracks:

- latest decision
- cycle count
- update timestamp
- decision history

## Operational Notes

- deterministic loop
- no distributed event bus required yet
- no Redis dependency required
- no Postgres dependency required
- designed for simple observability and testability

## Acceptance Criteria

The Runtime Loop must:

- execute at least one cycle
- update runtime state
- expose current state
- support max_cycles for testability
- remain deterministic in tests
