# System Invariants

Status: active governance baseline for issue #189.

This document defines project-wide invariants that must hold before evidence, reports, backtests, roadmap status or strategy-readiness claims are promoted.

These invariants are intentionally machine-checkable. They are not only guidance text. Each invariant must define its severity, enforcement surface, evidence requirements and exception policy.

## Severity model

| Severity | Meaning | Required behaviour |
|---|---|---|
| `P0_BLOCKER` | Unsafe or misleading state | Block merge, roadmap promotion, production-grade evidence claims and strategy-validation claims. |
| `P1_DEGRADED` | Usable only with explicit degradation | Allow research visibility only when degraded provenance and forbidden claims are explicit. |
| `P2_WARNING` | Non-blocking but review-relevant | Allow the run, but surface the warning in evidence, reports or review output. |

No invariant violation may be silently converted to `PASS`.

## Canonical evidence states

| State | Meaning | Claim boundary |
|---|---|---|
| `PASS` | Required evidence is complete, reproducible and validated for the stated scope. | Claims are limited to the validated scope only. |
| `DEGRADED` | The run may continue for research visibility, but evidence is incomplete, proxy-backed, partially unavailable or lower confidence. | Must not claim full confidence, production readiness, strategy validation or live-readiness. |
| `BLOCKED` | The run cannot support the requested evidence or promotion claim. | Must not claim success. Must include blocker reason codes. |
| `FAILED` | The run failed unexpectedly or implementation/runtime error occurred. | Must not be counted as a valid no-trade or valid degraded evidence state. |

DEGRADED must never behave like `PASS`.

## Required invariant schema

Every invariant must use this schema:

```yaml
id: SI-001
name: No silent success
rationale: Empty, invalid, incomplete or unreproducible inputs must never be counted as successful evidence.
severity: P0_BLOCKER
affected_layers:
  - scanner
  - signal_generator
  - paper_observation
  - backtesting
  - outcome_tracking
  - reporting
enforced_by:
  tests:
    - tests/test_system_invariants.py
  runtime_checks:
    - evidence_quality_gate
  ci_gates:
    - targeted-evidence-validation
valid_states:
  - PASS
  - DEGRADED
  - BLOCKED
  - FAILED
forbidden_claims:
  - production_ready
  - strategy_validated
  - paper_observation_success
required_evidence:
  - run_id
  - status
  - data_mode
  - input_data_source
  - pipeline_version
  - blocked_reasons
exception_policy: Demo/local exceptions must be explicit and must not count as production-grade evidence.
```

## SI-001 — No silent success

```yaml
id: SI-001
name: No silent success
rationale: Empty, invalid, incomplete or unreproducible upstream data must never be counted as successful evidence.
severity: P0_BLOCKER
affected_layers:
  - scanner
  - signal_generator
  - paper_observation
  - backtesting
  - outcome_tracking
  - reporting
enforced_by:
  tests:
    - tests/test_system_invariants.py
    - tests/test_no_silent_success.py
  runtime_checks:
    - evidence_quality_gate
  ci_gates:
    - targeted-evidence-validation
valid_states:
  - PASS
  - DEGRADED
  - BLOCKED
  - FAILED
forbidden_claims:
  - production_ready
  - strategy_validated
  - paper_observation_success
required_evidence:
  - run_id
  - status
  - input_count
  - valid_count
  - invalid_count
  - blocked_reasons
  - data_mode
exception_policy: Expected empty/demo/local runs must be explicit and must not count as production evidence.
```

## SI-002 — No uncoupled strategy evidence

```yaml
id: SI-002
name: No uncoupled strategy evidence
rationale: Backtest or strategy metrics must not validate the trading engine unless plans were produced through the actual runtime decision pipeline.
severity: P0_BLOCKER
affected_layers:
  - scanner
  - signal_generator
  - quality_engines
  - trade_plan_validator
  - backtesting
  - reporting
enforced_by:
  tests:
    - tests/test_system_invariants.py
  runtime_checks:
    - backtest_evidence_gate
  ci_gates:
    - real-data-backtest-evidence
valid_states:
  - PASS
  - BLOCKED
forbidden_claims:
  - strategy_validated
  - real_data_backtest_validated
  - decision_stack_validated
required_evidence:
  - pipeline_coupled
  - runtime_trace
  - accepted_trade_plan_count
  - rejected_trade_plan_count
  - generator_version
exception_policy: Deterministic or demo generators must be labelled demo/stub and blocked from real-data strategy evidence claims.
```

## SI-003 — No unknown regime promotion

```yaml
id: SI-003
name: No unknown regime promotion
rationale: Unknown, unavailable or proxy-degraded regime evidence must not authorize bullish/full-confidence/readiness claims.
severity: P0_BLOCKER
affected_layers:
  - regime
  - signals
  - validator
  - reporting
  - evidence
valid_states:
  - PASS
  - DEGRADED
  - BLOCKED
enforced_by:
  tests:
    - tests/test_system_invariants.py
  runtime_checks:
    - regime_evidence_gate
  ci_gates:
    - paper-observation-validation
forbidden_claims:
  - bullish_full_confidence
  - full_trade_readiness
  - paper_confidence_authorized
required_evidence:
  - regime_status
  - source
  - fallback_used
  - validation_status
  - reason
exception_policy: Proxy-backed regime evidence may continue as research visibility only and must be marked DEGRADED.
```

