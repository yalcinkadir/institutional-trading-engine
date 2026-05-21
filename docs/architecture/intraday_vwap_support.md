# Intraday VWAP Support

P18B adds deterministic VWAP calculation from intraday bars for entry-quality context.

P18A already made VWAP an optional breakout filter when a `vwap` value exists. P18B adds a calculation/enrichment path so VWAP can be produced from intraday aggregate bars.

---

## Components

```text
src/signals/intraday_vwap.py
scripts/generate_report.py
```

Tests:

```text
tests/test_intraday_vwap.py
tests/test_generate_report_intraday_vwap.py
```

---

## VWAP Formula

For each usable intraday bar:

```text
typical_price = (high + low + close) / 3
```

Then:

```text
VWAP = sum(typical_price * volume) / sum(volume)
```

The result is rounded to four decimals.

---

## Supported Bar Formats

Normalized keys:

```text
high
low
close
volume
```

Polygon aggregate keys:

```text
h
l
c
v
```

Invalid bars are ignored.

---

## Failure Behavior

VWAP enrichment is non-fatal.

If intraday bars are missing, invalid, rate-limited, unavailable on the Polygon plan, or have no usable volume:

```text
vwap is not added
report generation continues
signal generation continues
```

This preserves the existing P18A behavior:

```text
if vwap exists and close < vwap for momentum_breakout:
    reject breakout_entry_below_vwap
else:
    missing vwap is non-fatal
```

---

## Report Path

Report generation now includes:

```text
_load_intraday_bars(symbol)
_enrich_metrics_with_intraday_context(metrics, intraday_bars)
normalize_scanner_metrics_map()
build_signals()
```

The intraday loader requests recent 5-minute Polygon aggregate bars when available.

---

## Design Rules

- VWAP calculation is deterministic.
- Intraday data absence must not break reports.
- Entry Quality remains responsible for rejecting breakouts below VWAP.
- The VWAP module does not introduce broker execution or orderflow logic.
- The pipeline supports future alternative intraday data sources.

---

## Next Steps

Future improvements:

```text
configure intraday interval and lookback
session-aware VWAP reset
pre-market vs regular-session VWAP separation
VWAP-based late-breakout rejection
volume imbalance / orderflow confirmation
```
