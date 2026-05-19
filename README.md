# Institutional Trading Engine

![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![CI](https://img.shields.io/badge/CI-enabled-brightgreen.svg)
![Status](https://img.shields.io/badge/status-production--oriented-orange.svg)

Institutional-grade market analysis, reporting, screening, governance and outcome-tracking platform.

The project is designed as:

- modular
- auditable
- deterministic
- reproducible
- explainable
- risk-first
- production-oriented

The system is NOT intended to be a black-box trading bot.

Instead, it acts as an institutional intelligence platform.

---

# Architecture Reality Check

A critical architectural clarification:

The repository now contains many institutional intelligence modules.

However, not all modules are fully integrated into a single live runtime pipeline yet.

Current state:

| Layer | Status |
|---|---|
| Individual Engines | Implemented |
| Unit Tests | Mostly implemented |
| Architecture Docs | Partially implemented |
| End-to-End Orchestration | Partially implemented |
| Fully Unified Runtime Pipeline | In progress |

---

# Runtime Evolution Status

The platform is now transitioning from:

```text
collection of institutional intelligence engines
```

into:

```text
continuous institutional runtime system
```

---

# Phase 1 — Runtime Loop

Implemented:

```text
src/runtime/runtime_loop.py
src/runtime/runtime_state.py
```

Capabilities:

- continuous runtime cycles
- deterministic orchestration
- runtime state tracking
- cycle history
- state snapshots

Validation:

```text
tests/test_runtime_loop.py
```

Architecture documentation:

```text
docs/architecture/runtime_loop.md
```

---

# Phase 2 — Persistence Layer

Implemented:

```text
src/storage/decision_log_store.py
```

Capabilities:

- append-only decision persistence
- runtime audit trail
- historical replay foundation
- institutional memory foundation

Validation:

```text
tests/test_decision_log_store.py
```

Architecture documentation:

```text
docs/architecture/decision_log_store.md
```

Current implementation:

```text
JSONL persistence
```

Future target:

```text
Postgres-backed institutional persistence
```

---

# Phase 3 — Runtime State Layer

Implemented:

```text
src/runtime/in_memory_state_cache.py
```

Capabilities:

- runtime state caching
- shared runtime memory
- temporary orchestration state
- deterministic state access

Validation:

```text
tests/test_in_memory_state_cache.py
```

Important:

Redis was intentionally NOT added yet.

Reason:

```text
Deterministic runtime architecture
is currently more important than distributed infrastructure complexity.
```

The current architecture intentionally prioritizes:

- explainability
- auditability
- runtime simplicity
- deterministic execution

before introducing:

- distributed runtime systems
- event buses
- async infrastructure
- Redis pub/sub

---

# Connected Runtime Decision Flow

The following engines are NOW connected through:

```text
src/orchestration/institutional_decision_orchestrator.py
```

Connected layers:

```text
Cross Asset Intelligence
→ Tail Risk Engine
→ Liquidity Intelligence
→ Portfolio Intelligence
→ Macro Regime Fusion
→ Slippage Intelligence
→ Multi-Factor Fusion
→ Probabilistic Decision Engine
→ Confidence Weighted Execution
→ Runtime Loop
→ Runtime State
→ Decision Log Persistence
```

This now represents the first continuously executable institutional runtime architecture inside the repository.

---

# End-to-End Integration Validation

The repository now contains a real integration test:

```text
tests/test_end_to_end_institutional_flow.py
```

This validates that the major intelligence engines:

- communicate together
- exchange outputs
- produce a unified institutional decision
- generate final exposure sizing
- create explainable reasoning

This is one of the most important architectural milestones.

---

# Current Architectural Reality

Currently:

```text
Some modules are fully connected.
Some modules are still standalone intelligence layers.
```

Examples of connected systems:

- Macro Regime Fusion
- Cross Asset Intelligence
- Tail Risk Intelligence
- Liquidity Intelligence
- Portfolio Intelligence
- Multi-Factor Fusion
- Probabilistic Decisions
- Confidence-Weighted Execution
- Runtime Loop
- Runtime State
- Decision Persistence

Examples of partially isolated systems:

- Event Bus
- Background Workers
- Redis Runtime
- Postgres Runtime
- Regime Similarity Memory
- Feature Attribution Learning
- Adaptive Weighting Persistence

These exist and are tested individually, but are not yet fully integrated into one continuous runtime orchestration layer.

---

# Development Standard

No new feature should be added without:

```text
- tests
- architecture documentation
- explainability
- operational notes
- deterministic behavior
```

This is now considered an institutional development requirement.
