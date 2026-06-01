# BT8 Backtesting Evidence Report

Status date: 2026-06-01
Status: implemented / CI-wired

## Purpose

BT8 turns reproducible BT3 backtest run contracts into an audit-friendly Backtesting Evidence Report.

The report is research / paper-observation evidence only. It does not authorize live trading.

## Inputs

```text
BT3 backtest run contracts JSON
```

The input must contain deterministic backtest run contracts with pinned code version, parameter version, dataset fingerprint, symbol set, date range, seed, metrics and artifact hashes.

## Outputs

```text
BT8 JSON report
BT8 Markdown report
```

The report includes:

```text
- report version
- generated timestamp
- overall PASS / FAIL status
- run count
- strategy count
- dataset count
- symbol count
- total trade count
- average return percent
- average win rate percent
- average Sharpe
- worst max drawdown percent
- BT3 gate results
- run-level metrics
- limitations
- live-trading authorization guard
```

## CLI

```bash
python scripts/generate_backtesting_evidence_report.py \
  --contracts-json reports/backtest_run_contract/contracts.json \
  --output-json reports/backtesting_evidence/bt8_report.json \
  --output-md reports/backtesting_evidence/bt8_report.md
```

## Tests

```bash
pytest tests/test_bt8_backtesting_evidence_report.py -q
```

## Live trading authorization

Unchanged. The project remains research / paper / evidence infrastructure only. Live trading is not authorized by code.
