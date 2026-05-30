# B1.1 Daily Evidence Artifact Contract

Status date: 2026-05-29

## Purpose

This contract defines the minimum structure for daily evidence artifacts created during the B1.1 paper-observation period.

The goal is to make every daily evidence artifact auditable, reproducible and public-safe.

## Artifact scope

A daily evidence artifact is any generated record that summarizes one observation day, including:

```text
daily evidence JSON
daily evidence markdown
paper observation source snapshot
paper observation reconciliation record
notification dispatch record
runtime exception note
manual override note
```

## Required metadata

Every daily evidence artifact must include or link to:

```text
artifact_type
artifact_version
commit_sha
run_date_utc
created_at_utc
research_mode
source_name
source_fingerprint
input_fingerprint
output_fingerprint
reconciliation_status
evidence_status
manual_override_status
private_edge_status
public_safety_status
```

## Required status values

The following status values must be explicit:

```text
research_mode: paper_observation_only
private_edge_status: clean
public_safety_status: public_safe
```

The artifact must not use ambiguous values such as:

```text
production_ready
approved
ready
complete_without_review
```

## Required evidence references

Each daily evidence artifact must reference the relevant run inputs and outputs:

```text
input_source_path
runtime_report_path
reconciliation_record_path
notification_record_path
exception_record_path
```

If a reference does not exist for the day, the field must still be present with an explicit unavailable or not_applicable value.

## Invalid artifact conditions

The daily evidence artifact is invalid when any of these conditions are true:

```text
commit_sha is missing
run_date_utc is missing
research_mode is not paper_observation_only
private_edge_status is not clean
public_safety_status is not public_safe
reconciliation_status is missing
runtime_report_path points to committed public report examples
manual_override_status is present without rationale
source_fingerprint or input_fingerprint is missing
output_fingerprint is missing for generated reports
```

## Public repository boundary

Daily evidence artifacts committed to the public repository must be synthetic or public-safe. Real provider outputs, real ranked opportunity reports, private thresholds, private scoring weights and proprietary setup maps must not be committed.

## Review checklist

Before a daily evidence artifact is accepted as valid, check:

```text
metadata complete
paper-observation-only mode explicit
private edge status clean
public safety status public_safe
reconciliation status present
runtime report path safe
manual overrides explained
fingerprints present
notification content research-only
```

## Related operating procedure

```text
docs/operations/b11_daily_evidence_operating_procedure.md
```

## Related guards

```text
tests/test_b11_daily_evidence_artifact_contract.py
tests/test_b11_daily_evidence_operating_procedure.py
tests/test_evidence_artifact_index.py
```
