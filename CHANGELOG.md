# CHANGELOG

## SR4 Trusted Portfolio Governance Source — 2026-05-31

### Fixed
- SR4: runtime portfolio override arguments no longer mark portfolio governance as valid.
- `portfolio_drawdown_percent` and `daily_loss_percent` supplied directly to `LiveRuntimeCycle.run()` are treated as untrusted runtime arguments and fail closed.
- Governance now requires a trusted portfolio-state source such as `PortfolioStateStore` / `data/portfolio_state.json` before runtime checks can pass.

### Added
- Regression coverage proving runtime portfolio argument overrides are rejected with `runtime_argument_override_rejected`.
- Regression coverage proving valid runtime-cycle tests use an injected trusted portfolio-state store instead of runtime governance overrides.

### Stabilization Result
- SR4 implementation status: done.
- CI status: green.
- Live trading authorization: unchanged; not granted by code.

---

## B1.1 Daily Evidence Operating Procedure — 2026-05-29

### Added
- Daily evidence operating procedure in `docs/operations/b11_daily_evidence_operating_procedure.md`.
- Guard regression coverage in `tests/test_b11_daily_evidence_operating_procedure.py`.
- Dedicated main CI step for B1.1 daily evidence operating procedure guard tests.

### Stabilization Result
- B1.1 daily evidence operating procedure status: done.
- CI status: green.
- Live trading authorization: unchanged; not granted by code.

---

## Evidence Artifact Index Consistency — 2026-05-29

### Added
- Central evidence artifact index in `docs/operations/evidence_artifact_index.md`.
- Guard regression coverage in `tests/test_evidence_artifact_index.py`.
- Dedicated main CI step for evidence artifact index guard tests.

### Stabilization Result
- Evidence artifact index consistency status: done.
- CI status: green.
- Live trading authorization: unchanged; not granted by code.

---

## Full-Suite Flake Review — 2026-05-29

### Added
- Full-suite flake review policy in `docs/operations/full_suite_flake_review.md`.
- Guard regression coverage in `tests/test_full_suite_flake_review_policy.py`.
- Dedicated main CI step for full-suite flake review policy guard tests.

### Stabilization Result
- Full-suite flake review status: done.
- CI status: green.
- Live trading authorization: unchanged; not granted by code.

---

## CI Runtime Simplification — 2026-05-29

### Changed
- Renamed the final full-suite step to `Full regression suite residual tests`.
- Reduced duplicate CI work by excluding test files already executed in dedicated targeted gates from the residual full-suite step.
- Preserved the targeted EV, GOV, CL, BT, IP, report-boundary and evidence-guard CI steps.

### Stabilization Result
- CI runtime simplification status: done.
- CI status: green.
- Live trading authorization: unchanged; not granted by code.

---

## Roadmap EV Completion Cleanup — 2026-05-29

### Changed
- Roadmap now marks EV1-EV12 consistently as `Done / CI-green`.
- Removed stale roadmap focus text that still pointed to EV1-EV2 or EV3-EV6 as the next active remediation block.
- Updated current execution focus toward CI runtime simplification, full-suite flake review and evidence artifact index consistency.

### Added
- `tests/test_roadmap_ev_completion_guard.py` to prevent EV roadmap status from becoming stale again.
- Dedicated main CI step for roadmap EV completion guard tests.

### Stabilization Result
- Roadmap EV cleanup status: done.
- CI status: green.
- Live trading authorization: unchanged; not granted by code.

---

## EV Evidence Consolidation + Full-Suite Stability Review — 2026-05-29

### Added
- Consolidated EV1-EV12 evidence matrix in `docs/operations/ev_evidence_consolidation_full_suite_review.md`.
- Guard regression tests in `tests/test_ev_evidence_consolidation.py` to protect EV status coverage, primary regression file links, targeted EV CI steps, and the full regression suite guard.
- Dedicated main CI step for EV evidence consolidation guard tests.

### Stabilization Result
- EV1-EV12 evidence consolidation status: done.
- CI status: green.
- Live trading authorization: unchanged; not granted by code.

---

## EV12 Drawdown Magnitude Governance — 2026-05-29

### Fixed
- EV12: execution kill-switch drawdown governance now validates the actual drawdown magnitude, not only the drawdown source type and reconciliation state.
- Drawdown magnitude checks run only after equity values and reported drawdown percentage are internally consistent.

### Added
- `watch_drawdown_pct` and `max_drawdown_pct` thresholds in `ExecutionKillSwitchConfig`.
- `drawdown_watch_threshold_exceeded` warning reason for validated drawdown above the watch threshold.
- `drawdown_block_threshold_exceeded` blocking reason for validated drawdown above the block threshold.
- `drawdown_magnitude_checked` decision note for successfully evaluated drawdown magnitude.
- Dedicated EV12 regression coverage in `tests/test_ev12_drawdown_magnitude.py`.
- Dedicated main CI step for EV12 drawdown magnitude regression tests.

### Stabilization Result
- EV12 implementation status: done.
- CI status: green.
- Live trading authorization: unchanged; not granted by code.

---

## EV8 Fixed-Date Holdout Semantics — 2026-05-29

