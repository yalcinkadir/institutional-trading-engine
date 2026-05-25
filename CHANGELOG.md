# CHANGELOG

## Phase A Evidence Hygiene — 2026-05-25

### Added
- `ROADMAP.md` with Phase A-E institutional validation roadmap.
- Versioned decision threshold contract in `src/config/thresholds.py`.
- Threshold-aware decision engine integration.
- Threshold-aware out-of-sample lockbox invalidation.
- Evidence contract hash for lockbox reports.
- Lockbox invalidation reasons:
  - `stale_threshold_version`
  - `missing_record_threshold_versions`
  - `record_threshold_version_mismatch`
- Square-root regime-aware slippage model in `src/execution/slippage_model.py`.
- Execution realism metadata:
  - `slippage_model_version`
  - `slippage_quality`
  - `market_impact_pct`
  - `spread_cost_pct`
  - `slippage_pct`
  - `execution_cost_r`
- Statistical robustness utilities in `src/validation/statistical_robustness.py`.
- Deflated Sharpe probability gate in historical edge validation.
- Bootstrap confidence intervals for expectancy and win rate.
- Polygon structured JSON logging for universe and daily bars scripts.
- Polygon cache locking infrastructure with atomic writes:
  - lock-file acquisition
  - stale lock cleanup
  - timeout handling
  - temp-file write plus `os.replace`
- Operational documentation:
  - `docs/operations/threshold_evidence_contract.md`
  - `docs/operations/slippage_model.md`
  - `docs/operations/statistical_robustness.md`
  - `docs/operations/polygon_structured_logging.md`
  - `docs/operations/polygon_cache_locking.md`

### Tests Added / Updated
- `tests/test_out_of_sample_lockbox.py`
- `tests/test_slippage_model.py`
- `tests/test_execution_realism.py`
- `tests/test_statistical_robustness.py`
- `tests/test_historical_edge_validation.py`
- `tests/test_polygon_structured_logging.py`
- `tests/test_polygon_cache.py`

### Improved
- Backtest and lockbox evidence now fails closed when the threshold contract is stale.
- Execution realism now separates spread cost from market impact.
- Slippage now scales non-linearly with order size relative to ADV.
- Panic/risk-off regimes now increase execution-cost assumptions.
- Historical edge validation now penalizes multiple testing through Deflated Sharpe probability.
- Historical edge validation can require a positive bootstrap lower bound for expectancy.
- Polygon data workflows now emit machine-readable logs for rate limits, HTTP errors, skipped symbols, failed symbols and run summaries.
- Polygon cache writes now have a safe write primitive for future large data runs.

### Notes
- Tests have been written but still need to be executed in CI as part of the Phase A stabilization pass before Phase B starts.
- Broker execution remains intentionally not implemented.
- Live trading remains intentionally not authorized by code.
- Phase B should not start until Phase A tests are added to CI, executed and fixed if needed.

---

## v0.1.1-cloud-scanner
### Added
- Cloudbasierter Market Scanner über GitHub Actions
- Polygon API Integration über GitHub Secrets
- Automatische Markdown-Reports im `reports/`-Ordner
- Zeitstempel im Report-Dateinamen
- RSI(14), ATR(14), ATR%, SMA20, SMA50, SMA200
- RVOL und 20D Return
- Relative Strength Spread vs Benchmark
- Market Regime Summary
- Watchlist Candidates
- Leaders / Aggressive Leaders
- Weak Names
- Setup Readiness
- Data / Risk Warnings
- Telegram Summary nach Workflow-Run
- Telegram Watchlist-Tradeplan mit:
  - Trigger
  - Entry Zone
  - Stop
  - Exit 1
  - Exit 2

### Improved
- Benchmark-Zuordnung nach Asset-Typ verbessert
- GLD/SLV nicht mehr gegen QQQ verglichen
- Telegram-Ausgabe kompakter und mobilfreundlicher gemacht
- Leaders-Sektion in Clean / Aggressive getrennt
- Setup-Labels verfeinert
- Konfiguration in `config.py` strukturiert

### Notes
- VIX ist aktuell noch nicht sauber integriert
- Scanner ist aktuell Analyse-/Screening-System, kein vollständiges Trading-System
- Exit-Logik in Telegram ist aktuell indikativ und regelbasiert
