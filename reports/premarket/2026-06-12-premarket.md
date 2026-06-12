# Institutional Trading Engine — PREMARKET REPORT

Generated: 2026-06-12 13:44 UTC

## Market Regime

- Data Status: PARTIAL
- Regime: Strong Bullish (VIX proxy degraded)
- Market Health Score: 80

### Core Market Metrics

#### SPY
- Close: 688.98
- SMA50: 681.78 ✅
- SMA200: 636.04 ✅
- ATR14: 6.5

#### QQQ
- Close: 620.76
- SMA50: 616.26 ✅
- SMA200: 568.1 ✅
- ATR14: 8.68

#### VIX
- Close: DATA_UNAVAILABLE
- SMA50: DATA_UNAVAILABLE
- SMA200: DATA_UNAVAILABLE
- ATR14: DATA_UNAVAILABLE

#### VIX_PROXY
- Close: 25.22
- SMA50: 29.14 ❌
- SMA200: 40.96 ❌
- ATR14: 1.07

### Market Breadth
- Universe Size: 16
- Above SMA50: 6
- Breadth %: 37.5%

## Cross-Asset Regime

- Data Status: LIVE
- Cross-Asset Regime: cross_asset_neutral
- Risk Score: 86
- Risk-On Score: 51
- Risk-Off Score: 15

### Cross-Asset Warnings
- defensive_gold_outperformance

### Cross-Asset Confirmations
- usd_pressure_contained
- duration_stress_contained
- small_caps_confirm_risk_appetite
- equity_trend_supportive

### Focus Areas
- US index trend confirmation before open
- VIX risk regime before new exposure
- Leader continuation potential
- Opening gap and volatility risk

## Run Health / Silent-Failure Gate

- Run Health: NO_TRADE_VALID
- Success Status: SUCCESS
- Signal Generation: PASSED
- Scanner Data Quality: OK
- Governance Status: PASSED
- Governance Stage: active_report_path_governance
- Governance Active Path: scripts/generate_report.py::_build_market_payload
- Kill Switch Active: False
- Governance Approval Granted: True
- Live Trading Authorized: False
- Broker Execution Mode: paper_only
- Governance Reasons: none
- Scanner Valid Symbols: 8 / 8
- Reasons: no_actionable_signals_with_complete_data

## Decision Engine

- Market State: low_vol_bull
- Portfolio Heat Limit: 0.0
- Approved / Reduced Size: 0
- Blocked / No Trade: 8

### ⚠️ Hard Overrides Active
- invalid_portfolio_governance_state

> ℹ️ Data feeds partial (Free Polygon tier — VIX unavailable). Data confidence reduced; sizing conservative.

### Active Strategy Types
- momentum_breakout
- pullback_continuation
- speculative_growth

### Decision Summary
- Runtime governance blocked report-path risk approval. The report is defensive only and must not create actionable exposure.

### Ranked Opportunities

- No ranked opportunities qualified for active risk. Decision remains No-Trade / watch mode until setup quality improves.
- Asymmetry Score: n/a — no approved asymmetric setup available.

### 🚫 Blocked / No Trade

- **MSFT**: blocked — invalid_portfolio_governance_state | Asymmetry Score: 0.7
- **NVDA**: blocked — invalid_portfolio_governance_state | Asymmetry Score: 0.7
- **META**: blocked — invalid_portfolio_governance_state | Asymmetry Score: 0.7
- **AAPL**: blocked — invalid_portfolio_governance_state | Asymmetry Score: 0.7
- **MU**: blocked — invalid_portfolio_governance_state | Asymmetry Score: 0.7

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
- Polygon VIX index unavailable; using configured volatility proxy for degraded regime evidence.
- VIX/regime validation is DEGRADED; proxy evidence must not be treated as full VIX validation.
- Some market data feeds failed; report is running in degraded mode.