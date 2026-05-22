# Historical Polygon Data Ingestion

P23 adds historical Polygon aggregate ingestion as the foundation for backtesting and strategy validation.

The first implementation supports daily OHLCV bars. It is intentionally not a backtest runner and not an ML training module.

---

## Command

```bash
python scripts/ingest_historical_polygon.py \
  --symbols NVDA,AAPL,SPY \
  --start-date 2012-01-01 \
  --end-date 2026-05-22
```

Machine-readable output:

```bash
python scripts/ingest_historical_polygon.py \
  --symbols NVDA,AAPL,SPY \
  --start-date 2012-01-01 \
  --end-date 2026-05-22 \
  --json
```

Required environment variable:

```text
POLYGON_API_KEY
```

---

## Storage Layout

Current storage uses CSV plus JSON metadata:

```text
data/historical/bars/1day/NVDA.csv
data/historical/bars/1day/AAPL.csv
data/historical/metadata/ingestion_status.json
```

CSV is used because the current project dependencies include pandas but do not include a Parquet engine such as `pyarrow` or `fastparquet`.

Parquet can be added later as a performance/storage improvement.

---

## Stored Columns

Each stored bar contains:

```text
date
timestamp
open
high
low
close
volume
```

Polygon aggregate keys are normalized from:

```text
t -> timestamp/date
o -> open
h -> high
l -> low
c -> close
v -> volume
```

---

## Metadata

Ingestion status is written to:

```text
data/historical/metadata/ingestion_status.json
```

Each symbol/timespan key stores:

```text
symbol
timespan
multiplier
start_date
end_date
rows_fetched
rows_written
output_path
status
message
last_updated_at
```

Statuses:

```text
ok     -> usable bars were fetched and written
empty  -> Polygon returned no usable bars
error  -> request, API key or storage error
```

---

## Duplicate Handling

If ingestion is run multiple times, existing and new bars are merged by:

```text
timestamp
```

Duplicate timestamps are removed and rows are sorted by timestamp.

---

## CI / Tests

Tests use mocked Polygon responses only. CI does not call the live Polygon API.

Test file:

```text
tests/test_polygon_historical_ingestion.py
```

Covered behavior:

```text
URL construction
Polygon bar normalization
duplicate removal
CSV writing
metadata writing
empty responses
missing API key
batch ingestion counts
```

---

## Design Rules

- No live API calls in tests.
- No broker execution.
- No ML training in ingestion.
- No backtest decisions in ingestion.
- Historical data must be reproducible and auditable.
- Empty or failed ingestion must be visible in metadata.

---

## Next Steps

After P23:

```text
P24 Historical Entry / Stop / Exit Backtest Runner
P25 Out-of-Sample Validation and Adaptive Feedback Integration
P26 Paper-Live Observation Before Trading
```
