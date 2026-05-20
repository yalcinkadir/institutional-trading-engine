# Institutional Trading Engine — PREMARKET REPORT

Generated: 2026-05-20 13:28 UTC

## Market Regime

- Data Status: PARTIAL
- Regime: Bullish (VIX missing)
- Market Health Score: 75

### Core Market Metrics

#### SPY
- Close: 687.01
- SMA50: 678.29 ✅
- SMA200: 626.34 ✅
- ATR14: 5.81

#### QQQ
- Close: 619.43
- SMA50: 616.32 ✅
- SMA200: 557.14 ✅
- ATR14: 7.48

### Market Breadth
- Universe Size: 10
- Above SMA50: 6
- Breadth %: 60.0%

## Cross-Asset Regime

- Data Status: FALLBACK
- Cross-Asset Regime: cross_asset_unknown
- Risk Score: 50
- Risk-On Score: 0
- Risk-Off Score: 0

### Cross-Asset Warnings
- cross_asset_data_unavailable: RuntimeError: Polygon request failed after 3 retries: None

### Focus Areas
- US index trend confirmation before open
- VIX risk regime before new exposure
- Leader continuation potential
- Opening gap and volatility risk

## Decision Engine

- Market State: low_vol_bull
- Portfolio Heat Limit: 1.0
- Approved / Reduced Size Candidates: 0
- Blocked / No Trade Candidates: 8

### Hard Overrides
- liquidity_stress

### Active Strategy Types
- momentum_breakout
- pullback_continuation
- speculative_growth

### Decision Summary
- Hard risk override active. The report should prioritize defense and avoid new aggressive exposure.

### Ranked Opportunities

#### MSFT
- Decision: blocked
- Risk Tier: no_trade
- Setup Type: momentum_breakout
- Position Size Multiplier: 0.0
- Setup Score: 82
- Regime Alignment: 0.82
- Asymmetry Score: 0.72
- Data Confidence: 0.45

#### NVDA
- Decision: blocked
- Risk Tier: no_trade
- Setup Type: momentum_breakout
- Position Size Multiplier: 0.0
- Setup Score: 79
- Regime Alignment: 0.78
- Asymmetry Score: 0.69
- Data Confidence: 0.45

#### META
- Decision: blocked
- Risk Tier: no_trade
- Setup Type: momentum_breakout
- Position Size Multiplier: 0.0
- Setup Score: 76
- Regime Alignment: 0.74
- Asymmetry Score: 0.66
- Data Confidence: 0.45

#### AAPL
- Decision: blocked
- Risk Tier: no_trade
- Setup Type: momentum_breakout
- Position Size Multiplier: 0.0
- Setup Score: 73
- Regime Alignment: 0.7
- Asymmetry Score: 0.63
- Data Confidence: 0.45

#### MU
- Decision: blocked
- Risk Tier: no_trade
- Setup Type: momentum_breakout
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
- Live data source: Polygon.io daily aggregates.
- Breadth currently uses the configured leader universe, not the full S&P 500 universe.
- VIX data unavailable; scoring used a neutral fallback VIX value of 20.0.
- Some market data feeds failed; report is running in degraded mode.