# B1.1 Daily Evidence Run Record Schema

Status date: 2026-05-29

## Purpose

This document defines the canonical daily run record schema for B1.1 paper-observation evidence operations.

It complements the daily evidence operating procedure and the daily evidence artifact contract.

## Required top-level fields

```text
schema_version
record_type
record_id
commit_sha
run_date_utc
created_at_utc
research_mode
environment
source_summary
input_summary
output_summary
reconciliation_summary
notification_summary
exception_summary
manual_override_summary
sharing_summary
review_summary
```

## Required schema values

```text
schema_version: b11_daily_evidence_run_record_v1
record_type: daily_evidence_run_record
research_mode: paper_observation_only
```

## Environment block

```text
environment.provider_mode
environment.ci_context
environment.local_context
environment.python_version
environment.dependency_snapshot_status
```

## Source summary block

```text
source_summary.source_name
source_summary.source_status
source_summary.source_fingerprint
source_summary.missing_data_count
source_summary.provider_warning_count
```

## Input summary block

```text
input_summary.input_status
input_summary.input_fingerprint
input_summary.validation_status
input_summary.validation_error_count
```

## Output summary block

```text
output_summary.output_status
output_summary.output_fingerprint
output_summary.runtime_report_path
output_summary.generated_artifact_count
```

## Reconciliation summary block

```text
reconciliation_summary.reconciliation_status
reconciliation_summary.drift_status
reconciliation_summary.unmatched_record_count
reconciliation_summary.reconciliation_note
```

## Notification summary block

```text
notification_summary.notification_status
notification_summary.dispatch_record_path
notification_summary.content_review_status
```

## Exception and override blocks

```text
exception_summary.exception_status
exception_summary.exception_record_path
manual_override_summary.manual_override_status
manual_override_summary.manual_override_rationale
```

## Sharing summary block

```text
sharing_summary.repository_status
sharing_summary.example_data_status
sharing_summary.review_status
```

## Review summary block

```text
review_summary.review_status
review_summary.reviewer
review_summary.reviewed_at_utc
review_summary.review_note
```

## Invalid run record conditions

```text
schema_version is missing
record_id is missing
commit_sha is missing
research_mode is not paper_observation_only
source_fingerprint is missing
input_fingerprint is missing
output_fingerprint is missing when output_status is generated
reconciliation_status is missing
repository_status is not reviewed
manual_override_status is present without rationale
```

## Related documents

```text
docs/operations/b11_daily_evidence_operating_procedure.md
docs/operations/b11_daily_evidence_artifact_contract.md
docs/operations/evidence_artifact_index.md
```
