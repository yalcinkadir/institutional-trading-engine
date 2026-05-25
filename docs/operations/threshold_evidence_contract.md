# Threshold Evidence Contract

Decision thresholds are part of the strategy definition. A backtest, walk-forward report or out-of-sample lockbox result is only valid for the threshold version used when the evidence was generated.

## Current threshold source

```text
src/config/thresholds.py
```

The active default version is exposed through:

```python
DEFAULT_THRESHOLDS.version
```

## Why this exists

Changing a cutoff such as setup score, regime alignment, asymmetry, data confidence or position-size multiplier changes the strategy. Old evidence must not silently remain valid after such a change.

This prevents:

- accidental reuse of stale out-of-sample evidence
- threshold tuning without evidence reset
- lockbox leakage through repeated parameter changes
- false confidence from backtests generated under older strategy definitions

## Lockbox behavior

`src/validation/out_of_sample_lockbox.py` now writes the following fields into the report:

```text
threshold_version
evidence_contract_hash
invalidation_reasons
```

The lockbox fails closed when the configured threshold version does not match the active default threshold version.

Example invalidation reason:

```text
stale_threshold_version:2026.05.01-old!=2026.05.25-v1
```

The lockbox can also require records to carry matching threshold metadata by setting:

```python
OutOfSampleLockboxConfig(require_matching_record_threshold_version=True)
```

When enabled, records must include one of:

```text
thresholds_version
threshold_version
decision_thresholds_version
```

Missing or mismatched record-level threshold versions fail the report closed.

## Evidence contract hash

The evidence contract hash is a SHA-256 hash over the lockbox configuration that affects evidence validity:

- split date
- maximum allowed degradation
- historical edge validation config
- threshold version
- record-level threshold-version enforcement flag

If the hash changes, the old report is not the same evidence contract anymore.

## Operational rule

When `THRESHOLDS_VERSION` changes:

1. Treat prior lockbox evidence as stale.
2. Generate new historical evidence.
3. Run walk-forward validation again.
4. Open the out-of-sample lockbox only under the new evidence contract.
5. Keep the new lockbox result locked.

No manual override should mark stale threshold evidence as valid.
