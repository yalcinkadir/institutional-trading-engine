# CHANGELOG

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
- EV1: `calculate_sharpe_ratio` now returns sample-size-independent per-trade Sharpe instead of a t-statistic.
- EV2: Deflated Sharpe now receives the per-trade Sharpe unit expected by the DSR variance formula.
- Related audit fix: the historical edge drawdown gate now reports the effective absolute R threshold instead of the raw multiplier.

### Added
- `calculate_sharpe_tstat` as a separate significance proxy.
- `SHARPE_DEFINITION_VERSION = "per-trade-sharpe-2026.05.29-v1"` in historical edge validation and public threshold config.
- Regression coverage in `tests/test_sharpe_definition_regression.py`.
- Dedicated main CI step for EV1-EV2 Sharpe definition regression tests.

### Changed
- `MIN_SHARPE_RATIO` was recalibrated from `0.8` to `0.10` because the gate now uses per-trade Sharpe, not the previous sample-size-scaled t-statistic.
- `THRESHOLDS_VERSION` was bumped to `public-demo-2026.05.29-v4-ev1-ev2-sharpe-definition-fix` to invalidate older public-demo evidence artifacts that used the old Sharpe semantics.
- `calculate_sharpe_ratio` uses population variance for the evaluated artifact distribution so duplicating the same R distribution does not change the Sharpe value.

### Stabilization Result
- EV1 implementation status: done.
- EV2 implementation status: done.
- EV9 audit fix implementation status: done.
- CI status: green.
- Live trading authorization: unchanged; not granted by code.

---

## GOV7-GOV10 Pre-Live Hygiene — 2026-05-29

### Added
- GOV7 exact public/demo adaptive-weight normalization in `src/validation/gov7_gov10_pre_live_hygiene.py`.
- GOV8 explicit VIX term-structure inversion semantics with `DIRECT`, `PARTIAL`, `NONE` and `UNKNOWN` modes.
- GOV9 duplicate/overlapping module marker validation for ownership, deprecation and replacement tracking.
- GOV10 cumulative Paper Observation drift gate to detect small persistent drift that may evade max-daily-drift checks.
- Regression coverage in `tests/test_gov7_gov10_pre_live_hygiene.py`.
- Dedicated main CI step for GOV7-GOV10 pre-live hygiene tests.

### Improved
- Public/demo rounded weights can now be normalized so their published rounded sum is exactly `1.0`.
- VIX term-structure `PARTIAL` compression is no longer semantically equivalent to a `DIRECT` inversion.
- Duplicate module remediation can be tracked with explicit owner/replacement/rationale markers.
- Paper Observation drift checks can now capture cumulative small drift over multiple observations.

### Stabilization Result
- GOV7 implementation status: done.
- GOV8 implementation status: done.
- GOV9 implementation status: done.
- GOV10 implementation status: done.
- CI status: green.
- Live trading authorization: unchanged; not granted by code.

---

## GOV4-GOV6 Runtime Stability Hardening — 2026-05-29

### Fixed
- GOV4: `evaluate_negative_overrides` no longer treats `vix=None` or invalid VIX as `0` market stress.
- GOV5: `RuntimeState.history` no longer grows without bound during long-running observation.
- GOV6: `RuntimeLoop` no longer dies silently on a single `cycle_provider` exception.

### Added
- Explicit `vix_unavailable` minor override when a VIX key is present but unavailable or invalid.
- Bounded `RuntimeState.history` ring buffer with default max length of `1000`.
- `RuntimeLoopError` and max-consecutive-error handling in `RuntimeLoop.start`.
- Regression coverage in:
  - `tests/test_negative_override.py`
  - `tests/test_runtime_state.py`
  - `tests/test_runtime_loop.py`
- Dedicated main CI step for GOV4-GOV6 runtime stability hardening tests.

### Stabilization Result
- GOV4 implementation status: done.
- GOV5 implementation status: done.
- GOV6 implementation status: done.
- CI status: wired; final workflow-green status must be confirmed in GitHub Actions.
- Live trading authorization: unchanged; not granted by code.

---

## B1.1 Evidence Operation Discipline + TG2/TG3 Reporting Integration — 2026-05-29

### Added
- B1.1 evidence operation discipline gate in `src/operations/evidence_operation_discipline.py`.
- TG2/TG3 research-only report templates in `src/reporting/tg2_tg3_report_templates.py`.
- Regression coverage in `tests/test_b11_evidence_operation_discipline.py`.
- Operational documentation in `docs/operations/b11_evidence_operation_discipline.md`.
- Main CI step for B1.1 evidence operation discipline tests.

### Improved
- B1.1 now has an explicit fail-closed operation record for observation-only mode, daily evidence presence, daily evidence pass status, reconciliation cleanliness, TG3 template rendering and safe TG2 Telegram dispatch records.
- TG3 now renders Daily Evidence, Fill Quality, Kill Switch and Backtest Summary report templates with research-only operation boundaries.
- TG2 now reuses the TG1 research-only Telegram boundary for report delivery integration.
- README and ROADMAP now mark TG2/TG3 as implemented / CI-wired and B1.1 as operation-gated while long-running observation remains active.

### Stabilization Result
- B1.1 operation gate implementation status: done.
- TG2 implementation status: done / CI-wired.
- TG3 implementation status: done / CI-wired.
- Local targeted test status: `pytest tests/test_b11_evidence_operation_discipline.py -q` passed.
- CI status: wired; final workflow-green status must be confirmed in GitHub Actions.
- Live trading authorization: unchanged; not granted by code.

---

## IP9/IP10 Public Repository Governance — 2026-05-29
