# Historical Entry / Stop / Exit Backtest

P24 adds a deterministic historical backtest runner for already-generated long trade plans.

It uses historical daily OHLCV CSV bars produced by P23 Polygon historical ingestion.

---

## Command

```bash
python scripts/run_historical_entry_exit_backtest.py \
  --plans-file reports/signals/latest-signals.json \
  --bars-root data/historical/bars/1day \
  --max-bars 20
```

Custom outputs:

```bash
python scripts/run_historical_entry_exit_backtest.py \
  --plans-file reports/signals/latest-signals.json \
  --json-output reports/backtests/historical-entry-exit-backtest.json \
  --markdown-output reports/backtests/historical-entry-exit-backtest.md
```

---

## Input Trade Plans

The runner accepts JSON in any of these shapes:

```text
[]
{ "plans": [] }
{ "signals": [] }
```

Each actionable long plan needs:

```text
symbol
signal_date, date or created_at
entry_trigger
stop_loss
target_1
```

Optional fields:

```text
signal_id
target_2
valid_until
entry_type
setup_type
stop_model
exit_model
```

Non-`BUY_WATCH` signals are ignored when an `action` field exists.

Invalid long plans are skipped:

```text
missing symbol
missing signal date
missing entry/stop/target
stop_loss >= entry_trigger
entry_trigger >= target_1
```

---

## Historical Bars

Expected location:

```text
data/historical/bars/1day/<SYMBOL>.csv
```

Required columns:

```text
date
open
high
low
close
volume
```

---

## Outcomes

The runner can produce:

```text
ENTRY_NOT_HIT
EXPIRED
STOP_HIT
TARGET_1_HIT
TARGET_2_HIT
```

Same-bar ambiguity is handled conservatively:

```text
if stop and target are touched in the same daily bar, stop wins
```

This avoids optimistic daily-bar backtest bias.

---

## Metrics

The JSON/Markdown report includes:

```text
total
entry_hit_rate
expired_without_entry_rate
stop_hit_rate
target_1_hit_rate
target_2_hit_rate
false_breakout_rate
average_r
expectancy_r
```

---

## Output

Default outputs:

```text
reports/backtests/historical-entry-exit-backtest.json
reports/backtests/historical-entry-exit-backtest.md
```

---

## Limitations

P24 is intentionally conservative and limited:

```text
long-side only
single daily bar resolution
no intraday event ordering
no historical signal generation from scratch
no ML training
no out-of-sample optimization
no broker execution
```

---

## Next Steps

After P24:

```text
P25 Out-of-Sample Validation and Adaptive Feedback Integration
P26 Paper-Live Observation Before Trading
```

Strict rule:

```text
Historical backtest results are evidence, not proof.
No trading decision without out-of-sample validation and paper-live observation.
```
