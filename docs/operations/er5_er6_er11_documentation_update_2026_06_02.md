# ER5 / ER6 / ER11 Documentation Update — 2026-06-02

Status: documentation supplement / CI-green remediation recorded

## Purpose

This document captures the Roadmap / Changelog / README documentation update for the external-review remediation block:

```text
ER5 — Falsy-zero outcome metric substitution
ER6 — Missing result keys counted as breakeven evidence
ER11 — Expectancy Units / Naming Clarity
```

The repository-level files were inspected before documentation, following the project rule that documentation is updated only after the real files are checked.

## Verified source files

```text
ROADMAP.md
CHANGELOG.md
README.md
docs/operations/external_review_remediation_backlog_2026_06_01.md
```

## CI-green remediation summary

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

Relevant commits:

```text
419878b8a31b7de8cbac3c3afa085030d99fa59d
a7ad248b17d42cce4101503948f12cd1bb3b493e
8660b752e736513cd67d230364f7d6ec0358ba13
f5257df6485d3c835293b45e9a0a42c484186109
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

Relevant commits:

```text
5a931bda3edaec511f587c112d869bbe1cc3b9e8
0dfe9e8f13e9cf71856c6d07dfb9d87c44f60e7d
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

Relevant commits:

```text
bfad22fc357803c462b68f9e4dcf954242356e97
8a45637191913530f8ad4d78b6e6b1ca92b95b27
458e78a7b67c24450e90c8855eb04b6f302e485b
f5257df6485d3c835293b45e9a0a42c484186109
90951ccf1551da074ebe5e8fb42c19181e40907b
```

## Project status update text

Use this text in the root documentation status sections:

```text
ER5/ER6/ER11 external-review remediation is implemented and CI-green: falsy-zero outcome substitution is guarded, missing result evidence is surfaced instead of counted as breakeven, and expectancy units are explicit as expectancy_r.
```

## Changelog update text

Use this text in `CHANGELOG.md`:

```markdown
## ER5 / ER6 / ER11 External Review Remediation — 2026-06-02

### Fixed
- Preserved true `0.0` outcome results in expectancy adjustment instead of falling back to alternate metrics.
- Excluded missing result records from edge-evidence win/loss/breakeven metrics and surfaced `missing_result_count`.
- Renamed ambiguous expectancy outputs to explicit `expectancy_r` in the expectancy adjuster and decision-report payloads.

### Tests
- Added `tests/test_er5_expectancy_zero_result_guard.py`.
- Added `tests/test_er6_edge_evidence_missing_result_guard.py`.
- Added `tests/test_er11_expectancy_units_guard.py`.

### Status
- ER5: CLOSED_CI_GREEN.
- ER6: CLOSED_CI_GREEN.
- ER11: CLOSED_CI_GREEN.
- Live trading authorization: unchanged; not granted by code.
```

## Roadmap update text

Use this text in `ROADMAP.md` status sections:

```text
ER5/ER6/ER11 outcome/evidence metric remediation is implemented and CI-green. The system now preserves true zero outcomes, surfaces missing result evidence explicitly and uses expectancy_r for R-multiple expectancy semantics.
```

## README update text

Use this text in `README.md` Current Validation Status:

```text
ER5/ER6/ER11: outcome/evidence metric correctness and explicit expectancy_r units implemented and CI-green
```

## Safety boundary

This documentation update does not authorize live trading, broker execution, capital allocation or production deployment.

The system remains research / decision-support / paper-observation only.
