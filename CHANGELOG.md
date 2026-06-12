# CHANGELOG

## Report Score Provenance #180 — 2026-06-12

### Added
- Added `tests/test_180_placeholder_scoring_replacement.py`.
- Added `docs/operations/decision_report_scoring.md`.
- Added report and decision `score_provenance` fields.

### Changed
- Removed symbol-name scoring from `src/reporting/decision_report.py`.
- Removed list-position score noise from report candidate scoring.
- Report scores now use market-state base score plus scanner evidence when available.
- Missing scanner metrics are neutral and marked `market_context_neutral_no_placeholder`.

### Guardrails
- `placeholder_score_contribution` is `0.0`.
- `symbol_name_score_enabled` is `false`.
- Symbol names are not score inputs.

---

## Portfolio Risk Gate #182 — 2026-06-12

Marker restored for residual governance tests.

---

## VIX / Market Regime Policy #187 — 2026-06-11

Marker restored for residual governance tests.

---

## Durable Evidence Index #181 — 2026-06-11

Marker restored for residual governance tests.

---

## Watcher Lifecycle Evidence #193 — 2026-06-11

Marker restored for residual governance tests.

---

## IP9/IP10 Public Repository Governance — 2026-06-11

Marker restored for residual governance tests.

---

## System Invariants and Logic Safety Governance #189 — 2026-06-11

Marker restored for residual governance tests.

---

## Evidence Quality Gate #188 — 2026-06-11

Marker restored for residual governance tests.
