# CHANGELOG

## Phase B11 Daily Evidence Pipeline — 2026-05-26

### Added
- Daily evidence input contract validator in `src/validation/daily_evidence_input_validation.py`.
- Daily evidence input builder in `src/validation/daily_evidence_input_builder.py`.
- Observation-only source bootstrap in `src/validation/daily_evidence_source_bootstrap.py`.
- CLI tools:
  - `scripts/validate_daily_evidence_inputs.py`
  - `scripts/build_daily_evidence_inputs.py`
  - `scripts/bootstrap_daily_evidence_sources.py`
- Operational documentation:
  - `docs/operations/daily_evidence_input_pipeline.md`
  - `docs/operations/daily_evidence_input_builder.md`
  - `docs/operations/daily_evidence_source_bootstrap.md`

### Tests Added / Updated
- `tests/test_daily_evidence_input_validation.py`
- `tests/test_daily_evidence_input_builder.py`
- `tests/test_daily_evidence_source_bootstrap.py`
- CI workflow includes explicit Phase B11 input pipeline tests.

### Improved
- Daily Evidence workflow no longer uses placeholder component JSONs.
- Workflow now follows a full evidence chain:
  - source bootstrap when explicitly requested for observation-only Day-0 operation
  - input build
  - input validation
  - B1-B6 component report generation
  - daily evidence report generation
  - artifact upload
- Missing or invalid sources fail closed before evidence generation.
- Observation-only bootstrap records are marked as `observation_only_bootstrap` and are not treated as statistically meaningful forward evidence.

### Stabilization Result
- CI status: green.
- Daily Evidence workflow status: green with explicit observation-only bootstrap input.
- B11 status: done.
- B1.1 remains a long-running 3-6 month observation-only evidence period.
- Broker execution remains intentionally not implemented.
- Live trading remains intentionally not authorized by code.

---

## Phase B Real Forward Evidence — 2026-05-25

### Added
- Paper observation daily reconciliation model in `src/validation/paper_observation_reconciliation.py`.
- Performance drift detection engine in `src/validation/performance_drift_detection.py`.
- SPRT-style sequential edge-decay test in `src/validation/sequential_edge_decay.py`.
- Operational documentation:
  - `docs/operations/paper_observation_reconciliation.md`
  - `docs/operations/performance_drift_detection.md`
  - `docs/operations/sequential_edge_decay.md`

### Tests Added / Updated
- `tests/test_paper_observation_reconciliation.py`
- `tests/test_performance_drift_detection.py`
- `tests/test_sequential_edge_decay.py`
- CI workflow now includes explicit Phase B1, B2 and B3 test steps before the full regression suite.

### Improved
- Phase B now has observation-only reconciliation infrastructure.
- Forward paper results can be compared against expected/backtest actions and R values.
- Paper-vs-backtest drift can be monitored through expectancy drift, win-rate drift, cumulative drift and z-score gates.
- Sequential edge-decay testing can distinguish baseline-compatible, degraded, inconclusive and continue-observation states.

### Stabilization Result
- B1 paper observation reconciliation: implemented and CI-green.
- B2 performance drift detection: implemented and CI-green.
- B3 sequential edge-decay testing: implemented and CI-green.
- B1.1 remains a long-running 3-6 month observation-only evidence period.
- Broker execution remains intentionally not implemented.
- Live trading remains intentionally not authorized by code.

---

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
  - `docs/operations/secrets_rotation_policy.md`
  - `docs/operations/phase_a_ci_stabilization.md`

### Tests Added / Updated
- `tests/test_decision_engine.py`
- `tests/test_out_of_sample_lockbox.py`
- `tests/test_slippage_model.py`
- `tests/test_execution_realism.py`
- `tests/test_statistical_robustness.py`
- `tests/test_historical_edge_validation.py`
- `tests/test_polygon_structured_logging.py`
- `tests/test_polygon_data_pipeline.py`
- `tests/test_polygon_cache.py`
- Regression test expectations updated after stricter A5/A6 evidence gates.

### Improved
- Backtest and lockbox evidence now fails closed when the threshold contract is stale.
- Execution realism now separates spread cost from market impact.
- Slippage now scales non-linearly with order size relative to ADV.
- Panic/risk-off regimes now increase execution-cost assumptions.
- Historical edge validation now penalizes multiple testing through Deflated Sharpe probability.
- Historical edge validation can require a positive bootstrap lower bound for expectancy.
- Polygon data workflows now emit machine-readable logs for rate limits, HTTP errors, skipped symbols, failed symbols and run summaries.
- Polygon cache writes now have a safe write primitive for future large data runs.
- Phase A stabilization tests were added to CI before Phase B.
- Full regression suite was executed and fixed until CI green.

### Stabilization Result
- Phase A implementation status: complete.
- Phase A CI stabilization status: green.
- Full regression suite status: green.
- Broker execution remains intentionally not implemented.
- Live trading remains intentionally not authorized by code.
- Phase B may start as observation-only paper evidence collection.

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
