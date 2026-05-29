# BT4 Backtest Result Quality Gate

BT4 adds a result-quality gate after BT3 reproducibility validation.

It answers one operational question:

```text
Is the reported result quality sufficient for continued research or paper observation?
```

BT4 does not claim statistical proof, optimize strategy parameters, approve capital use or connect to external services. It is a fail-closed quality screen for reported historical validation metrics.

## Position in the roadmap

```text
BT1: deterministic backtest contract
BT2: strategy test matrix
BT3: reproducibility contract gate
BT4: result quality gate
```

BT3 checks whether a reported run can be replayed from stable metadata. BT4 checks whether the reported metrics meet minimum quality thresholds before the run is considered for further observation.

## Required case fields

| Field | Purpose |
|---|---|
| `run_id` | Stable result-quality case identifier |
| `strategy_id` | Public-safe strategy family identifier |
| `contract_version` | Related BT3/evidence contract version |
| `trade_count` | Sample size guard |
| `max_drawdown_pct` | Downside quality guard |
| `expectancy_r` | Average expected return per risk unit |
| `profit_factor` | Gross positive result divided by gross negative result |
| `sharpe` | Risk-adjusted summary score |
| `win_rate_pct` | Context metric only, not standalone proof |
| `loss_rate_pct` | Loss-frequency guard |
| `total_return_pct` | Summary return metric |
| `regime_slices` | Market-condition split evidence |
| `tags` | Demo/public-safe boundary |
| `footer` | Research-only boundary |

## Default thresholds

```text
min_trade_count: 30
max_drawdown_pct_floor: -12.0
min_expectancy_r: 0.05
min_profit_factor: 1.15
min_sharpe: 0.75
max_loss_rate_pct: 55.0
min_regime_count: 2
max_single_regime_trade_share_pct: 80.0
```

## Gates

BT4 validates:

- required identity fields are present
- minimum trade count is satisfied
- drawdown is within threshold
- expectancy is positive enough
- profit factor is above threshold
- Sharpe is above threshold
- loss rate is not excessive
- regime split is available
- no single-regime concentration dominates the sample
- demo/public-safe tags are present
- research-only footer is preserved
- at least one case exists
- all cases pass their quality gates

## Demo input

```text
data/demo_backtest_result_quality.json
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

## Output

```text
reports/backtest_result_quality/backtest_result_quality.json
reports/backtest_result_quality/backtest_result_quality.md
```

## Non-goals

BT4 does not:

- prove long-term edge
- replace walk-forward validation
- replace forward paper observation
- expose private scoring logic
- connect to external services
- approve capital use

## Research boundary

```text
Research / Paper Observation Only. Result quality is not execution approval.
```
