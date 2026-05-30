# B1.1 Daily Evidence Operating Procedure

Status date: 2026-05-29

## Purpose

This runbook defines the daily operating procedure for the B1.1 observation-only evidence period.

It exists to keep paper observation disciplined, repeatable and auditable while real-money execution remains explicitly unauthorized.

## Operating boundary

```text
mode: observation_only
real_money_execution: prohibited
manual_review_required: true
private_edge_publication: prohibited
```

The daily evidence procedure must never imply live trading authorization, portfolio automation authorization or production-readiness.

## Daily sequence

1. Confirm repository and local environment are on the intended commit.
2. Confirm required non-secret configuration is present.
3. Confirm no private edge configuration is being committed or printed.
4. Run daily evidence input validation.
5. Build the daily evidence input package.
6. Run daily paper observation source collection.
7. Run paper observation reconciliation.
8. Generate daily evidence report.
9. Record pass/fail status and exceptions.
10. Send only research-safe notification summaries when configured.
11. Store generated runtime reports outside committed public report example paths.
12. Record any drift, missing data, reconciliation difference, provider issue or manual override.

## Required checks

Each daily run must document:

```text
commit_sha
run_date
observation_mode
input_validation_status
source_collection_status
reconciliation_status
daily_evidence_status
runtime_report_location
notification_status
exceptions_or_manual_overrides
```

## Fail-closed conditions

The daily run must be treated as failed or incomplete when any of these conditions are true:

```text
input validation fails
source collection is incomplete
reconciliation is not clean
required evidence artifact is missing
runtime report path points to committed public examples
notification content implies live trading authorization
private edge values are exposed
manual override is present without rationale
```

## Allowed notification content

Allowed notification summaries may include:

```text
observation-only status
evidence pass/fail summary
reconciliation status
missing-data warnings
drift warnings
report availability
```

Disallowed notification summaries include:

```text
live trading approval
production readiness claims
private edge thresholds
private scoring weights
private setup maps
private target profiles
broker execution instructions
```

## Escalation rules

Escalate to remediation when:

```text
the same evidence step fails twice consecutively
reconciliation drift repeats across two observation days
source collection fails because of provider contract or schema drift
a notification would expose private edge or live-trading implication
a generated report attempts to overwrite committed public examples
```

## Completion criteria for the observation period

B1.1 remains in progress until the configured observation period is complete and the accumulated evidence is reviewed.

Completion requires:

```text
observation window completed
daily evidence artifacts available
daily reconciliation reviewed
drift log reviewed
provider issues reviewed
manual overrides reviewed
no live authorization granted by code
```

## Related guards

```text
tests/test_b11_evidence_operation_discipline.py
tests/test_paper_observation_reconciliation.py
tests/test_daily_evidence_input_validation.py
tests/test_daily_evidence_input_builder.py
tests/test_daily_paper_observation_source.py
tests/test_daily_evidence_report.py
tests/test_report_output_boundary.py
tests/test_generate_report_output_boundary.py
```

## Next recommended action

Add a CI guard test to ensure this operating procedure retains observation-only boundaries, required daily checks and fail-closed conditions.
