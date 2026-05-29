# CHANGELOG

## Report Output Boundary Guard — 2026-05-29

### Added
- Central report-output boundary guard in `src/report_output_boundary.py`.
- Generator wiring in `scripts/generate_report.py` so runtime report output is validated before writing.
- Unit coverage in `tests/test_report_output_boundary.py`.
- Generator wiring coverage in `tests/test_generate_report_output_boundary.py`.
- Operational documentation in `docs/operations/report_output_boundary_guard.md`.
- CI step for report output boundary guard tests.

### Protected Public Artifacts
- `reports/premarket-report.md`
- `reports/postmarket-report.md`
- `reports/weekly-report.md`

### Improved
- Runtime generators now fail closed before writing to committed public report examples.
- Public synthetic report files remain protected from accidental live/provider-backed/private content overwrite.
- Generated report output is directed toward non-committed locations such as `reports/generated/`, `reports/live/`, `reports/private/` or `outputs/`.

### Stabilization Result
- Report Output Boundary Guard implementation status: done.
- CI status: wired; final workflow-green status must be confirmed in GitHub Actions.
- Live trading remains intentionally not authorized by code.

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
