# Institutional Trading Engine — POSTMARKET REPORT

Generated: 2026-05-21 07:59 UTC

## Market Regime

- Data Status: PARTIAL
- Regime: Risk-Off (VIX missing)
- Market Health Score: 20

### Core Market Metrics

#### SPY
- Close: DATA_UNAVAILABLE
- SMA50: DATA_UNAVAILABLE
- SMA200: DATA_UNAVAILABLE
- ATR14: DATA_UNAVAILABLE

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
- Universe Size: 0
- Above SMA50: 0
- Breadth %: 0.0%

## Cross-Asset Regime

- Data Status: FALLBACK
- Cross-Asset Regime: cross_asset_unknown
- Risk Score: 50
- Risk-On Score: 0
- Risk-Off Score: 0

### Cross-Asset Warnings
- cross_asset_data_unavailable: RuntimeError: Polygon request failed after 3 retries: None

### Focus Areas
- Closing trend confirmation
- Sector and leader rotation
- Institutional accumulation / distribution clues
- Risk-off signals after cash close

## Decision Engine

- Market State: risk_off
- Portfolio Heat Limit: 0.5
- Approved / Reduced Size: 8
- Blocked / No Trade: 0

> ℹ️ Data feeds partial (Free Polygon tier — VIX unavailable). Data confidence reduced; sizing conservative.

### Active Strategy Types
- defensive_rotation
- mean_reversion

### Decision Summary
- Decision context allows selective risk-taking in regime-aligned setups.

### Ranked Opportunities

#### MSFT
- Decision: **reduced_size** | Risk Tier: tier_2
- Setup Type: defensive_rotation | Size: 0.25x
- Setup Score: 82.0 | Regime Alignment: 0.82 | Asymmetry Score: 0.72 | Data Confidence: 0.65

#### NVDA
- Decision: **reduced_size** | Risk Tier: tier_2
- Setup Type: defensive_rotation | Size: 0.25x
- Setup Score: 79.0 | Regime Alignment: 0.78 | Asymmetry Score: 0.69 | Data Confidence: 0.65

#### META
- Decision: **reduced_size** | Risk Tier: tier_2
- Setup Type: defensive_rotation | Size: 0.25x
- Setup Score: 76.0 | Regime Alignment: 0.74 | Asymmetry Score: 0.66 | Data Confidence: 0.65

#### AAPL
- Decision: **reduced_size** | Risk Tier: tier_2
- Setup Type: defensive_rotation | Size: 0.25x
- Setup Score: 73.0 | Regime Alignment: 0.7 | Asymmetry Score: 0.63 | Data Confidence: 0.65

#### MU
- Decision: **reduced_size** | Risk Tier: tier_2
- Setup Type: defensive_rotation | Size: 0.25x
- Setup Score: 70.0 | Regime Alignment: 0.66 | Asymmetry Score: 0.6 | Data Confidence: 0.65

#### QQQ
- Decision: **reduced_size** | Risk Tier: tier_2
- Setup Type: defensive_rotation | Size: 0.25x
- Setup Score: 67.0 | Regime Alignment: 0.62 | Asymmetry Score: 0.57 | Data Confidence: 0.65

#### GLD
- Decision: **reduced_size** | Risk Tier: tier_3
- Setup Type: defensive_rotation | Size: 0.125x
- Setup Score: 64.0 | Regime Alignment: 0.58 | Asymmetry Score: 0.54 | Data Confidence: 0.65

#### SLV
- Decision: **reduced_size** | Risk Tier: tier_3
- Setup Type: defensive_rotation | Size: 0.125x
- Setup Score: 61.0 | Regime Alignment: 0.54 | Asymmetry Score: 0.51 | Data Confidence: 0.65

## Post-Market Review

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
- Closing strength validation
- Failed breakout detection
- Swing continuation candidates

### Warnings
- Avoid oversized exposure before macro events.
- Confirm liquidity before entering trades.

### Notes
- Live data source: Polygon.io daily aggregates.
- Breadth currently uses the configured leader universe, not the full S&P 500 universe.
- VIX data unavailable; scoring used a neutral fallback VIX value of 20.0.
- Some market data feeds failed; report is running in degraded mode.