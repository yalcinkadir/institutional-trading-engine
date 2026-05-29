# CHANGELOG

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

### Added
- PR public-edge review checklist in `.github/pull_request_template.md`.
- MIT license in `LICENSE`.
- Research and usage disclaimer in `DISCLAIMER.md`.
- Operational documentation in `docs/operations/ip9_ip10_public_repo_governance.md`.
- Regression coverage in `tests/test_ip9_ip10_public_repo_governance.py`.
- Dedicated governance workflow in `.github/workflows/ip9_ip10.yml`.

### Improved
- Future PRs that touch strategy, scoring, thresholds, setup maps, exit profiles, ranking, reports, evidence, execution or sizing now have an explicit public-edge review checklist before merge.
- Public repository usage terms are clearer: research and decision-support only, no financial advice, no performance guarantee and no live trading permission.
- Boundary scanner policy now ignores its own scanner implementation and scanner self-tests so CI can run public-boundary checks without false positives from intentionally unsafe fixture text.
- README and ROADMAP now mark IP9/IP10 as implemented and CI-wired.

### Stabilization Result
- IP9 implementation status: done.
- IP10 implementation status: done.
- CI status: dedicated workflow wired; final workflow-green status must be confirmed in GitHub Actions.
- Live trading authorization: unchanged; not granted by code.

---

## Report Output Boundary Guard — 2026-05-29

### Added
- Fail-closed report output boundary module in `src/report_output_boundary.py`.
- Guarded report writer integration in `scripts/generate_report.py`.
- Regression coverage in `tests/test_report_output_boundary.py` and `tests/test_generate_report_output_boundary.py`.
- Operational documentation in `docs/operations/report_output_boundary_guard.md`.
- Main CI step for report output boundary guard tests.

### Improved
- Generated runtime reports can no longer overwrite committed public report examples:
  - `reports/premarket-report.md`
  - `reports/postmarket-report.md`
  - `reports/weekly-report.md`
- Relative traversal attempts such as `reports/generated/../premarket-report.md` are normalized and blocked.
- Allowed runtime report output paths remain explicit: `reports/generated/`, `reports/live/`, `reports/private/` and `outputs/`.
- README and ROADMAP now mark the Report Output Boundary Guard as implemented and CI-green.

### Stabilization Result
- Report Output Boundary Guard implementation status: done.
- CI status: green.
- Live trading authorization: unchanged; not granted by code.

---

## CL5 Regime Alignment Governance — 2026-05-29

### Added
- CL5 independent `regime_alignment` gate in `src/decision_engine.py`.
- CL5 regression coverage in `tests/test_decision_engine.py`.
- Operational documentation in `docs/operations/cl5_regime_alignment_governance.md`.
- CI step for CL5 regime-alignment governance tests.

### Improved
- Poor regime alignment now returns `NO_TRADE` with `poor_regime_alignment` instead of being hidden behind a generic insufficient-quality result.
- Decision notes now include `regime_alignment_independent_gate` when the CL5 gate rejects a candidate.
- High setup score, asymmetry score and data confidence can no longer rescue a candidate below the independent regime-alignment floor.
- The public-demo Tier 3 regime-alignment cutoff is reused as the fail-closed floor, avoiding new proprietary public constants.
- Ranking regression coverage proves that a high-score poor-regime candidate is ranked below an approved candidate.
- README and ROADMAP now mark CL5 as implemented and CI-wired.

### Stabilization Result
- CL5 implementation status: done.
- CI status: wired; final workflow-green status must be confirmed in GitHub Actions.
- Live trading authorization: unchanged; not granted by code.

---

## CL4 ATR Governance — 2026-05-29

### Added
- CL4 ATR calculation governance module in `src/validation/atr_governance.py`.
- CL4 regression coverage in `tests/test_atr_governance.py`.
- Operational documentation in `docs/operations/cl4_atr_governance.md`.
- CI step for CL4 ATR governance tests.

### Improved
- ATR semantics are now explicit and versioned instead of being treated as an invisible indicator detail.
- True range calculation explicitly includes previous-close gap risk.
- Wilder ATR is available as a deterministic public-demo calculation method seeded by the first simple average.
- `ATR_CALCULATION_VERSION` was added to `src/config/thresholds.py`.
- `THRESHOLDS_VERSION` was bumped to `public-demo-2026.05.29-v2-cl4-atr-governance` because ATR migration is evidence-affecting.
- ATR method changes now require explicit evidence invalidation instead of silently reusing older ATR-dependent artifacts.

### Stabilization Result
- CL4 implementation status: done.
- CI status: wired; final workflow-green status must be confirmed in GitHub Actions.
- Live trading authorization: unchanged; not granted by code.

---

## CL2/CL3 Scoring Audit and Drawdown-Source Governance — 2026-05-29

