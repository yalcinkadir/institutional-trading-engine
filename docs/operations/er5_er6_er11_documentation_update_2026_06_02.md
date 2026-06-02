# ER5 / ER6 / ER11 Documentation Update — 2026-06-02

Status: documentation supplement / CI-green remediation recorded

## Purpose

This document captures the Roadmap / Changelog / README / Backlog documentation update for the external-review remediation block:

```text
ER5 — Falsy-zero outcome metric substitution
ER6 — Missing result keys counted as breakeven evidence
ER11 — Expectancy Units / Naming Clarity
```

The repository-level files were inspected before documentation, following the project rule that documentation is updated only after the real files are checked.

## Replacement Files Generated

The following full replacement files were generated:

```text
README.md
ROADMAP.md
CHANGELOG.md
docs/operations/external_review_remediation_backlog_2026_06_01.md
docs/operations/er5_er6_er11_documentation_update_2026_06_02.md
```

## CI-Green Remediation Summary

### ER5

Implemented behavior:

```text
A true 0.0 result is preserved and is not replaced by a fallback metric.
Flat 0.0R expectancy remains neutral rather than negative/blocking.
```

Files:

```text
src/scoring/expectancy_adjuster.py
tests/test_er5_expectancy_zero_result_guard.py
```

Status:

```text
CLOSED_CI_GREEN
```

### ER6

Implemented behavior:

```text
Missing result_r records are no longer counted as artificial 0.0 breakeven evidence.
Missing result records are surfaced as missing_result_count.
True 0.0 values remain valid breakeven records.
```

Files:

```text
src/backtesting/edge_evidence_backtest.py
tests/test_er6_edge_evidence_missing_result_guard.py
```

Status:

```text
CLOSED_CI_GREEN
```

### ER11

Implemented behavior:

```text
Ambiguous expectancy field names were made explicit as expectancy_r.
Decision report payloads now expose expectancy_r instead of a naked expectancy key.
The unit means average R-multiple per evaluated trade/outcome profile.
```

Files:

```text
src/scoring/expectancy_adjuster.py
src/reporting/decision_report.py
tests/test_er11_expectancy_units_guard.py
```

Status:

```text
CLOSED_CI_GREEN
```

## Recommended Verification Commands

```bash
pytest tests/test_er5_expectancy_zero_result_guard.py -q
pytest tests/test_er6_edge_evidence_missing_result_guard.py -q
pytest tests/test_er11_expectancy_units_guard.py -q
pytest tests/test_expectancy_adjuster.py -q
pytest tests/test_edge_evidence_backtest.py -q
pytest tests/test_decision_report.py -q
pytest -q
```

## Safety Boundary

This documentation update does not authorize live trading, broker execution, capital allocation or production deployment.

The system remains research / decision-support / paper-observation only.
