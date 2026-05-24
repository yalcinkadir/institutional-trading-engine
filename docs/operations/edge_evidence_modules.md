# Edge Evidence Modules

This patch adds four evidence modules on top of the existing validation stack:

```text
src/data/survivorship_universe.py
src/quality/liquidity_filter.py
src/outcomes/forward_outcome_tracker.py
src/macro/vix_adapter.py
```

The purpose is to improve evidence quality before any validation result is treated as meaningful.

## Survivorship universe

`survivorship_universe.py` loads ticker lifecycles and builds point-in-time snapshots. A ticker is considered tradeable only when the tested date is inside its active window.

Expected CSV columns:

```text
symbol,active_from,active_to,delisting_reason,successor_symbol,final_close_price,notes
```

The module can also audit backtest records and flag records whose ticker was not active on the signal date.

## 500+ asset gate

A very small symbol universe is not strong evidence. The patch adds:

```python
validate_universe_coverage(universe, as_of, minimum_tradeable_count=500)
```

and a CLI:

```bash
python scripts/validate_universe_coverage.py \
  --universe data/universe/survivorship_universe.csv \
  --as-of 2024-01-02 \
  --minimum 500
```

If fewer than 500 assets are tradeable on the date, the script exits with status `1`.

## Liquidity filter

`liquidity_filter.py` blocks symbols that do not satisfy basic execution realism assumptions.

Defaults:

| Threshold | Default |
|---|---:|
| minimum average daily dollar volume | 50,000,000 |
| minimum close price | 5 |
| minimum valid bars | 60 |
| maximum zero-volume days | 2 |

Use this before scanner or backtest candidate generation.

## Forward outcome tracker

`forward_outcome_tracker.py` computes realized signal outcomes from forward bars:

- realized entry
- exit reason
- realized R-multiple
- MFE and MAE
- horizon outcomes
- append-only JSONL storage

This closes the learning loop for generated signals.

## VIX adapter

`vix_adapter.py` tries multiple symbol formats for VIX, VIX9D and VIX3M and returns a `VixSnapshot` with a quality level.

Quality levels:

| Quality | Meaning | Decision-engine behavior |
|---|---|---|
| DIRECT | direct implied-vol term structure | trusted |
| PARTIAL | partial implied-vol data | trusted with lower confidence |
| REALIZED_PROXY | SPY realized-vol proxy | ignored unless explicitly allowed |
| UNAVAILABLE | no usable data | ignored |

`decision_engine.py` now exposes:

```python
apply_vix_snapshot_to_context(context, snapshot, allow_realized_proxy=False)
```

This activates VIX safely: direct and partial implied-vol data can update the hard-override input; proxy data does not unless explicitly allowed.

## Tests

Added tests:

```text
tests/test_survivorship_universe.py
tests/test_liquidity_filter.py
tests/test_forward_outcome_tracker.py
tests/test_vix_adapter.py
```

Local validation before PR creation:

```text
24 passed
```

## Next integration steps

1. Add a real point-in-time universe CSV with 500+ assets.
2. Run the universe coverage script before serious validation.
3. Wire liquidity filtering into scanner and backtest candidate selection.
4. Wire VIX snapshot creation into market-context creation.
5. Start appending real signal outcomes to the outcomes journal.
