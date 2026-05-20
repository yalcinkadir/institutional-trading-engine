# Historical Validation

Historical validation connects setup/signal research to real Polygon daily aggregate bars.

The goal is not broker simulation. The goal is to falsify whether generated setups produce useful forward follow-through across fixed horizons.

---

## Components

```text
src/data/polygon_client.py
  → get_daily_bars_range()

src/historical_validation.py
  → fetch_historical_bars()
  → run_historical_validation()
  → save_historical_validation_summary()

scripts/run_historical_validation.py
  → CLI wrapper
```

The implementation reuses the existing deterministic backtesting framework:

```text
src/backtesting_framework.py
```

---

## Output

Default output path:

```text
reports/backtests/backtest_summary.json
```

The report includes one metrics block per holding horizon:

```json
{
  "symbols": ["AAPL"],
  "start_date": "2024-01-01",
  "end_date": "2024-12-31",
  "horizons": [5, 10, 20],
  "metrics_by_horizon": [
    {
      "horizon_days": 5,
      "sample_size": 12,
      "win_rate": 0.5833,
      "average_return": 1.42,
      "max_adverse_excursion": -3.8,
      "false_positive_rate": 0.4167
    }
  ]
}
```

---

## Signal Input Format

The CLI expects a JSON list of BacktestSignal-like objects:

```json
[
  {
    "timestamp_utc": "2024-01-02T00:00:00+00:00",
    "symbol": "AAPL",
    "market_state": "risk_on",
    "setup_type": "momentum_breakout",
    "decision": "approved",
    "risk_tier": "tier_1",
    "entry_price": 100.0,
    "position_size_multiplier": 1.0,
    "holding_days": 5
  }
]
```

Required fields:

- `timestamp_utc`
- `symbol`
- `entry_price`

Optional fields default to conservative generic values:

- `market_state`
- `setup_type`
- `decision`
- `risk_tier`
- `position_size_multiplier`
- `holding_days`

---

## Run Example

```bash
python scripts/run_historical_validation.py \
  --signals-file data/backtest_signals.json \
  --symbols AAPL,MSFT,NVDA \
  --start-date 2024-01-01 \
  --end-date 2024-12-31 \
  --horizons 5,10,20 \
  --output reports/backtests/backtest_summary.json
```

Requires:

```text
POLYGON_API_KEY
```

---

## Caching

Historical Polygon responses are cached through `PolygonClient` under:

```text
.cache/polygon/historical/
```

The cache key includes:

- ticker
- range
- adjusted/raw mode
- result limit

This keeps repeated research runs deterministic and avoids unnecessary API calls.

---

## Metrics

| Metric | Meaning |
|---|---|
| `sample_size` | Number of simulated trades for that horizon |
| `win_rate` | Share of trades with return above threshold |
| `average_return` | Mean raw forward return percentage |
| `max_adverse_excursion` | Worst intra-window drawdown from entry |
| `false_positive_rate` | Share of trades with return at or below threshold |

Default win threshold:

```text
0.0 percent
```

---

## Testing Standard

Tests use mocked historical bars and must not call Polygon.

Relevant tests:

```bash
pytest tests/test_historical_validation.py
pytest tests/test_polygon_client_historical_range.py
```

---

## Current Limitations

- Validation uses daily bars only.
- No intraday fill simulation.
- No broker execution.
- No transaction-cost adjustment in the first historical-validation summary layer.
- Signal extraction from live generated signal files is not fully automated yet.

Future work can connect generated machine-readable signals directly into the historical validation input format.
