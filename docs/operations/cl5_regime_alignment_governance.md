# CL5 Regime Alignment Governance

CL5 makes `regime_alignment` an explicit independent decision gate before risk-tier scoring can approve or watch a setup.

## Purpose

A candidate may have a strong setup score, good asymmetry and high data confidence while still being poorly aligned with the current market regime. CL5 prevents that case from being treated as merely a generic quality failure.

The goal is not to add a new predictive model. The goal is to make the existing regime-alignment contract fail closed and auditable.

## Implemented safeguards

```text
src/decision_engine.py
tests/test_decision_engine.py
```

Safeguards:

- `regime_alignment` is checked after hard risk overrides and setup-regime mapping, but before asymmetry, data-confidence and tier scoring.
- A candidate below the independent regime floor returns `NO_TRADE` with `poor_regime_alignment`.
- The decision notes include `regime_alignment_independent_gate` for auditability.
- The public-demo Tier 3 regime-alignment cutoff is reused as the fail-closed floor to avoid introducing new proprietary public constants.
- Custom threshold objects can tighten the regime-alignment floor without code changes.
- Ranking regression coverage proves that a high setup score cannot outrank an approved candidate when regime alignment fails.

## Test command

```bash
pytest tests/test_decision_engine.py -q
```

## Operational rule

A candidate with poor regime alignment must not be rescued by setup score, asymmetry score or data confidence. Regime mismatch is decision-critical context, not a cosmetic ranking detail.

## Safety note

CL5 improves decision-governance transparency only. It does not prove edge and does not authorize live trading.
