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

The first three P0 tracks are:

1. Survivorship-safe historical data foundation
2. Second data source cross-validation
3. Real persisted observation feed for paper observation

---

## Important terminology: Paper Observation vs Broker Paper Trading

The project must keep two concepts separate.

### Paper Observation

Paper Observation is an observation-only validation loop.

It can generate signals, write theoretical entries/stops/targets into a journal and later calculate hypothetical 5D/20D outcomes from market data.

This is useful for forward evidence and model drift detection.

It is not broker paper trading.

No order leaves the system. No broker confirms a fill. No real execution slippage is measured.

### Current limitation

The current observation flow must not be treated as statistically meaningful if it still depends on bootstrap-seed data instead of a real persisted daily observation source feed.

Therefore B12 is a blocker for serious forward-evidence claims.

### Broker Paper Trading

Broker Paper Trading starts only when Phase C execution components exist:

- broker adapter interface
- paper broker implementation, for example Alpaca paper
- order lifecycle handling
- order reconciliation
- fill-quality reporting
- execution kill switch

Until then, the system is observation-only.

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

## P0 Track 3: B12 real persisted daily observation source feed

### Problem

Observation-only paper validation is not useful if the system is evaluating bootstrap-seed data instead of real persisted forward observations.

This creates false confidence. It may prove that the journal code works, but it does not prove forward evidence.

### Required work

- Replace bootstrap-seed observation input with a real persisted daily observation source feed.
- Persist every generated signal with timestamp, symbol, setup, theoretical entry, stop, target and data-confidence metadata.
- Store immutable daily observation snapshots.
- Reconcile 5D and 20D hypothetical outcomes from persisted observations, not regenerated hindsight input.
- Mark observation periods as invalid if the source feed is missing, stale or regenerated.
- Add tests proving bootstrap-seed observations cannot be treated as valid forward evidence.

### Exit gate

B12 is not Done until a 5D/20D outcome can be traced back to a real persisted observation generated on the original signal date.

---

## Phase C dependency: real broker paper trading

Broker paper trading should not be started casually.

The earliest controlled path is:

1. Finish or unblock B12.
2. Define the broker adapter interface.
3. Implement an Alpaca paper adapter or another paper broker adapter.
4. Add order reconciliation before trusting fills.
5. Add fill-quality reporting before comparing live-paper results with backtests.
6. Add execution kill switch before any later live-capital discussion.

Broker paper trading without order reconciliation is not evidence. It is just order submission.

---

## Immediate action sequence

1. Close Phase A documentation gate.
2. Keep Phase B focused on data integrity and real observation persistence.
3. Create minimal provider-neutral interfaces before choosing implementation details.
4. Add tests before wiring any external provider.
5. Add a small fixture-based proof for delisted-symbol inclusion.
6. Add a fixture-based proof for provider divergence detection.
7. Add B12: replace bootstrap observation with persisted daily observation source feed.
8. Only after these foundations exist, wire real vendor data and plan broker-paper execution.

---

## Explicit non-goals for this phase

- No live trading.
- No automatic broker execution.
- No broker-paper trading before B12 and C1/C2/C4 are designed.
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
