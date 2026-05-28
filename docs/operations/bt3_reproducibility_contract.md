# BT3 Reproducibility Contract Gate

BT3 adds an evidence gate for historical validation reports.

It answers one operational question:

```text
Can this historical validation result be replayed from stable metadata?
```

The gate does not run a strategy, claim statistical significance, approve capital use or connect to a broker. It validates whether a reported run has enough pinned metadata to be audited later.

## Required contract dimensions

| Dimension | Purpose |
|---|---|
| `run_id` | Stable identifier for the validation run |
| `strategy_id` | Public-safe strategy family identifier |
| `strategy_version` | Version of the evaluated strategy implementation |
| `code_commit_sha` | Git commit used for the run |
| `parameter_version` | Public-safe parameter package version |
| `dataset_id` | Dataset identifier |
| `dataset_fingerprint` | Stable fingerprint of the dataset or manifest |
| `symbols` | Replayable symbol set |
| `start_date` / `end_date` | Historical validation window |
| `data_mode` | Synthetic, paper-observation or historical-demo mode |
| `execution_model` | Explicit fill/price assumption model |
| `seed` | Deterministic replay seed |
| `deterministic` | Whether replay behavior is expected to be deterministic |
| `metrics` | Required summary metrics |
| `artifacts` | Required artifact paths and SHA-256 fingerprints |

## Required metrics

```text
total_return_pct
max_drawdown_pct
sharpe
win_rate_pct
trade_count
```

These values are not proof of edge. They are minimal summary evidence that a run produced a measurable result.

## Required artifacts

```text
input_manifest
result_summary
```

Each artifact reference must include a path and SHA-256 fingerprint.

## Gates

BT3 validates:

- at least one contract exists
- required identity fields are present
- date windows are valid
- code commit SHA is present and well formed
- symbol set is present
- seed is recorded
- deterministic replay is declared
- data and execution modes are explicitly allowed
- required metrics are present and numeric
- required artifacts and SHA-256 fingerprints are present
- contract fingerprints are unique
- demo/public-safe tags are present
- research-only footer is preserved

## Demo input

```text
data/demo_backtest_run_contracts.json
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
```

## Output

```text
reports/backtest_run_contract/backtest_run_contract.json
reports/backtest_run_contract/backtest_run_contract.md
```

## Non-goals

BT3 does not:

- optimize strategy parameters
- replace walk-forward validation
- replace forward paper observation
- expose private scoring logic
- authorize execution
- connect to a broker

## Status

BT3 is a metadata and evidence-contract gate. It makes historical validation auditable before stronger statistical and forward-observation gates are considered.

```text
Research / Paper Observation Only. Execution is not authorized by this report.
```
