# Action Plan: Phase B Data Integrity

Status: Active planning and controlled start
Date: 2026-05-26
Owner: yalcinkadir

---

## Current confirmed baseline

Phase A is treated as CI-validated based on the latest stabilization run:

- Phase A stabilization tests: success
- Full regression suite: success
- A3-A10 implemented
- Phase-A tests included in CI
- Full regression green

This creates a valid stabilization baseline, but not yet a proven trading edge.

---

## Strategic rule

The next phase is not feature expansion.

The next phase is evidence hardening.

No ML, options-flow, broker execution or alternative-data layer should be prioritized before the data integrity foundation is good enough to trust historical evidence.

---

## Phase B objective

Build a data integrity foundation that prevents the system from validating strategy logic on biased, incomplete or single-vendor data.

The first two P0 tracks are:

1. Survivorship-safe historical data foundation
2. Second data source cross-validation

---

## P0 Track 1: Survivorship-safe historical data

### Problem

Historical backtests that only use currently available symbols can overstate edge because failed, delisted or merged companies may be missing.

A strategy can look robust historically while quietly benefiting from survivorship bias.

### Required work

- Select one survivorship-safe research data provider candidate.
- Define a provider-neutral historical universe interface.
- Represent delisted symbols.
- Represent symbol history and symbol changes.
- Document corporate-action adjustment assumptions.
- Add tests proving delisted symbols can be included.
- Compare at least one validation path against Polygon-only history.
- Produce a bias-impact report.

### Exit gate

This track is not Done until a historical validation path can include delisted symbols and show the difference versus Polygon-only history.

---

## P0 Track 2: Second data source cross-validation

### Problem

Single-vendor data is a hidden operational and evidence risk.

A provider can return missing bars, stale bars, incorrect volume, split-adjustment inconsistencies or delayed corporate-action corrections.

### Required work

- Define a provider-neutral OHLCV model.
- Define a cross-provider comparison contract.
- Compare open, high, low, close and volume with explicit tolerances.
- Detect missing bars.
- Detect stale bars.
- Detect corporate-action mismatches when available.
- Add fail-closed behavior for critical mismatches.
- Add tests for acceptable and unacceptable provider divergence.

### Exit gate

This track is not Done until provider conflicts are observable, testable and able to block downstream evidence/signals when the mismatch is critical.

---

## Immediate action sequence

1. Close Phase A documentation gate.
2. Keep Phase B focused on data integrity only.
3. Create minimal provider-neutral interfaces before choosing implementation details.
4. Add tests before wiring any external provider.
5. Add a small fixture-based proof for delisted-symbol inclusion.
6. Add a fixture-based proof for provider divergence detection.
7. Only after these foundations exist, wire real vendor data.

---

## Explicit non-goals for this phase

- No live trading.
- No automatic broker execution.
- No ML feature work.
- No options-flow feature work.
- No LLM-sentiment feature work.
- No new dashboard work.

---

## Quality gate language

A task can only move to Done when it is:

- implemented,
- tested,
- documented,
- CI-compatible,
- and connected to a clear failure mode it prevents.

Code quality is not trading edge. Phase B exists to protect evidence quality before the system claims edge.