## SI-004 — No placeholder scoring in confidence/readiness

```yaml
id: SI-004
name: No placeholder scoring in confidence/readiness
rationale: Placeholder, synthetic or demo scoring must never feed confidence, ranking, readiness or allocation-like outputs.
severity: P0_BLOCKER
affected_layers:
  - scoring
  - decision_confidence
  - ranking
  - reporting
valid_states:
  - PASS
  - BLOCKED
enforced_by:
  tests:
    - tests/test_system_invariants.py
  runtime_checks:
    - scoring_source_gate
  ci_gates:
    - targeted-evidence-validation
forbidden_claims:
  - confidence_score_validated
  - readiness_validated
  - rank_order_validated
required_evidence:
  - scoring_source
  - scoring_mode
  - is_placeholder
  - data_mode
exception_policy: Placeholder values are allowed only in public-safe demo output and must be excluded from confidence/readiness.
```

## SI-005 — No missing provenance for production-grade evidence

```yaml
id: SI-005
name: No missing provenance for production-grade evidence
rationale: Evidence must be tied to reproducible inputs, execution identity and generator/runtime versions.
severity: P0_BLOCKER
affected_layers:
  - paper_observation
  - backtesting
  - outcome_tracking
  - reporting
  - ci
valid_states:
  - PASS
  - DEGRADED
  - BLOCKED
enforced_by:
  tests:
    - tests/test_evidence_traceability_contract.py
  runtime_checks:
    - evidence_traceability_gate
  ci_gates:
    - evidence-quality-gate
forbidden_claims:
  - production_grade_evidence
  - reproducible_evidence
  - strategy_validated
required_evidence:
  - run_id
  - workflow_run_id
  - input_data_source
  - input_data_checksum
  - symbol_universe
  - date_range
  - pipeline_version
  - runtime_trace
  - generator_version
  - data_mode
  - status
exception_policy: Missing provenance may be DEGRADED for research visibility only; it cannot be PASS for production-grade evidence.
```

## SI-006 — No decision-critical module without runtime reachability

```yaml
id: SI-006
name: No decision-critical module without runtime reachability
rationale: A decision-critical module is not complete when it is only unit-tested but not executed in the runtime path that creates evidence or decisions.
severity: P0_BLOCKER
affected_layers:
  - architecture
  - scanner
  - quality_engines
  - decision_confidence
  - validator
  - reporting
valid_states:
  - PASS
  - BLOCKED
enforced_by:
  tests:
    - tests/test_system_invariants.py
  runtime_checks:
    - runtime_reachability_trace
  ci_gates:
    - architecture-reachability-validation
forbidden_claims:
  - decision_stack_validated
  - module_complete
  - strategy_validated
required_evidence:
  - critical_module_registry
  - runtime_trace
  - executed_modules
  - missing_modules
exception_policy: Non-runtime support modules must be explicitly classified as support, experimental, legacy or deprecated.
```

## SI-007 — DEGRADED must not behave like PASS

```yaml
id: SI-007
name: DEGRADED must not behave like PASS
rationale: Degraded states are useful for continuity and visibility, but must never authorize the same claims as a fully validated PASS.
severity: P0_BLOCKER
affected_layers:
  - all_evidence
  - reporting
  - roadmap
  - ci
valid_states:
  - PASS
  - DEGRADED
  - BLOCKED
  - FAILED
enforced_by:
  tests:
    - tests/test_logic_safety_state_matrix.py
  runtime_checks:
    - status_claim_gate
  ci_gates:
    - evidence-quality-gate
forbidden_claims:
  - production_ready
  - full_confidence
  - strategy_validated
  - live_ready
required_evidence:
  - status
  - degradation_reasons
  - forbidden_claims
  - claim_scope
exception_policy: None. DEGRADED may be reported, but it must not be promoted as PASS.
```

## Logic-safety state matrix

| Condition | Allowed state | Forbidden claims |
|---|---|---|
| VIX missing and no fallback exists | `BLOCKED` or `DEGRADED` | bullish/full-confidence, paper-confidence-authorized |
| VIX proxy fallback is used | `DEGRADED` | full VIX validation, live-readiness, full confidence |
| Empty signal batch in production outcome tracking | `BLOCKED` | successful outcome learning, paper observation success |
| Real-data backtest is not pipeline-coupled | `BLOCKED` | strategy validation, decision stack validated |
| Decision-critical module is not runtime-reachable | `BLOCKED` | module complete, decision stack validated |
| Demo/stub/synthetic data is used | `DEGRADED` or `BLOCKED` | real-data evidence, production-grade evidence |
| Input checksum/provenance is missing | `DEGRADED` or `BLOCKED` | reproducible evidence, production-grade evidence |
| Regime is unknown/unvalidated | `BLOCKED` or `DEGRADED` | full trade readiness, bullish/full confidence |

## Relation to #188 Evidence Quality Gate

Issue #188 defines the promotion-level Evidence Quality Gate. This document defines the lower-level logic-safety invariants that the gate must evaluate.

The hierarchy is:

```text
System Invariants (#189)
  -> Logic Safety State Matrix
    -> Evidence Traceability Contract
      -> Evidence Quality Gate (#188)
        -> Roadmap / strategy / live-readiness promotion decisions
```

A roadmap or strategy claim is not valid unless the relevant invariants are satisfied for the claimed scope.