### Added
- CL2 scoring-system audit registry in `src/validation/scoring_audit.py`.
- CL2 regression coverage in `tests/test_scoring_audit.py`.
- CL3 drawdown-source validation in `src/validation/execution_kill_switch.py`.
- CL3 regression coverage in `tests/test_execution_kill_switch.py`.
- CLI wiring for `drawdown_source_validation` in `scripts/evaluate_execution_kill_switch.py`.
- Operational documentation in `docs/operations/cl2_scoring_system_audit.md` and `docs/operations/execution_kill_switch.md`.
- CI step for CL2/CL3 scoring and drawdown-source governance tests.

### Improved
- Report-only ranking scores are explicitly separated from decision-authoritative gates.
- Decision Engine tier gating is documented as the authoritative downstream decision gate.
- Kill-switch drawdown governance now fails closed when the drawdown source is missing, backtest-only, unknown, unreconciled or internally inconsistent.
- README and ROADMAP now mark CL2/CL3 as implemented and set CL4/CL5 as the next focus.

### Stabilization Result
- CL2 implementation status: done.
- CL3 implementation status: done.
- CI status: wired; final workflow-green status must be confirmed in GitHub Actions.
- Live trading authorization: unchanged; not granted by code.

---

## CL1 Core Decision Logic Remediation — 2026-05-29

### Fixed
- Corrected downside asymmetry calculation in `src/setup_scoring.py` so below-SMA50 assets no longer receive inflated reward/risk scores from negative `close - sma50` distance.
- Updated `src/portfolio_risk.py` so elevated portfolio risk reduces all tradable tiers, not only Tier 1 candidates.
- Updated `src/outcome_tracking.py` so breakeven outcomes are neutral in basic expectancy instead of being counted as losses.

### Added
- Regression coverage for downside asymmetry inflation in `tests/test_setup_scoring.py`.
- Regression coverage for all-tier portfolio-risk reduction in `tests/test_portfolio_risk.py`.
- Regression coverage for breakeven expectancy handling in `tests/test_outcome_tracking.py`.
- CI step for CL1 core logic remediation tests.

### Deferred
- Short-history direct-call behavior for setup-scoring helper functions remains unchanged for compatibility and is tracked separately as lower-priority interface-hardening work.

### Stabilization Result
- CL1 implementation status: done.
- CI status: wired; final workflow-green status must be confirmed in GitHub Actions.

---

## IP5/IP6 Artifact Hygiene and `.gitignore` Hardening — 2026-05-29

### Added
- Hardened `.gitignore` coverage for private edge modules, local strategy configuration, generated reports, raw data, evidence, lockbox output, caches, databases, logs and runtime artifacts.
- Public-safe synthetic report examples for premarket, postmarket and weekly report files.
- Artifact hygiene regression tests in `tests/test_artifact_hygiene.py`.
- CI step for IP5/IP6 artifact hygiene tests.

### Improved
- Public report files no longer contain live-looking ranked opportunities or provider-backed market data.
- Generated live/private/raw reports are blocked from normal version-control hygiene by ignore rules.

### Stabilization Result
- IP5 implementation status: done.
- IP6 implementation status: done.
- CI status: wired; final workflow-green status must be confirmed in GitHub Actions.

---

## IP3/IP4 Public Demo Defaults and Private Edge Boundary — 2026-05-29

### Added
- Optional external edge provider boundary in `src/config/external_edge_provider.py`.
- Public-demo threshold marker and versioning in `src/config/thresholds.py`.
- External edge provider tests in `tests/test_external_edge_provider.py`.
- Operational documentation in `docs/operations/ip3_ip4_public_demo_and_private_edge_boundary.md`.
- CI step for IP3/IP4 public-demo and external edge boundary tests.

### Improved
- Public thresholds are now explicitly documented as demo defaults only.
- The public repository remains self-contained without any private module.
- Local/private threshold providers can be loaded through `ITE_EXTERNAL_EDGE_PROVIDER` without committing proprietary configuration.
- Fallback behavior proves that missing private modules do not break public CI operation.

### Stabilization Result
- IP3 implementation status: done.
- IP4 implementation status: done.
- IP8 fallback/private-edge absence test coverage: done.
- CI status: green.
- Full regression status: green.

---

## BT7 Capacity / Turnover / Realism Gate — 2026-05-29

### Added
- BT7 capacity, turnover and transaction-cost realism gate model in `src/validation/capacity_turnover_realism_gate.py`.
- Public-safe synthetic capacity/turnover fixture in `data/demo_bt7_capacity_turnover.json`.
- CLI report generator in `scripts/generate_bt7_capacity_turnover_report.py`.
- Operational documentation in `docs/operations/bt7_capacity_turnover_realism_gate.md`.
- Dedicated BT7 GitHub Actions workflow in `.github/workflows/bt7.yml`.
- Main CI step for `tests/test_bt7_capacity_turnover_realism_gate.py`.

### Stabilization Result
- BT7 implementation status: done.
- BT7 CI status: green.
- Full regression status: green.
