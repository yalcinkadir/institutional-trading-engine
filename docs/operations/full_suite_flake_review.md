# Full-Suite Flake Review

Status date: 2026-05-29

## Purpose

This document defines how CI instability is reviewed after the targeted EV, GOV, CL, BT, IP and evidence-guard checks have been split from the residual full regression suite.

## Current CI shape

The pipeline has two layers:

```text
1. Targeted gates for known critical domains
2. Full regression suite residual tests for everything not already covered by targeted gates
```

The residual suite is intentionally not a second full duplicate of all targeted test files. It is a coverage backstop for non-dedicated tests.

## Flake classification

A failed CI run must be classified into one of these categories before retrying repeatedly:

```text
product_failure
regression_failure
environment_failure
timing_or_ordering_flake
external_service_dependency
unknown_flake
```

## Retry policy

```text
one automatic retry is acceptable for environment_failure or timing_or_ordering_flake
no blind repeated retry is allowed for product_failure or regression_failure
unknown_flake requires triage notes before a second retry
```

## Escalation policy

Escalate to a remediation task when any of these conditions are true:

```text
the same test fails twice in consecutive CI runs
the same module flakes more than once in seven days
a failure affects evidence, governance, scoring, backtest, or report-boundary logic
a test requires network, clock, file-system ordering, random seed, or mutable shared state without isolation
```

## Required triage note

A flake triage note must include:

```text
failing test name
CI step name
failure category
first failing commit
reproduction command
retry decision
owner or remediation path
```

## Guarded CI expectations

The following CI expectations must remain true:

```text
targeted EV/GOV/CL/BT/IP gates remain explicit
roadmap and evidence consolidation guards remain explicit
residual full-suite step remains present
residual full-suite step must not silently replace targeted gates
```

## Recommended next action

After this policy is CI-guarded, add an evidence artifact index so generated evidence files, completion documents and CI-green status documents can be found without searching the repository manually.
