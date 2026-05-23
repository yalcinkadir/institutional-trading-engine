# Manual Portfolio Sync

P31 adds a broker-free manual portfolio synchronization layer.

The goal is to make governance risk fields operational without connecting to a broker API.

## Scope

This feature is intentionally limited to decision support.

- No broker API integration
- No order execution
- No trading authorization
- Manual snapshot input only
- Governance-compatible `data/portfolio_state.json` output

## Input

Default example:

```text
data/manual_portfolio_snapshot.example.json
```

Required fields:

```json
{
  "equity_start": 100000.0,
  "equity_peak": 103000.0,
  "equity_previous_close": 101500.0,
  "equity_current": 100700.0,
  "positions": []
}
```

Optional fields:

```json
{
  "snapshot_time": "2026-05-23T20:00:00Z",
  "source": "manual_example_no_broker_api",
  "cash": 75000.0
}
```

Position object:

```json
{
  "symbol": "SPY",
  "quantity": 10,
  "market_value": 5200.0,
  "unrealized_pnl": 120.0,
  "side": "long"
}
```

Supported side values:

```text
long, short, cash, hedge
```

## Calculated Fields

The sync calculates:

```text
drawdown_percent = max(0, (equity_peak - equity_current) / equity_peak * 100)
daily_loss_percent = max(0, (equity_previous_close - equity_current) / equity_previous_close * 100)
total_position_value = sum(position.market_value)
total_unrealized_pnl = sum(position.unrealized_pnl)
```

If `equity_peak` is below `equity_current`, the current equity is used as the drawdown reference and a warning is emitted.

## CLI

```bash
python scripts/sync_manual_portfolio_state.py \
  --snapshot data/manual_portfolio_snapshot.example.json \
  --portfolio-state-out data/portfolio_state.json \
  --report-json-out reports/portfolio/manual-portfolio-sync.json \
  --report-md-out reports/portfolio/manual-portfolio-sync.md
```

## GitHub Actions

Manual workflow:

```text
Actions → Manual Portfolio Sync → Run workflow
```

Artifact:

```text
manual-portfolio-sync-artifacts
```

The artifact contains:

```text
data/portfolio_state.json
reports/portfolio/manual-portfolio-sync.json
reports/portfolio/manual-portfolio-sync.md
```

## Governance Impact

The generated `portfolio_state.json` is compatible with the runtime governance layer.

It enables the existing drawdown and daily loss gates to use calculated values instead of static placeholders.

## Failure Modes

The sync fails explicitly when:

- required equity fields are missing
- numeric fields are invalid or non-finite
- equity reference values are non-positive
- positions are not objects
- position symbol is missing
- position side is unsupported

## Non-Goals

- Broker integration
- Account login
- Position reconciliation with a broker
- Automatic order sizing from live broker data
- Order execution
- Trading authorization
