# Logic Safety Governance

Status: active governance baseline for issue #189.

This policy explains how new features are allowed to change trading, evidence, reporting, backtesting or governance logic without introducing silent logic errors.

## Objective

New features must not weaken existing evidence, runtime, fail-closed or claim-boundary guarantees.

The project must prefer explicit `BLOCKED` or `DEGRADED` states over ambiguous success when data, provenance, reachability or runtime behaviour is uncertain.

## Required development sequence

For changes touching scanner, signals, quality engines, regime, risk, validator, watcher, reporting, backtesting, outcome tracking, evidence generation or CI gates, use this order:

1. Define the intended behaviour and claim boundary.
2. Identify affected system invariants from `docs/architecture/system-invariants.md`.
3. Define dangerous states and allowed outputs.
4. Add or update guard/contract tests first.
5. Implement the minimal change.
6. Run targeted tests.
7. Run affected module/integration tests.
8. Produce or validate evidence output where applicable.
9. Update README, ROADMAP, CHANGELOG or operations docs only after behaviour is proven.

## Feature mini-spec

Every logic-changing issue or PR should be answerable through this compact spec:

```md
## Intent
What behaviour changes and why?

## Affected invariants
- SI-___

## Inputs
Which data fields, external sources, config values or artifacts are required?

## Outputs
Which statuses, evidence fields or report claims may be emitted?

## Dangerous states
What must never silently pass?

## State matrix
| Condition | Allowed state | Forbidden claim |
|---|---|---|

## Evidence
Which artifact proves the behaviour and how is it tied to run_id, checksum/provenance and runtime trace?

## Exception policy
Are demo/local/degraded modes allowed? If yes, what claims are forbidden?
```

## Automated enforcement expectation

Manual checkboxes are not enough. A PR should link to at least one of:

- a guard test,
- a contract test,
- a validation script,
- a CI workflow result,
- an evidence artifact with run identity and provenance.

A checklist item that cannot be mapped to a test, script or evidence artifact is advisory only and must not be used as proof.

## State semantics

| Status | Required meaning |
|---|---|
| `PASS` | Evidence is complete for the stated scope and does not violate relevant invariants. |
| `DEGRADED` | The run is useful for research visibility but cannot authorize full-confidence or production-grade claims. |
| `BLOCKED` | The run cannot support the requested claim. The blocker must be visible and machine-readable. |
| `FAILED` | Runtime or implementation failure. Must not be treated as valid no-trade, degraded evidence or success. |

## Forbidden conversions

The following conversions are forbidden:

| From | To | Reason |
|---|---|---|
| `UNKNOWN` | `PASS` | Unknown is not evidence. |
| `DEGRADED` | `PASS` | Degraded states do not authorize full claims. |
| `BLOCKED` | `NO_TRADE_VALID` | Blocked input is not a valid market decision. |
| `FAILED` | `NO_TRADE_VALID` | Runtime failure is not a valid no-trade day. |
| demo/stub output | real-data evidence | Demo data is not strategy evidence. |

## Evidence traceability minimum

Production-grade evidence must include:

- `run_id`
- `workflow_run_id` or equivalent execution identifier
- `input_data_source`
- `input_data_checksum` or artifact hash
- `symbol_universe`
- `date_range`
- `pipeline_version` or commit SHA
- `runtime_trace` or executed decision-critical module list
- `generator_version`
- `data_mode`: `real`, `demo`, `stub`, or `synthetic`
- `status`: `PASS`, `DEGRADED`, `BLOCKED`, or `FAILED`
- `blocked_reasons` or `degradation_reasons` when not `PASS`

## Promotion rule

A new roadmap phase, strategy rule, backtest conclusion, Paper Observation conclusion or live-readiness statement may be promoted only when:

1. affected system invariants are identified,
2. P0 invariant violations are absent,
3. P1 degraded states are explicitly surfaced,
4. evidence is traceable to reproducible inputs or documented runtime artifacts,
5. forbidden claims are not emitted for degraded/blocked states.

## Over-hardening guardrail

This policy must not make small non-logic changes unnecessarily heavy.

For documentation-only, formatting-only or non-decision-support refactors, the PR may state:

```text
Logic safety impact: none
Affected invariants: none
Reason: no scanner/signal/risk/evidence/backtesting/reporting/runtime behaviour changed
```

That statement must be honest. If runtime behaviour, evidence semantics or claim boundaries change, the full logic-safety process applies.

## Relation to TEST1 and Evidence Quality Gate

TEST1 defines the development order: guard test first, minimal fix, targeted tests, module tests, full suite, documentation.

This policy defines what the guard must protect: system invariants, state semantics, evidence provenance and forbidden claims.

Issue #188 Evidence Quality Gate consumes these outputs before roadmap or strategy promotion.
