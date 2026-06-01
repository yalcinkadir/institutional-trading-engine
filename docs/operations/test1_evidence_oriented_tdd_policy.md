# TEST1 Evidence-Oriented TDD Policy

Status date: 2026-06-01
Status: Active project policy

## Purpose

TEST1 makes test-first development the default for safety-relevant fixes and external review findings.

A green suite is not enough unless the dangerous path is explicitly covered.

## Core workflow

```text
1. Define the finding or requirement.
2. State the correct invariant.
3. Write the guard test first.
4. Confirm the test represents the unsafe path.
5. Implement the smallest safe fix.
6. Run the targeted test.
7. Run the relevant module tests.
8. Run the full test suite.
9. Update documentation after validation.
```

## Required test layers

```text
Happy path
Dangerous path
Boundary case
Fail-closed invariant
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
Documentation comes after implementation and test validation.
```

## Safety boundary

TEST1 is a development policy only. It does not approve production execution, broker execution or capital allocation.
