# ER12 / ER13 Evidence Caveats and Accounting Precision CI-Green Closure — 2026-06-02

Status: closed / CI-green by user confirmation

## Scope

```text
ER12 — Sharpe evidence caveats / small-sample and IID assumptions
ER13 — Money / PnL float accounting precision review
```

## TEST1 workflow

```text
real evidence and risk files inspected
guard test added
minimal implementation added
CI failure inspected
hygiene leak fixed
CI confirmed green by user
Doku updated after green validation
```

## Findings

ER12:

```text
Historical edge reports exposed per-trade Sharpe and deflated Sharpe metrics, but did not explicitly surface caveats for population standard deviation, unverified IID assumptions, small-sample warnings and the fact that research diagnostics are not proof of live edge.
```

ER13:

```text
Position-risk money fields used float arithmetic at accounting boundaries.
```

## Implemented remediation

ER12:

```text
HistoricalEdgeCaveats added
report.to_dict()["caveats"] added
Markdown section "Sharpe caveats" added
population_std explicitly documented
IID assumption explicitly marked not_verified
small_sample_warning exposed
not_proof_of_edge exposed
```

ER13:

```text
Decimal-based money arithmetic added to calculate_position_risk
cent-stable rounding added for risk_amount, risk_per_share, notional and notional_cap
whole-share rounding remains deterministic via ROUND_DOWN
public output remains backward-compatible JSON-safe float values
```

Artifact hygiene:

```text
reports/postmarket-report.md restored to synthetic public-safe example after generated report content was detected by the hygiene guard
```

## Files

```text
src/validation/historical_edge_validation.py
src/trading/risk_engine.py
tests/test_er12_er13_evidence_accounting_precision_guard.py
reports/postmarket-report.md
```

## Guard coverage

```text
tests/test_er12_er13_evidence_accounting_precision_guard.py
tests/test_historical_edge_validation.py
tests/test_artifact_hygiene.py
```

Validated behavior:

```text
historical edge JSON exposes caveats
historical edge Markdown exposes Sharpe caveats
small-sample caveat is surfaced
Sharpe metrics are explicitly not proof of live edge
position-risk accounting returns cent-stable values
public report examples remain synthetic / public-safe
```

## CI confirmation

The user confirmed the CI workflow is green after ER12/ER13 implementation and the artifact hygiene fix.

Recommended verification commands:

```bash
pytest tests/test_er12_er13_evidence_accounting_precision_guard.py -q
pytest tests/test_historical_edge_validation.py -q
pytest tests/test_artifact_hygiene.py -q
pytest -q
```

## Safety boundary

This closure does not authorize live trading, broker execution, capital allocation or production deployment.

The system remains research / decision-support / paper-observation only.
