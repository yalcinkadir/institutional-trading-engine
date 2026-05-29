# CHANGELOG

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
- Live trading remains intentionally not authorized by code.

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
- Live trading remains intentionally not authorized by code.
