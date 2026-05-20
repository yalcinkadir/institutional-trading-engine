# Phase 1 — Live Data Integration Layer
## Architecture & Current State

**Status:** Production-ready (Phase 1 complete)  
**Last updated:** 2026-05-20

---

## What Phase 1 Accomplishes

Before Phase 1, two worlds were completely disconnected:

```
World A — live, running:
  scanner.py → Polygon API → metrics_map → markdown report

World B — framework, no live data:
  orchestrator.py ← synthetic float inputs (e.g. market_regime_score=72.0)
```

After Phase 1, one connected runtime:

```
scanner.py
  ↓ (metrics_map, vix_data)
scanner_market_snapshot_builder.build_snapshot()
  ↓
scanner_to_orchestrator.translate()         ← BridgeTranslation
  ↓ (InstitutionalDecisionInputs)
InstitutionalDecisionOrchestrator.evaluate()
  ↓ (InstitutionalDecisionResult)
RuntimeMarketSnapshot.create()              ← immutable audit record
  ↓
live_runtime_cycle._persist()              ← DecisionLogStore (JSONL)
  ↓
runtime_state.update()                     ← in-memory cycle tracking
  ↓
in_memory_state_cache.set()                ← fast latest-value access
```

**No synthetic floats. Every input is derived from live scanner data.**

---

## Module Responsibilities (mandatory separation)

### `src/bridge/scanner_to_orchestrator.py`

**Responsibility:** Pure data transformation. No side effects. No I/O.

Input:  `metrics_map: dict[str, Any]`, `vix_data: dict | None`  
Output: `BridgeTranslation` (inputs + derivation_notes + symbols_used + warnings)

Contains `_derive_*` functions for each `InstitutionalDecisionInputs` field.
Every derivation is documented, individually testable, and produces
a human-readable note stored in `BridgeTranslation.derivation_notes`.

**Fallback rule:** When data is unavailable, use conservative values.
Never optimistic defaults. Example: missing VIX → 25.0 (elevated), not 15.0 (calm).

---

### `src/bridge/scanner_market_snapshot_builder.py`

**Responsibility:** Runtime orchestration. Calls bridge + orchestrator + measures time.

Input:  `metrics_map`, `vix_data`  
Output: `RuntimeMarketSnapshot`

