# Historical Entry Exit Backtest Workflow

This workflow runs the P24 historical Entry / Stop / Exit backtest from GitHub Actions.

It is designed for browser/iPhone operation when local CLI access is not available.

---

## Workflow

```text
Actions → Historical Entry Exit Backtest → Run workflow
```

---

## Inputs

### plan_mode

```text
sample
existing
```

Use `sample` for pipeline smoke validation.

Use `existing` when a real plans/signals JSON file already exists in the repository checkout.

### symbols

Default:

```text
SPY,QQQ,NVDA,AAPL,MSFT,AMD,TSLA,META,GOOGL,AMZN
```

### start_date / end_date

Default 10-year window:

```text
2016-05-22 → 2026-05-22
```

### sample_signal_date

Used only in `plan_mode=sample`.

Default:

```text
2017-01-03
```

### existing_plans_file

Used only in `plan_mode=existing`.

Default:

```text
reports/signals/latest-signals.json
```

### max_bars

Maximum daily bars evaluated after the signal date.

Default:

```text
20
```

---

## What the Workflow Does

```text
1. Checkout repo
2. Setup Python
3. Install requirements
4. Re-ingest historical Polygon bars
5. Create sample plans OR use existing plans file
6. Run historical Entry / Stop / Exit backtest
7. Print Markdown summary
8. Upload artifacts
```

---

## Artifacts

Artifact name:

```text
historical-entry-exit-backtest-artifacts
```

Expected files:

```text
reports/backtests/sample-historical-plans.json
reports/backtests/historical-entry-exit-backtest.json
reports/backtests/historical-entry-exit-backtest.md
data/historical/metadata/ingestion_status.json
```

---

## Required Secret

```text
POLYGON_API_KEY
```

---

## Safety

This workflow does not place trades.

It only:

```text
ingests historical market data
runs deterministic historical simulation
writes reports
uploads artifacts
```

---

## Recommended First Run

```text
plan_mode: sample
symbols: SPY,QQQ,NVDA,AAPL,MSFT,AMD,TSLA,META,GOOGL,AMZN
start_date: 2016-05-22
end_date: 2026-05-22
sample_signal_date: 2017-01-03
max_bars: 20
```

After this is green, use `existing` only when a real signal/plan file exists.

---

## Important Limitation

`sample` plans are deterministic smoke-test plans only.

They are not trading recommendations and should not be used for strategy performance conclusions.

Real validation needs real historical trade plans or historically reconstructed signal snapshots.
