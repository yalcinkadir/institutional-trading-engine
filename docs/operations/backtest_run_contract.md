# BT1 — Deterministic Backtest Run Contract

BT1 defines a deterministic, versioned contract for every backtest run.

The goal is reproducibility before strategy scenario testing starts.

## Captured fields

```text
strategy id
strategy version
universe id
symbol list
date window
data source version
configuration version labels
execution assumptions
benchmark id
run purpose
metadata
```

The generated `contract_id` is stable across timestamp changes.

## CLI

```bash
python scripts/validate_backtest_contract.py input.json output.json
```

The CLI validates the input contract and writes a normalized JSON contract with a stable `contract_id`.

## Safety

```text
No broker call
No order execution
No live trading authorization
No private edge parameters
```

Public contracts should use demo identifiers or version labels. Real private-edge configuration stays outside the public repository.
