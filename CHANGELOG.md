# CHANGELOG

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
