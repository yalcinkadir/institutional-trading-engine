# BT132 Strategy Improvement Report

## Evidence Contract

- Report version: bt132.v1
- Source evidence: reports/backtests/real-data-backtest-evidence.json
- Run ID: bt131-real-data-manual
- Data source: real_data
- Is demo: False
- Input pack gate: PASSED
- Input completeness: OK
- Run health: OK
- Total trades: 24
- Review status: READY_FOR_REVIEW

## Portfolio Metrics

- expectancy_r: 0.2763
- average_r: 0.2763
- entry_hit_rate: 0.9583
- stop_hit_rate: 0.5
- target_1_hit_rate: 0.4583
- target_2_hit_rate: 0.25
- false_breakout_rate: 0.5

## Best Symbols by Expectancy

| Symbol | Trades | Expectancy R | Stop Rate | T2 Rate | False Breakout Rate |
|---|---|---|---|---|---|
| GLD | 3 | 0.8335 | 0.3333 | 0.3333 | 0.6667 |
| AAPL | 3 | 0.7126 | 0.3333 | 0.3333 | 0.3333 |
| NVDA | 3 | 0.6975 | 0.3333 | 0.3333 | 0.6667 |
| QQQ | 3 | 0.4673 | 0.0 | 0.0 | 0.3333 |
| META | 3 | 0.3333 | 0.6667 | 0.3333 | 0.3333 |

## Worst Symbols by Expectancy

| Symbol | Trades | Expectancy R | Stop Rate | T2 Rate | False Breakout Rate |
|---|---|---|---|---|---|
| MSFT | 3 | -1.0225 | 1.0 | 0.0 | 1.0 |
| SLV | 3 | -0.1446 | 0.6667 | 0.3333 | 0.3333 |
| META | 3 | 0.3333 | 0.6667 | 0.3333 | 0.3333 |
| MU | 3 | 0.3333 | 0.6667 | 0.3333 | 0.3333 |
| QQQ | 3 | 0.4673 | 0.0 | 0.0 | 0.3333 |

## Entry Findings

- Entry not hit count: 1
- Entry not hit rate: 0.0417
- False breakout count: 12
- False breakout rate: 0.5

## Stop-Loss Findings

- Stop hit count: 12
- Stop hit rate: 0.5

## Exit Findings

- Target 1 without Target 2 count: 5
- Target 1 without Target 2 rate: 0.2083
- Target 2 hit count: 6
- Target 2 hit rate: 0.25

## Recommendations

### HIGH - entry

- Finding: False-breakout rate is elevated.
- Next test: Compare current breakout trigger against stricter confirmation variants before changing production rules.

### HIGH - stop_loss

- Finding: Stop-hit rate is elevated.
- Next test: Run a guarded comparison of fixed stop vs wider ATR-based stop and same-bar stop handling.

### MEDIUM - symbol_selection

- Finding: Worst symbol by expectancy is MSFT.
- Next test: Run symbol-level exclusion/sizing sensitivity before excluding any symbol.

Research only. No live trading authorization.
