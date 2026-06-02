# ER10 OOS Purge / Embargo CI-Green Closure — 2026-06-02

Status: closed / CI-green by user confirmation

## Scope

```text
ER10 — Out-of-sample purge / embargo around fixed-date holdout split
```

## TEST1 workflow

```text
real OOS lockbox files inspected
guard test added
minimal implementation added
CI failure inspected
boundary semantics fixed
CI confirmed green
documentation updated after green validation
```

## Finding

```text
A trade that started before the OOS split and exited after the split could be assigned fully to the holdout segment.
```

This can contaminate fixed-date holdout evidence because the trade overlaps the train/test boundary.

## Implemented remediation

The OOS lockbox now supports explicit purge and embargo settings:

```text
purge_days
embargo_days
purged_records
embargoed_records
```

Boundary semantics:

```text
trade starts before split and exits on/after split -> purged
trade exits inside the pre-split purge window -> purged
trade starts on/after split within embargo window -> embargoed
normal post-embargo OOS trades -> holdout segment
```

The report fails closed when purge or embargo removals occur and exposes explicit invalidation reasons:

```text
purged_overlap_records:<count>
embargoed_records:<count>
```

## Files

```text
src/validation/out_of_sample_lockbox.py
tests/test_er10_oos_purge_embargo_guard.py
tests/test_out_of_sample_lockbox.py
```

## Guard coverage

```text
tests/test_er10_oos_purge_embargo_guard.py
```

Validated behavior:

```text
split-spanning trades are purged and not assigned to OOS
post-split embargo-window trades are embargoed, not purged
purge_days and embargo_days are included in JSON, Markdown and evidence contract hash
```

## CI confirmation

The user confirmed CI is green after ER10 implementation, boundary fix and test reconciliation.

Recommended verification commands:

```bash
pytest tests/test_er10_oos_purge_embargo_guard.py -q
pytest tests/test_out_of_sample_lockbox.py -q
pytest tests/test_historical_edge_validation.py -q
pytest -q
```

## Safety boundary

This closure does not authorize live trading, broker execution, capital allocation or production deployment.

The system remains research / decision-support / paper-observation only.
