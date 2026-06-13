# CHANGELOG

## Real-Data Backtest Pipeline Coupling #177 — 2026-06-13

History marker retained. CI run `27472676520` passed, including the full regression residual suite.

---

## Signal State Consistency #194 — 2026-06-13

History marker retained. `NO_TRADE` signal records are guarded by `tests/test_194_signal_state_consistency.py`, and `action` is documented as the execution-readiness source of truth. CI run `27472676520` passed.

---

## Exception Audit Hardening #198 — 2026-06-12

### Added
- Added `docs/architecture/broad_exception_allowlist.json`.
- Added `scripts/check_broad_exception_policy.py`.
- Added `tests/test_198_broad_exception_policy.py`.
- Added `docs/operations/broad_exception_policy.md`.

### Changed
- Active broad exception handlers are now covered by an explicit allowlist contract.
- Structured exception audit metadata is tested for outcome, runtime-loop and safe-call paths.
- CI has a lightweight policy guard for broad exception handlers in active paths.

---

## Scanner Market-Data Run Context #195 — 2026-06-12

History marker retained.

---

## OOS Lockbox Direct Guards #197 — 2026-06-12

History marker retained.

---

## Decision Engine Consistency #200 — 2026-06-12

History marker retained.

---

## Confidence Provenance #196 — 2026-06-12

History marker retained.

---

## Report Score Provenance #180 — 2026-06-12

History marker retained.

---

## Portfolio Risk Gate #182 — 2026-06-12

History marker retained.

---

## VIX / Market Regime Policy #187 — 2026-06-11

History marker retained.

---

## Durable Evidence Index #181 — 2026-06-11

History marker retained.

---

## Watcher Lifecycle Evidence #193 — 2026-06-11

History marker retained.

---

## IP9/IP10 Public Repository Governance — 2026-06-11

History marker retained.

---

## System Invariants and Logic Safety Governance #189 — 2026-06-11

History marker retained.
