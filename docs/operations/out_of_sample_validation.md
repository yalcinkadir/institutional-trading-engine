# Out-of-Sample Historical Validation

P25 adds a conservative historical validation layer on top of the P24 backtest runner.

It reconstructs deterministic historical trade plans from daily bars and compares in-sample vs. out-of-sample results.

---

## Important Guardrail

P25 does not train a model.

P25 does not change adaptive scoring.

P25 does not authorize trading.

It only produces validation evidence.

---

## Local Command

```bash
python scripts/run_out_of_sample_validation.py \
  --symbols SPY,QQQ,NVDA,AAPL,MSFT,AMD,TSLA,META,GOOGL,AMZN \
  --bars-root data/historical/bars/1day \
  --split-date 2023-01-01 \
  --lookback-bars 20 \
  --every-nth-signal 20 \
  --max-bars 20
```

Outputs:

```text
reports/backtests/reconstructed-historical-plans.json
reports/backtests/out-of-sample-validation.json
reports/backtests/out-of-sample-validation.md
```

---

## GitHub Actions Workflow

```text
Actions → Out-of-Sample Historical Validation → Run workflow
```

Recommended first run:

```text
symbols: SPY,QQQ,NVDA,AAPL,MSFT,AMD,TSLA,META,GOOGL,AMZN
start_date: 2016-05-22
end_date: 2026-05-22
split_date: 2023-01-01
lookback_bars: 20
every_nth_signal: 20
max_bars: 20
```

Artifact:

```text
out-of-sample-validation-artifacts
```

Expected files:

```text
reports/backtests/reconstructed-historical-plans.json
reports/backtests/out-of-sample-validation.json
reports/backtests/out-of-sample-validation.md
data/historical/metadata/ingestion_status.json
```

---

## Reconstruction Method

The first P25 reconstruction method is deliberately simple:

```text
previous lookback high = entry trigger
percentage stop below entry
R-multiple based targets
one signal every N bars
long-side only
```

Defaults:

```text
lookback_bars = 20
every_nth_signal = 20
stop_pct = 5%
target_1 = 2R
target_2 = 4R
```

---

## Split Logic

```text
signal_date < split_date  → in-sample
signal_date >= split_date → out-of-sample
```

---

## Metrics

The report contains metrics for:

```text
all
in_sample
out_of_sample
```

Each segment includes:

```text
total
entry_hit_rate
target_1_hit_rate
target_2_hit_rate
stop_hit_rate
false_breakout_rate
expectancy_r
```

---

## Interpretation

Good in-sample performance alone is not enough.

Required minimum interpretation rule:

```text
If out-of-sample is weak, do not trust the reconstructed rule.
If in-sample is strong but out-of-sample fails, treat it as overfit or regime-dependent.
If both are weak, reject or redesign the rule.
If both are acceptable, continue to paper-live observation.
```

---

## Limitations

```text
long-side only
daily bars only
no intraday event ordering
simple breakout reconstruction only
no optimization
no adaptive scoring update
no broker execution
```

---

## Next Step

After P25 is stable:

```text
P26 Paper-Live Observation Before Trading
```

Strict rule:

```text
No paper-live observation → no trading decision.
```
