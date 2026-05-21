# Institutional Trading Engine — PREMARKET REPORT

Generated: 2026-05-21 11:00 UTC

## Market Regime

- Data Status: PARTIAL
- Regime: Neutral (VIX missing)
- Market Health Score: 60

### Core Market Metrics

#### SPY
- Close: 681.92
- SMA50: 678.5 ✅
- SMA200: 626.91 ✅
- ATR14: 5.66

#### QQQ
- Close: 614.31
- SMA50: 616.37 ❌
- SMA200: 557.8 ✅
- ATR14: 7.31

#### VIX
- Close: DATA_UNAVAILABLE
- SMA50: DATA_UNAVAILABLE
- SMA200: DATA_UNAVAILABLE
- ATR14: DATA_UNAVAILABLE

### Market Breadth
- Universe Size: 5
- Above SMA50: 3
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

- Market State: neutral
- Portfolio Heat Limit: 1.0
- Approved / Reduced Size: 6
- Blocked / No Trade: 0

> ℹ️ Data feeds partial (Free Polygon tier — VIX unavailable). Data confidence reduced; sizing conservative.

### Active Strategy Types
- pullback_continuation
- mean_reversion

### Decision Summary
- Decision context allows selective risk-taking in regime-aligned setups.

### Ranked Opportunities

#### MSFT
- Decision: **approved** | Risk Tier: tier_2
- Setup Type: pullback_continuation | Size: 0.5x
- Setup Score: 82.0 | Regime Alignment: 0.82 | Asymmetry Score: 0.72 | Data Confidence: 0.65

#### NVDA
- Decision: **approved** | Risk Tier: tier_2
- Setup Type: pullback_continuation | Size: 0.5x
- Setup Score: 79.0 | Regime Alignment: 0.78 | Asymmetry Score: 0.69 | Data Confidence: 0.65

#### META
- Decision: **approved** | Risk Tier: tier_2
- Setup Type: pullback_continuation | Size: 0.5x
- Setup Score: 76.0 | Regime Alignment: 0.74 | Asymmetry Score: 0.66 | Data Confidence: 0.65

#### AAPL
- Decision: **approved** | Risk Tier: tier_2
- Setup Type: pullback_continuation | Size: 0.5x
- Setup Score: 73.0 | Regime Alignment: 0.7 | Asymmetry Score: 0.63 | Data Confidence: 0.65

#### MU
- Decision: **approved** | Risk Tier: tier_2
- Setup Type: pullback_continuation | Size: 0.5x
- Setup Score: 70.0 | Regime Alignment: 0.66 | Asymmetry Score: 0.6 | Data Confidence: 0.65

#### QQQ
- Decision: **approved** | Risk Tier: tier_2
- Setup Type: pullback_continuation | Size: 0.5x
- Setup Score: 67.0 | Regime Alignment: 0.62 | Asymmetry Score: 0.57 | Data Confidence: 0.65

#### GLD
- Decision: **watch** | Risk Tier: tier_3
- Setup Type: pullback_continuation | Size: 0.25x
- Setup Score: 64.0 | Regime Alignment: 0.58 | Asymmetry Score: 0.54 | Data Confidence: 0.65

#### SLV
- Decision: **watch** | Risk Tier: tier_3
- Setup Type: pullback_continuation | Size: 0.25x
- Setup Score: 61.0 | Regime Alignment: 0.54 | Asymmetry Score: 0.51 | Data Confidence: 0.65

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