# Portfolio Risk Active Enforcement #202

Status date: 2026-06-12

## Scope

#202 records the active enforcement path for portfolio-risk checks in signal generation and trade-plan validation.

## Active files

```text
src/signals/signal_generator.py
src/signals/trade_plan_validator.py
src/portfolio_risk.py
```

## Required inputs

For actionable candidates, portfolio-risk evaluation needs:

```text
symbol
sector
risk_tier
position_size_multiplier
returns_20d
```

`returns_20d` must contain at least 3 numeric values.

## Required evidence fields

Signals must expose:

```text
portfolio_risk_status
portfolio_risk_block_reason
portfolio_risk_multiplier
```

## Required behavior

When portfolio-risk enforcement is required:

```text
missing portfolio context -> NO_TRADE
portfolio heat failure -> NO_TRADE
sector heat failure -> NO_TRADE
passed portfolio risk -> BUY_WATCH with evidence fields
```

## Guard tests

```text
tests/test_202_portfolio_risk_active_path.py
```
