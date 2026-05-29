# BT7 Capacity / Turnover / Realism Gate

BT7 adds a deterministic capacity, turnover and transaction-cost realism gate before any private production sizing work.

BT7 is intentionally research-only. It does not prove production edge, does not approve real-money execution and does not replace forward paper observation.

## What BT7 blocks

BT7 fails closed when historical validation looks attractive but the execution assumptions are not realistic enough for the proposed scale.

The gate checks:

```text
complete run identity
required numeric capacity and turnover metrics
positive proposed capital and symbol count
single-position ADV usage
portfolio ADV usage
average daily turnover
annual turnover
transaction-cost drag versus gross expectancy
net expectancy after costs
average holding-period realism
minimum trade count
slippage-model coverage
artifact hash references
public-safe demo tags
research-only footer
```

## Demo command

```bash
python scripts/generate_bt7_capacity_turnover_report.py --demo
```

## File-based command

```bash
python scripts/generate_bt7_capacity_turnover_report.py \
  --input-json data/demo_bt7_capacity_turnover.json \
  --output-json reports/bt7_capacity_turnover/report.json \
  --output-md reports/bt7_capacity_turnover/report.md
```

## Test command

```bash
pytest tests/test_bt7_capacity_turnover_realism_gate.py -q
```

## Public-safe data policy

Public BT7 examples must remain synthetic or demo-only. Real capacity limits, real private sizing decisions, proprietary liquidity assumptions and non-public execution analytics belong outside the public repository.

## Research-only rule

Every generated BT7 report remains compatible with:

```text
Research / Paper Observation Only. Execution is not authorized by this report.
```
