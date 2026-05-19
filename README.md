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
```

This now represents the first true institutional end-to-end decision pipeline inside the repository.

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
