# Institutional Trading Engine — PREMARKET REPORT

Generated: 2026-05-19 11:08 UTC

## Market Regime

- Data Status: FALLBACK
- Regime: Unknown
- Market Health Score: DATA_UNAVAILABLE

### Core Market Metrics

- SPY: DATA_UNAVAILABLE
- VIX: DATA_UNAVAILABLE
- SMA50: DATA_UNAVAILABLE
- SMA200: DATA_UNAVAILABLE
- ATR14: DATA_UNAVAILABLE

### Market Breadth
- Breadth data unavailable during fallback mode.

## Cross-Asset Regime

- Data Status: LIVE
- Cross-Asset Regime: cross_asset_neutral
- Risk Score: 86
- Risk-On Score: 36
- Risk-Off Score: 0

### Cross-Asset Confirmations
- usd_pressure_contained
- duration_stress_contained
- equity_trend_supportive

### Focus Areas
- US index trend confirmation before open
- VIX risk regime before new exposure
- Leader continuation potential
- Opening gap and volatility risk

## Decision Engine

- Market State: neutral
- Portfolio Heat Limit: 1.0
- Approved / Reduced Size Candidates: 0
- Blocked / No Trade Candidates: 8

### Hard Overrides
- liquidity_stress

### Active Strategy Types
- pullback_continuation
- mean_reversion

### Decision Summary
- Hard risk override active. The report should prioritize defense and avoid new aggressive exposure.

### Ranked Opportunities

#### MSFT
- Decision: blocked
- Risk Tier: no_trade
- Setup Type: pullback_continuation
- Position Size Multiplier: 0.0
- Setup Score: 82
- Regime Alignment: 0.82
- Asymmetry Score: 0.72
- Data Confidence: 0.45

#### NVDA
- Decision: blocked
- Risk Tier: no_trade
- Setup Type: pullback_continuation
- Position Size Multiplier: 0.0
- Setup Score: 79
- Regime Alignment: 0.78
- Asymmetry Score: 0.69
- Data Confidence: 0.45

#### META
- Decision: blocked
- Risk Tier: no_trade
- Setup Type: pullback_continuation
- Position Size Multiplier: 0.0
- Setup Score: 76
- Regime Alignment: 0.74
- Asymmetry Score: 0.66
- Data Confidence: 0.45

#### AAPL
- Decision: blocked
- Risk Tier: no_trade
- Setup Type: pullback_continuation
- Position Size Multiplier: 0.0
- Setup Score: 73
- Regime Alignment: 0.7
- Asymmetry Score: 0.63
- Data Confidence: 0.45

#### MU
- Decision: blocked
- Risk Tier: no_trade
- Setup Type: pullback_continuation
- Position Size Multiplier: 0.0
- Setup Score: 70
- Regime Alignment: 0.66
- Asymmetry Score: 0.6
- Data Confidence: 0.45

## Pre-Market Watchlist

### Watchlist
- MSFT
- NVDA
- META
- AAPL
- MU
- QQQ
- GLD
- SLV

### Objectives
- Gap analysis
- Opening range preparation
- High relative strength leaders

### Warnings
- Avoid oversized exposure before macro events.
- Confirm liquidity before entering trades.

### Notes
- Live market data could not be loaded.
- Error: RuntimeError: Polygon request failed after 3 retries: 403 Client Error: Forbidden for url: https://api.polygon.io/v2/aggs/ticker/I:VIX/range/1/day/2024-12-15/2026-05-19?adjusted=true&sort=asc&limit=260&apiKey=3yCh_HubVOJU8ilguDyfnkCPzRBfab_y