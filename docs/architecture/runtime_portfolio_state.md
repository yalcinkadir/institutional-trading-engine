# Runtime Portfolio State

`LiveRuntimeCycle` uses portfolio state to make governance checks operational.

Without portfolio state, drawdown and daily-loss governance can only use fallback values. With portfolio state, the runtime can enforce real risk limits before creating and persisting institutional decisions.

---

## File Location

Runtime reads the live state from:

```text
data/portfolio_state.json
```

An example file is available at:

```text
data/portfolio_state.example.json
```

Copy it before live use:

```bash
cp data/portfolio_state.example.json data/portfolio_state.json
```

---

## Expected JSON Shape

```json
{
  "equity_start": 10000.0,
  "equity_current": 9900.0,
  "drawdown_percent": 1.0,
  "daily_loss_percent": 0.25,
  "open_positions": [
    {
      "symbol": "EXAMPLE",
      "side": "long",
      "entry": 100.0,
      "current": 101.0,
      "risk_amount": 100.0,
      "unrealized_pnl": 10.0
    }
  ],
  "updated_at": "2026-05-20T22:00:00+02:00",
  "source": "manual_example"
}
```

---

## Required Fields

| Field | Purpose |
|---|---|
| `equity_start` | Reference equity for the current tracking period |
| `equity_current` | Current portfolio equity |
| `drawdown_percent` | Current portfolio drawdown percentage consumed by kill switch / risk limits |
| `daily_loss_percent` | Current daily loss percentage consumed by risk limits |
| `open_positions` | Optional list of open positions for audit context |
| `updated_at` | Timestamp of the last state update |

---

## Governance Behavior

`LiveRuntimeCycle` loads `data/portfolio_state.json` when no explicit runtime override is supplied.

The loaded values are passed into:

- `evaluate_kill_switch()`
- `validate_risk_limits()`

If governance blocks a cycle, the portfolio state is persisted inside the governance-block event payload.

If governance allows a cycle, the portfolio state is persisted inside the decision log payload.

---

## Missing File Behavior

If `data/portfolio_state.json` is missing, runtime does not crash.

Instead, `PortfolioStateStore` returns a conservative fallback:

```text
source = conservative_missing_portfolio_state_fallback
warnings = ["Portfolio state file missing..."]
```

The fallback uses zero drawdown and zero daily loss, but prints and persists a visible warning.

This is intentionally non-fatal for research workflows, but live operation should maintain the file.

---

## Invalid File Behavior

The runtime fails explicitly if the file exists but is invalid.

Examples of invalid state:

- malformed JSON
- JSON array instead of object
- missing required fields
- non-numeric risk values
- `NaN` or infinite values
- `open_positions` not being a list

Invalid portfolio state should not silently fall back because that would hide a broken risk control input.

---

## Runtime Argument Overrides

`LiveRuntimeCycle.run()` still accepts explicit values:

```python
cycle.run(
    metrics_map=metrics_map,
    vix_data=vix_data,
    portfolio_drawdown_percent=1.0,
    daily_loss_percent=0.5,
)
```

When those arguments are supplied, they override the file-backed state and a warning is attached:

```text
source = runtime_argument_override
```

For live governance, prefer `data/portfolio_state.json`.

---

## Current Limitation

The portfolio state is currently file-backed and must be updated by a caller, workflow, or future broker/account integration.

This implementation makes governance consume real state, but it does not yet calculate account equity automatically from broker execution data.

Future target:

```text
Broker/account data → PortfolioStateStore → Governance → DecisionLog
```
