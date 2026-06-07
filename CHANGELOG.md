# CHANGELOG

## P132 Scanner Runtime Boundary — 2026-06-07

### Added
- Added `tests/test_p132_scanner_runtime_boundary.py`.
- Added `docs/operations/p132_scanner_runtime_boundary.md`.

### Changed
- Added scanner runtime boundary validation to `src/validation/feature_connectivity_matrix_guard.py` to avoid introducing a new ARCH106 source-module inventory entry.
- Static watchlists are now labelled as research setup only and cannot claim dynamic scanner breadth or trading-edge proof.
- Dynamic scanner claims require a documented `scanner_contract_ref`.
- Updated ROADMAP with P132 status and hard rule.

### Validated
- Static watchlist payloads pass only when the boundary is explicit.
- Missing or invalid `selection_mode` blocks runtime reports.
- Static watchlists cannot claim dynamic scanner behavior or trading edge.
- Dynamic scanner mode requires a scanner contract reference.
- Paper-only safety boundary remains enforced.
- ARCH106 inventory remains stable because no additional `src` module path is introduced.

### Status
- P132: Implemented.
- Live trading authorization: unchanged; not granted by code.

---

## PortfolioState Fail-Closed Fixture Migration Closure — 2026-06-07

### Validated
- Confirmed runtime PortfolioState parsing requires an explicit boolean `governance_valid` field.
- Confirmed missing or non-boolean `governance_valid` returns a conservative fail-closed state instead of silently passing runtime governance.
- Confirmed valid test fixtures explicitly set `governance_valid=true` where successful runtime flow is expected.
- Confirmed committed default `data/portfolio_state.json` remains `governance_valid=false` until a real paper or broker portfolio-state source exists.