### Fixed
- EV8: the lockbox report no longer overstates fixed-date split evidence as broad out-of-sample or walk-forward validation.
- Report title changed to `Fixed-Date Holdout Validation Lockbox`.
- Validation scope now explicitly states the evidence is not walk-forward optimization, not k-fold cross-validation, and not proof against overfitting.

### Added
- `validation_method = fixed_date_holdout_degradation_check` in lockbox JSON and markdown reports.
- `validation_scope_note` in lockbox JSON and markdown reports.
- Validation method and scope note are included in the evidence contract hash.
- Regression coverage proving the report declares fixed-date holdout semantics and does not use the previous overbroad title.
- Regression coverage proving JSON output contains the validation method and scope note.
- Dedicated main CI step for EV8 fixed-date holdout semantics regression tests.

### Stabilization Result
- EV8 implementation status: done.
- CI status: green.
- Live trading authorization: unchanged; not granted by code.

---

## EV11 Conservative Setup Scoring Fallbacks — 2026-05-29

### Fixed
- EV11: missing long-horizon setup indicators no longer receive optimistic fallback scores.
- Setup scoring now treats insufficient long-horizon trend/asymmetry history conservatively with `0.0` component scores.
- Invalid close values no longer create optimistic trend or asymmetry scores.

### Added
- Conservative missing-indicator constants for trend and asymmetry scoring.
- Audit notes for missing long-horizon trend and asymmetry inputs.
- Audit note for missing or invalid close data.
- Regression coverage proving partial-history setups do not receive optimistic defaults.
- Regression coverage proving invalid close values do not create optimistic setup scores.
- Dedicated main CI step for EV11 conservative setup scoring regression tests.

### Stabilization Result
- EV11 implementation status: done.
- CI status: green.
- Live trading authorization: unchanged; not granted by code.

---

## EV10 Profit-Factor Infinity Handling — 2026-05-29

### Fixed
- EV10: profit-factor degradation now handles `inf` boundaries deterministically without producing `nan`.
- Historical edge JSON reports now serialize infinite profit factor as the string `"inf"` instead of non-standard JSON `Infinity`.

### Added
- `calculate_profit_factor_degradation` for explicit profit-factor degradation semantics.
- JSON-safe serialization for historical edge metrics and gates.
- Regression coverage for `inf -> inf`, `inf -> finite`, `finite -> inf`, and finite-to-finite degradation cases.
- Regression coverage proving historical edge JSON output contains no `Infinity` or `NaN` tokens.
- Dedicated main CI step for EV10 profit-factor infinity regression tests.

### Stabilization Result
- EV10 implementation status: done.
- CI status: green.
- Live trading authorization: unchanged; not granted by code.

---

## EV7 Decision Ranking Fix — 2026-05-29

### Fixed
- EV7: `rank_candidates` no longer lets a `tier_3` candidate with `REDUCED_SIZE` outrank a clean `tier_3` `WATCH` candidate.

### Added
- Tier-aware ranking priority through `_ranking_decision_priority`.
- Regression coverage proving clean Tier-3 WATCH ranks above Tier-3 REDUCED_SIZE.
- Regression coverage proving reduced Tier-2 can still rank above Tier-3 WATCH.
- Dedicated main CI step for EV7 decision ranking regression tests.

### Stabilization Result
- EV7 implementation status: done.
- CI status: green.
- Live trading authorization: unchanged; not granted by code.

---

## EV3-EV6 Backtest Fidelity Fix — 2026-05-29

### Fixed
- EV3: historical backtests now fail closed for unsupported `stop_model` and `exit_model` values instead of silently applying an implicit default.
- EV4: `breakeven_after_t1` can now stop at entry after Target 1 instead of booking a false full `-1R` loss.
- EV5: gap-through-stop bars can now fill at the bar open when the open is worse than the configured stop-loss.
- EV6: Target-1-only exits now use the actual Target 1 hit date instead of the last bar in the evaluation window.

### Added
- `BacktestExecutionConfig` for explicit same-bar and stop-gap execution assumptions.
- Supported stop model contract: `None`, `fixed`, `percentage_stop`, `breakeven_after_t1`.
- Supported exit model contract: `None`, `t1_t2`, `r_multiple_targets`, `t1_only`.
- Regression coverage in `tests/test_backtest_fidelity_ev3_ev6.py`.
- Dedicated main CI step for EV3-EV6 backtest fidelity tests.

### Stabilization Result
- EV3 implementation status: done.
- EV4 implementation status: done.
- EV5 implementation status: done.
- EV6 implementation status: done.
- CI status: green.
- Live trading authorization: unchanged; not granted by code.

---

## EV1-EV2 Sharpe Definition Fix — 2026-05-29

### Fixed
- EV1: `calculate_sharpe_ratio` now returns sample-size-independent per-trade Sharpe instead of a sample-size-scaled t-statistic.
- EV2: Deflated Sharpe inputs now use per-trade Sharpe units.

### Added
- `calculate_sharpe_tstat` for the separate sample-size-scaled significance proxy.
- Regression coverage in `tests/test_sharpe_definition_regression.py`.
- Dedicated main CI step for EV1-EV2 Sharpe definition tests.

### Stabilization Result
- EV1 implementation status: done.
- EV2 implementation status: done.
- CI status: green.
- Live trading authorization: unchanged; not granted by code.
