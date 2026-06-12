# Portfolio Risk Gate Contract

Status date: 2026-06-12

Issue: #182

## Purpose

A valid individual setup is not enough for executable or review-ready signal output.

Portfolio-level heat, sector concentration, correlation exposure and missing portfolio context must be evaluated before an otherwise valid signal can remain executable when portfolio-risk enforcement is required.

## Enforcement path

The gate is enforced in:

```text
src/signals/trade_plan_validator.py
src/signals/signal_generator.py
```

Signal generation calls the portfolio-risk layer through:

```text
src.portfolio_risk.evaluate_portfolio_risk()
```

when `portfolio_risk_required` is enabled by the decision report or explicitly passed to `build_signals()`.

## Required portfolio-risk inputs

For each actionable candidate, portfolio-risk evaluation requires:

```text
symbol
sector
risk_tier
position_size_multiplier
returns_20d
```

`returns_20d` must contain at least 3 numeric values because correlation evaluation is not meaningful without a minimum return series.

## Fail-closed states

The gate blocks an otherwise valid trade plan when:

```text
portfolio_risk_context_missing
portfolio_risk_blocked
```

Common block reasons include:

```text
portfolio_heat_exceeded:<value>
sector_heat_exceeded:<sector>:<value>
high_correlation:<symbol_a>-<symbol_b>:<correlation>
```

## Signal evidence fields

Each exported signal includes:

```text
portfolio_risk_status
portfolio_risk_block_reason
portfolio_risk_multiplier
```

Allowed statuses:

```text
NOT_EVALUATED
NOT_REQUIRED
PASSED
BLOCKED
```

## Runtime boundary

When portfolio-risk is required:

- missing context must not create a `BUY_WATCH` signal
- portfolio heat or concentration failure must downgrade to `NO_TRADE`
- blocked portfolio-risk must set `position_size` to `0.0`
- block evidence must be visible in signal notes and JSON payload

## Safety boundary

This gate is portfolio-risk evidence hardening only.

It does not authorize broker execution, production deployment, capital allocation or live trading.
