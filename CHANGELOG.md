# CHANGELOG

## Portfolio Risk Gate #182 — 2026-06-12

### Added
- Added `tests/test_182_portfolio_risk_gate.py` for portfolio-context-missing and portfolio-heat/concentration failure paths.
- Added `docs/operations/portfolio_risk_gate.md` as the portfolio-risk gate contract.
- Added signal evidence fields: `portfolio_risk_status`, `portfolio_risk_block_reason`, `portfolio_risk_multiplier`.

### Changed
- Updated `src/signals/trade_plan_validator.py` so required portfolio-risk context can block an otherwise valid long trade plan.
- Updated `src/signals/signal_generator.py` so `build_signals()` calls `evaluate_portfolio_risk()` when portfolio-risk enforcement is required.
- Missing returns context, portfolio heat, sector concentration or correlation warnings downgrade otherwise valid actionable signals to `NO_TRADE`.
- Removed `src/portfolio_risk.py` from the P150 orphan quarantine manifest because #182 wires it into the active signal-generation path.

### Guardrails
- Individual trade-plan validity is no longer sufficient when portfolio-risk enforcement is required.
- Missing portfolio context fails closed.
- Portfolio-risk block reasons are visible in signal notes and JSON payloads.

### Boundary
- This is portfolio-risk evidence hardening.
- No strategy rule or scoring threshold is changed.
- Repository-wide full-regression green is not claimed by this changelog entry.

---

## VIX / Market Regime Policy #187 — 2026-06-11

### Added
- Added `tests/test_187_vix_regime_policy.py` to guard VIX available, VIX missing with proxy, VIX missing without proxy, missing index data and Polygon client failure paths.
- Added `docs/operations/vix_regime_policy.md` as the explicit VIX/regime fallback and blocking policy.
- Added structured `regime_policy` payloads to market-regime summaries.

### Changed
- Updated `src/reporting/market_regime.py` so market-regime summaries no longer emit unexplained `Unknown` when required regime inputs are unavailable.
- VIX available now yields `regime_policy.action=ALLOW` and `confidence=FULL`.
- VIX missing with proxy available yields `regime_policy.action=DEGRADE`, `confidence=DEGRADED` and `source=polygon_proxy`.
- VIX missing without proxy, missing index trend inputs or Polygon client failure now yield `BLOCKED_MARKET_REGIME_UNAVAILABLE` and `regime_policy.action=BLOCK`.
- Aligned existing P164 and P118 tests with the stricter #187 blocking policy.
- Updated `README.md` with the #187 VIX/regime policy boundary.

### Guardrails
- Reports must not emit unexplained `regime: Unknown` for market-regime evidence.
- Regime payloads expose `source`, `fallback_used`, `confidence`, `action`, VIX status and index-trend status.
- Proxy evidence is explicitly degraded and must not be promoted as full VIX validation.
- Missing VIX/proxy or required index trend inputs produce a deterministic blocked regime state.

### Boundary
- This is market-regime evidence-quality hardening.
- No strategy rule, scoring threshold, entry/exit rule or broker execution capability is changed.
- Live trading authorization: unchanged; not granted by code.
- Repository-wide full-regression green is not claimed by this changelog entry.

---

## Durable Evidence Index #181 — 2026-06-11

### Added
- Added `tests/test_181_durable_evidence_index.py` to guard durable Paper Observation evidence-index behavior.
- Added `docs/operations/durable_evidence_index.md` as the #181 durable evidence-index contract.
- Extended `reports/daily_observation_automation/review_index.json` semantics with schema `paper_observation_durable_evidence_index.v1`.

### Changed
- Extended `src/operations/daily_observation_artifact_review_index.py` so PO12 review indexes now preserve durable audit metadata for #181:
  - workflow run id
  - artifact pointer
  - artifact checksum field
  - data mode
  - degradation flags
  - durable status
  - no-trade-valid classification
- Updated `README.md` with the #181/PO12 durable evidence-index boundary.

### Guardrails
- GitHub Actions artifacts are explicitly not treated as the durable audit source of truth.
- Large runtime artifacts remain blocked from being committed to `main` by default.
- Missing metadata is made explicit with `UNKNOWN` / `not_available` instead of silently omitted.
- Durable statuses distinguish `SUCCESS`, `BLOCKED`, `DEGRADED`, `FAILED` and `NO_TRADE_VALID`.

