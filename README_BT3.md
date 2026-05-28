# BT3 — Reproducibility Contract Gate

BT3 adds a report-level evidence gate for historical validation runs.

It complements the existing deterministic backtest contract by validating whether a reported run has enough pinned metadata to be replayed and audited later.

## What BT3 validates

BT3 checks that each historical validation report includes:

- stable `run_id`
- `strategy_id` and `strategy_version`
- `code_commit_sha`
- `parameter_version`
- `dataset_id` and `dataset_fingerprint`
- replayable symbol set
- valid `start_date` / `end_date`
- explicit `data_mode`
- explicit `execution_model`
- deterministic `seed`
- required result metrics
- required artifact references with SHA-256 fingerprints
- demo/public-safe tags
- research-only footer

## Files

```text
src/validation/backtest_run_contract.py
data/demo_backtest_run_contracts.json
scripts/generate_bt3_contract_report.py
tests/test_bt3_backtest_run_contract.py
docs/operations/bt3_reproducibility_contract.md
```

## CLI

Demo mode:

```bash
python scripts/generate_bt3_contract_report.py --demo
```

File-based mode:

```bash
python scripts/generate_bt3_contract_report.py \
  --input-json data/demo_backtest_run_contracts.json \
  --output-json reports/backtest_run_contract/backtest_run_contract.json \
  --output-md reports/backtest_run_contract/backtest_run_contract.md
```

## Tests

```bash
pytest tests/test_bt3_backtest_run_contract.py -q
pytest -q
```

## Research-only boundary

```text
Research / Paper Observation Only. Execution is not authorized by this report.
```

BT3 does not optimize strategies, claim edge, replace forward paper observation, expose private scoring logic, authorize execution or connect to a broker.
