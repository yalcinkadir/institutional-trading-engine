# Evidence Quality Gate (#188)

Status date: 2026-06-11

## Purpose

The Evidence Quality Gate prevents the project from promoting Paper Observation, Backtesting, strategy quality, roadmap maturity or live-readiness while the evidence layer is incomplete, transient, degraded, demo-based or disconnected from the real runtime path.

This gate implements the project rule:

> A new layer may only be promoted when the previous layer is demonstrably stable, reliable and auditable.

## Canonical issue

- Canonical implementation issue: #188
- Duplicate issue closed: #190

## Scope

The gate applies before any of these claims are made:

- roadmap phase marked stable
- strategy promotion
- production-grade evidence claim
- paper-confidence authorization
- backtesting evidence promotion
- live-readiness claim
- decision-stack maturity claim

## Required evidence dimensions

A promoted evidence layer must prove all of the following:

1. Real-data backtests are coupled to the actual Scanner → Signal → Quality → Validator runtime path.
2. Decision-critical modules are runtime-reachable or explicitly non-runtime classified.
3. Paper Observation artifacts are durable, indexed and reviewable over time.
4. Historical inputs are persisted with reproducible checksums or manifests.
5. Report validation gates are robust and not dependent on brittle formatting assumptions.
6. Empty or no-signal states are explicitly classified and do not count as successful evidence runs by default.
7. Regime/VIX degradation is resolved through fallback/provenance or blocks evidence claims.

## Blocking issue references

The gate tracks these evidence-critical blockers:

- #177 — Couple real-data backtest to the actual Scanner → Signal → Quality → Validator pipeline.
- #178 — Enforce runtime reachability for decision-critical modules.
- #181 — Add durable evidence index for Paper Observation artifacts.
- #184 — Persist historical real-data backtest inputs for auditability.
- #185 — Fix daily report validation gate for Risk Tier detection.
- #186 — Block outcome tracking when upstream signal files are empty or invalid.
- #187 — Add robust VIX fallback or explicit regime block when VIX is unavailable.

If any required blocker is still open, promotion is blocked unless the gate input explicitly documents why that blocker is not applicable to the attempted claim.

## Gate states

The machine-readable gate result must be one of:

- `PASS` — all required evidence dimensions are satisfied and no blocking condition remains.
- `DEGRADED` — evidence is useful for research visibility, but it cannot support production-grade or strategy-promotion claims.
- `BLOCKED` — at least one required dimension is missing, unsafe or unresolved.

## Hard blocking conditions

The gate must return `BLOCKED` if any of the following is true:

- A production-grade or roadmap-promotion claim is attempted with `data_mode` equal to `demo`, `stub`, `synthetic`, `placeholder` or `degraded`.
- Real-data backtesting is not coupled to the actual runtime pipeline.
- Decision-critical modules are only unit-tested but not runtime-reachable or explicitly non-runtime classified.
- Paper Observation evidence lacks a durable index.
- Historical backtest inputs are not persisted with checksums or manifests.
- Report validation is missing or known brittle.
- Empty/no-signal states are not explicitly classified.
- VIX/regime degradation is neither resolved through provenance/fallback nor treated as a blocker.
- Required evidence fields such as `run_id`, `data_mode`, `provenance`, `checksum_or_manifest`, `runtime_trace` or `promotion_claim` are missing when a promotion claim is attempted.

## Machine-readable result schema

The result produced by `src/evidence_quality_gate.py` or `scripts/evaluate_evidence_quality_gate.py` must include:

```json
{
  "schema_version": 1,
  "gate": "Evidence Quality Gate #188",
  "status": "PASS|DEGRADED|BLOCKED",
  "blockers": [
    {
      "code": "string",
      "issue": "#188 or related issue",
      "reason": "human-readable explanation"
    }
  ],
  "warnings": ["string"],
  "data_mode": "real_data|demo|stub|synthetic|placeholder|degraded",
  "promotion_claim": false
}
```

## Validation command

Targeted guard command:

```bash
pytest tests/test_evidence_quality_gate_188.py -q
```

Optional machine-readable CLI evaluation:

```bash
python scripts/evaluate_evidence_quality_gate.py --input path/to/evidence_gate_input.json
```

## Boundary

This gate does not authorize live trading, broker execution or capital allocation.

This gate does not claim repository-wide full-regression green.

It is an evidence-governance layer. It prevents false promotion until runtime coupling, durability, provenance and degradation handling are proven.
