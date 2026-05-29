# BT4 — Backtest Result Quality Gate

BT4 adds a fail-closed result-quality screen after BT3 reproducibility validation.

BT3 answers:

```text
Can the reported run be reproduced?
```

BT4 answers:

```text
Is the reported result quality sufficient for continued research or paper observation?
```

## What BT4 validates

BT4 checks each public-safe demo quality case for:

- minimum trade count
- maximum drawdown boundary
- positive expectancy
- minimum profit factor
- minimum Sharpe
- maximum loss rate
- available regime split
- no single-regime concentration
- demo/public-safe tags
- research-only footer

## Files

```text
src/validation/backtest_result_quality_gate.py
data/demo_backtest_result_quality.json
scripts/generate_bt4_quality_report.py
tests/test_bt4_backtest_result_quality_gate.py
docs/operations/bt4_backtest_result_quality_gate.md
```

## CLI

Demo mode:

```bash
python scripts/generate_bt4_quality_report.py --demo
```

File-based mode:

```bash
python scripts/generate_bt4_quality_report.py \
  --input-json data/demo_backtest_result_quality.json \
  --output-json reports/backtest_result_quality/backtest_result_quality.json \
  --output-md reports/backtest_result_quality/backtest_result_quality.md
```

## Tests

```bash
pytest tests/test_bt4_backtest_result_quality_gate.py -q
pytest -q
```

## Research-only boundary

```text
Research / Paper Observation Only. Result quality is not execution approval.
```

BT4 does not prove long-term edge, replace walk-forward validation, replace forward paper observation, expose private scoring logic or connect to external services.