Does NOT contain derivation logic (that is the bridge's job).
Does NOT handle persistence (that is live_runtime_cycle's job).

**Why separate from the bridge:**
- Bridge is stateless and testable without mocking anything.
- Builder needs to measure time and call two systems — runtime concerns.
- Keeping them separate makes each independently testable.

---

### `src/runtime/runtime_market_snapshot.py`

**Responsibility:** Immutable audit record of one complete cycle.

Frozen dataclass. Contains:
- Raw scanner inputs (metrics_map, vix_data)
- Full bridge output (inputs, derivation_notes, warnings)
- Orchestrator result (macro_regime, exposure, classification)
- Timestamps and cycle duration

`to_persistence_payload()` produces a flat, JSON-serialisable dict
suitable for `DecisionLogStore`. The full `metrics_map` is excluded
from persistence (too large for JSONL line).

---

### `src/runtime/live_runtime_cycle.py`

**Responsibility:** One complete institutional cycle with governance guarantee.

**Execution order is invariant — never reorder these steps:**

```
Step 1: evaluate_kill_switch()      ← GOVERNANCE FIRST, always
Step 2: validate_risk_limits()      ← GOVERNANCE SECOND, always
         → raises GovernanceBlockedError if blocked
         → persists block event to DecisionLogStore
Step 3: translate()                 ← bridge
Step 4: orchestrator.evaluate()     ← institutional analysis
Step 5: RuntimeMarketSnapshot.create()
Step 6: decision_log_store.append() ← persistence
Step 7: runtime_state.update()      ← cycle state
Step 8: in_memory_state_cache.set() ← fast access cache
```

**Governance guarantee:** A decision is never produced or persisted
when governance conditions are breached. Only the block event is persisted.

**Error handling:** `GovernanceBlockedError` is a controlled exception
that scanners catch explicitly. All other exceptions propagate.

---

### `src/scanner.py` (modified)

The runtime cycle is called at the end of `main()`, after the report
file is written:

```python
try:
    from src.runtime.live_runtime_cycle import GovernanceBlockedError, live_runtime_cycle
    snapshot = live_runtime_cycle.run(metrics_map=metrics_map, vix_data=vix_data)
    print(f"[Runtime] cycle={snapshot.snapshot_id} | {snapshot.regime_summary}")
except GovernanceBlockedError as e:
    print(f"[Runtime] GOVERNANCE BLOCK: {e.reasons}")
except Exception as e:
    print(f"[Runtime] cycle error (non-fatal): {type(e).__name__}: {e}")
```

**Why after the report:**
The markdown report is the primary deliverable. It must never be blocked
by a runtime cycle failure. The runtime cycle is additive — its failure
is logged and non-fatal.

---

## What Phase 1 Does NOT Include

These are deliberate exclusions — not oversights:

| Excluded | Reason | When |
|---|---|---|
| Redis / Event Bus | Determinism before distributed complexity | Phase 5+ |
| Async execution | Synchronous runtime is simpler to audit | Phase 5+ |
| Portfolio position tracking | Requires live portfolio state | Phase 4 |
| Earnings calendar integration | External calendar API needed | Phase 4 |
| DXY / TLT in universe | Not yet in symbol config | Phase 3 |
| SQLite persistence | JSONL is sufficient now, upgrade is incremental | Phase 2 |
| Structured logging | print() is sufficient for single-node operation | Phase 3 |

---

## Data Quality Handling

When scanner data is degraded (e.g., VIX unavailable):

1. Bridge populates `BridgeTranslation.data_quality_warnings`
2. Conservative fallback values are used (never optimistic)
3. Warnings are included in the persistence payload
4. Warnings are printed to stdout
5. The cycle continues — degraded data is better than no analysis
6. Only governance breaches stop a cycle

---

## Inputs That Are Still Approximated

The following `InstitutionalDecisionInputs` fields use approximations
until the corresponding data sources are added to the universe:

| Field | Approximation | Real source (future) |
|---|---|---|
| `bond_strength` | VIX-level proxy | TLT/IEF in symbol universe |
| `dollar_strength` | Inverse GLD/equity | DXY or UUP in universe |
| `correlation_risk_percent` | VIX-scaled estimate | Portfolio correlation engine (Phase 4) |
| `event_risk_percent` | Static 15.0 | Earnings calendar (Phase 4) |
| `order_size_percent_adv` | Static 2.0 | Portfolio position tracker (Phase 4) |
| `portfolio_*` fields | Conservative defaults | Portfolio tracker (Phase 4) |

These approximations are conservative, documented, and individually replaceable.

---

## Test Coverage

| File | Tests | What is covered |
|---|---|---|
| `test_scanner_to_orchestrator_bridge.py` | 39 | All derivation functions, edge cases, NaN/None handling |
| `test_runtime_market_snapshot.py` | 16 | Creation, serialisation, quality flags, JSON validity |
| `test_live_runtime_cycle.py` | 12 | Success path, governance blocks, state/persistence updates |
| `test_scanner_market_snapshot_builder.py` | 12 | Builder integration, scanner contract |
| **Total** | **79** | |

---

## What Comes Next (Phase 2)

Phase 2 — Governance Integration — will:

1. Move governance thresholds from constants to `config.py`
2. Wire real portfolio drawdown into the governance check
3. Add daily loss tracking (requires portfolio position state)
4. Activate SQLite as persistence backend (sqlite_store.py exists, needs wiring)
5. Add structured JSON logging (json_logger.py exists, needs wiring)

Phase 2 does NOT add new engines. It hardens what Phase 1 built.
