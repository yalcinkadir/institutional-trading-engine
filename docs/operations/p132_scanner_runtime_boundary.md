# P132 Scanner Runtime Boundary

Status date: 2026-06-07

## Purpose

P132 separates a static Paper Observation watchlist from a real dynamic scanner.

The system must not imply that a complete market universe was dynamically screened when the runtime path only processed a fixed research watchlist.

## Required evidence fields

Every runtime report and Paper Observation evidence payload that depends on symbol selection must expose:

- `selection_mode`
- `selected_symbols`
- `selection_reason`
- `scanner_contract_ref` when `selection_mode=dynamic_scanner`
- `live_trading_authorized=false`
- `broker_execution_mode=paper_only`

## Valid selection modes

### `static_watchlist`

A static watchlist is allowed for research and Paper Observation.

It is not a proof of scanner breadth and it is not a trading edge claim.

Static-watchlist payloads must not set:

- `dynamic_scanner_claimed=true`
- `trading_edge_claimed=true`

### `dynamic_scanner`

A dynamic scanner is only claimable when the runtime payload links a documented contract through `scanner_contract_ref`.

## Dynamic scanner contract

A future real scanner contract must define at minimum:

- universe source
- symbol inclusion / exclusion rules
- liquidity filters
- data completeness filters
- regime or setup filters
- timestamp of universe evaluation
- selected-symbol reason codes
- evidence artifact path

Until that contract is implemented and CI-green, static-watchlist output remains research-only and must be labelled as such.

## Runtime guard

Implementation:

- `src/validation/scanner_runtime_boundary.py`

Tests:

- `tests/test_p132_scanner_runtime_boundary.py`

## Safety boundary

P132 does not authorize live trading, broker execution, capital allocation or production deployment.

The system remains research / decision-support / paper-observation only.
