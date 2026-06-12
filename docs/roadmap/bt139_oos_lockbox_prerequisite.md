# BT139 OOS Lockbox Prerequisite

Status date: 2026-06-12

Issue: #197

BT139 sample expansion depends on direct OOS lockbox guard coverage.

Required test:

```text
tests/test_197_oos_lockbox_direct.py
```

Required evidence fields:

```text
split_date
purge_days
embargo_days
in_sample_count
out_of_sample_count
unassigned_records
purged_records
embargoed_records
invalidation_reasons
evidence_contract_hash
```

Required manifest fields:

```text
split_parameters
date_ranges
counts
source_records_sha256
report_sha256
evidence_contract_hash
```

Required invalidation reasons:

```text
duplicate_signal_ids
duplicate_record_dates
leaked_symbols
insufficient_in_sample_records
insufficient_out_of_sample_records
purged_overlap_records
embargoed_records
```
