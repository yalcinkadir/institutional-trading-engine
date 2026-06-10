# TEST1 Evidence-Oriented TDD Policy

Status date: 2026-06-11
Status: Active project policy

## Purpose

TEST1 makes test-first development the default for safety-relevant fixes and external review findings.

A green suite is not enough unless the dangerous path is explicitly covered.

For this project, especially around Paper Observation and Backtesting, the target is not to break workflows aggressively. The target is to keep them operationally stable while making their evidence status honest, explicit and audit-ready.

## Core workflow

```text
1. Define the finding or requirement.
2. State the correct invariant.
3. Run the Operational Stability Decision Gate.
4. Write the guard test first.
5. Confirm the test represents the unsafe path.
6. Implement the smallest safe fix.
7. Run the targeted test.
8. Run the relevant module tests.
9. Run the full test suite.
10. Update documentation after validation.
```

## Operational Stability Decision Gate

Before any important decision or safety-relevant change, the implementer must decide which operational outcome is correct.

This gate is mandatory for changes touching:

```text
Paper Observation
Backtesting
Evidence generation
Report generation
Signal persistence
Outcome tracking
Risk / governance gates
CI workflow gates
```

Required decision question:

```text
Should this condition stop the workflow, or should the workflow continue and emit an honest PASS / BLOCKED / DEGRADED artifact?
```

Default rule:

```text
Do not crash or hard-fail operational workflows merely because evidence is not valid.
Prefer a reviewable BLOCKED or DEGRADED artifact when the system can safely explain the problem.
Hard-fail only when continuing would corrupt state, persist unsafe actionable data, or create misleading executable signals.
```

### Allowed evidence states

```text
PASS / VALID
- Inputs are complete.
- Runtime gates were applied.
- Evidence can be interpreted normally.

BLOCKED
- The workflow stayed stable.
- Evidence could not be produced honestly.
- Artifact must include explicit reason codes and zero/empty metrics where appropriate.

DEGRADED
- The workflow stayed stable.
- Evidence is usable only with reduced confidence.
- Artifact must include provenance, fallback and confidence fields.

FAILED
- The workflow or implementation itself malfunctioned.
- This is not a valid substitute for BLOCKED when the condition is expected and diagnosable.
```

### Hard-fail conditions

Hard-fail is required when continuing would create false or unsafe output, for example:

```text
Persisting BUY_WATCH signals with missing close / entry / ATR / stop / target.
Writing actionable reports from missing scanner metrics.
Treating demo or placeholder data as real-data evidence.
Marking non-pipeline-coupled backtests as strategy evidence.
Corrupting existing evidence, state or audit history.
Authorizing live execution from research-only artifacts.
```

### Stable-block conditions

Stable `BLOCKED` artifacts are preferred when the problem is expected or externally caused, for example:

```text
POLYGON_API_KEY missing.
VIX unavailable and no approved fallback is configured.
Validated observations missing for pipeline-coupled BT131 evidence.
No eligible signals exist for outcome tracking.
Historical bars, universe or coverage manifest are missing.
All plans are rejected by validation.
```

In these cases, CI may stay green if and only if the artifact explicitly states the blocked reason and does not claim evidence-grade results.

## Required test layers

```text
Happy path
Dangerous path
Boundary case
Fail-closed invariant
Operational stability invariant
```

The operational stability invariant must prove one of the following:

```text
Valid input -> workflow runs and emits normal evidence.
Expected missing/invalid input -> workflow emits BLOCKED/DEGRADED evidence without fake success.
Unsafe actionable output -> workflow hard-fails before persistence.
```

## External review guards

External review findings should use explicit guard-test names.

```text
tests/test_er<id>_<area>_<risk>_guard.py
```

Examples:

```text
tests/test_er1_backtest_t1_expiry_guard.py
tests/test_er2_backtest_gap_fill_guard.py
tests/test_risk_engine_notional_cap.py
```

## Definition of green

```text
Targeted guard test green
Relevant module tests green
Full suite green
Dangerous path covered
Safety invariant asserted
Operational stability decision documented in code, test or docs
Evidence state is honest: PASS, BLOCKED, DEGRADED or FAILED
```

## Mandatory principles

```text
No fix is complete without a guard test.
No happy-path-only test is sufficient for safety-critical logic.
No missing data should silently become valid evidence.
No valid zero result should be treated as missing data.
Backtest realism assumptions must be tested.
Risk sizing must test notional exposure, not only risk amount.
State or evidence corruption must fail closed.
Operational workflows should remain stable with honest BLOCKED/DEGRADED artifacts when safe.
Do not confuse BLOCKED evidence with failed infrastructure.
Do not convert expected missing inputs into fake metrics.
Do not convert expected missing inputs into unnecessary pipeline crashes.
Documentation comes after implementation and test validation.
```

## Safety boundary

TEST1 is a development policy only. It does not approve production execution, broker execution or capital allocation.
