# RGP10 Latest Bar Ordering Guard

Status date: 2026-06-01

## Purpose

RGP10 prevents watcher lifecycle decisions from depending on provider response order.

Before RGP10, `latest_bars_to_price_map()` selected `bars_list[-1]`. That is unsafe when provider data arrives unsorted.

## Implemented guard

The watcher now selects the latest bar using timestamp ordering before converting the bar into a `PriceBar`.

Supported timestamp sources:

- numeric Polygon-style `t` timestamp
- ISO-like `timestamp`, `datetime` or `date` fields
- unknown timestamps sort behind known timestamps

## Updated code

```text
src/watchers/entry_exit_watcher.py
```

## Regression coverage

```text
tests/test_entry_exit_watcher.py
```

Coverage includes:

- unsorted numeric timestamps
- ISO/date timestamp fallback
- known timestamp preferred over unknown timestamp

## Live trading authorization

RGP10 does not authorize live trading. It only hardens research/paper lifecycle evaluation against provider ordering drift.