### Boundary
- This is Paper Observation evidence-retention and auditability hardening.
- No strategy rule, scoring threshold, entry/exit rule or broker execution capability is changed.
- Live trading authorization: unchanged; not granted by code.
- Repository-wide full-regression green is not claimed by this changelog entry.

---

## Watcher Lifecycle Evidence #193 — 2026-06-11

### Added
- Added `scripts/watcher_lifecycle_summary.py` to build deterministic, lightweight watcher lifecycle summaries without growing the ARCH106 `src/` module baseline.
- Added dated and latest lifecycle summary outputs:
  - `reports/watchers/lifecycle/YYYY-MM-DD.json`
  - `reports/watchers/lifecycle/latest.json`
- Added `tests/test_193_watcher_lifecycle_summary.py` to prove lifecycle summaries are written for zero-actionable/no-trade watcher runs.
- Added `docs/operations/watcher_lifecycle_evidence.md` as the authoritative lifecycle evidence contract.

### Changed
- Updated `scripts/run_entry_exit_watcher.py` so every successful watcher cycle writes lifecycle summary evidence, including cycles with zero actionable open signals.
- Moved watcher lifecycle summary writing out of `src/` and into the runner/script evidence layer to keep ARCH106 production-module ratchet stable.
- Updated `README.md` and `ROADMAP.md` with the #193 watcher lifecycle evidence boundary.

### Guardrails
- A watcher cycle with zero actionable open signals is explicitly marked `NO_ACTIONABLE_SIGNALS`.
- Silent watcher success is not accepted as signal-level forward evidence.
- Lifecycle summaries include the original signal file path and SHA256 checksum reference.
- `data/signal_lifecycle.jsonl` remains a mutable event log; the repo-visible authoritative summary is under `reports/watchers/lifecycle/`.

### Boundary
- This is watcher evidence/auditability hardening.
- No strategy rule, scoring threshold, entry/exit rule or broker execution capability is changed.
- Live trading authorization: unchanged; not granted by code.
- Repository-wide full-regression green is not claimed by this changelog entry.

---

## IP9/IP10 Public Repository Governance — 2026-06-11

### Added
- Added IP9 public-edge review governance to the PR review process.
- Added IP10 license and research-only usage disclaimer status coverage.

### Guardrails
- Public repository changes must preserve public-demo defaults and must not expose proprietary thresholds, setup maps, scoring weights, exit profiles or production-like parameters.
- Research/paper-only and no-live-trading language must remain intact in public-facing project files.

### Boundary
- This is public repository governance and disclosure-safety documentation.
- No strategy rule, scoring threshold, entry/exit rule or broker execution capability is changed.
- Live trading authorization: unchanged; not granted by code.

---

## System Invariants and Logic Safety Governance #189 — 2026-06-11

### Added
- Added machine-checkable System Invariants and Logic Safety Governance coverage for #189.
- Added status coverage for forbidden state conversions, logic-safety severity classes and evidence-traceability requirements.

### Guardrails
- `DEGRADED`, `BLOCKED`, `UNKNOWN`, demo/stub and missing-provenance states must not be promoted as full `PASS` evidence.
- Logic-safety mappings require evidence commands, guard tests, contract tests, validation scripts, CI workflow results or evidence artifacts.

### Boundary
- This is logic-safety governance and evidence-traceability hardening.
- No strategy rule, scoring threshold, entry/exit rule or broker execution capability is changed.
- Live trading authorization: unchanged; not granted by code.
- Repository-wide full-regression green is not claimed by this changelog entry.

---

## Evidence Quality Gate #188 — 2026-06-11

### Added
- Added the #188 Evidence Quality Gate to block roadmap-stable, strategy-promotion, production-grade evidence, paper-confidence, backtesting-promotion, decision-stack-validation and live-readiness claims unless evidence quality is proven.
- Added CI/tooling linkage through `scripts/evaluate_evidence_quality_gate.py` and `tests/test_evidence_quality_gate_188.py`.

### Guardrails
- Evidence quality, durability, runtime reachability, historical input reproducibility, report validation, empty/no-signal classification and VIX/regime provenance must be proven before promotion claims.
- Repository-wide full-regression green is not claimed unless explicitly validated by CI.

### Boundary
- This is evidence-governance hardening.
- No strategy rule, scoring threshold, entry/exit rule or broker execution capability is changed.
- Live trading authorization: unchanged; not granted by code.
