# P47: Final Live Readiness Gate

## Purpose

P47 consolidates all validation evidence before any real-capital decision can be reviewed.

It is a decision-support gate only. It does not authorize trading, connect to a broker, or execute orders.

## Inputs

The gate consumes evidence from the validation stack:

```text
P41 historical edge validation
P42 regime-phase matrix
P43 walk-forward validation
P44 execution realism layer
P45 out-of-sample validation lockbox
P46 paper trading journal / live observation v2
```

## Required Evidence

All core gates must pass:

```text
historical_edge_passed
regime_phase_passed
walk_forward_passed
execution_realism_passed
out_of_sample_passed
paper_observation_passed
manual_review_completed
risk_limits_defined
kill_switch_defined
```

## Paper Observation Requirements

```text
minimum observation duration: 3 months
preferred observation duration: 6 months if no meaningful regime shift occurs
paper/live quality retention: at least 85% of expected paper/backtest quality
```

## Kill-Switch Rule

```text
live drawdown kill switch must be <= 1.5x backtest max drawdown
```

Default review rules:

```text
Stop and review if live drawdown exceeds configured multiple.
Stop and review if live/paper metrics fall below 85% of expectation.
Stop and review after unexplained execution deviation clusters.
Stop and review after manual protocol breach clusters.
```

## Staged Capital-Risk Phases

The report defines staged review phases but does not authorize trading.

```text
Months 1-3:  max 50% size after all gates and manual review pass
Months 4-6:  max 75% size if observed metrics remain >=85% of expectation
Month 7+:    max 100% only if cumulatively profitable and drawdown remains below kill switch
```

## Readiness Levels

```text
NOT_READY
OBSERVATION_ONLY
REVIEW_READY
```

`REVIEW_READY` means the evidence is complete enough for human review. It does not mean live trading is approved.

## Example

```python
from src.validation.final_live_readiness_gate import (
    FinalReadinessEvidence,
    evaluate_final_live_readiness,
)

evidence = FinalReadinessEvidence(
    historical_edge_passed=True,
    regime_phase_passed=True,
    walk_forward_passed=True,
    execution_realism_passed=True,
    out_of_sample_passed=True,
    paper_observation_passed=True,
    paper_observation_months=6,
    paper_vs_backtest_ratio=0.9,
    manual_review_completed=True,
    risk_limits_defined=True,
    kill_switch_defined=True,
)

report = evaluate_final_live_readiness(evidence)
```

## Report Helpers

```python
from pathlib import Path
from src.validation.final_live_readiness_gate import write_final_live_readiness_report

write_final_live_readiness_report(
    report,
    json_path=Path("reports/validation/final-live-readiness.json"),
    markdown_path=Path("reports/validation/final-live-readiness.md"),
)
```

## Tests

```bash
pytest tests/test_final_live_readiness_gate.py
```

## Guardrails

```text
Decision-support only.
No broker integration.
No order execution.
No automatic live-trading authorization.
Code quality is not trading edge.
```
