# Institutional Reports Archive

This directory contains all generated institutional market reports.

---

## Report Types

### Premarket Report

Purpose:
Prepare for the upcoming US market session.

Schedule:
Sunday to Friday before the US market open.

Contains:
- market regime
- volatility structure
- watchlist candidates
- setup readiness
- event risks
- cross-asset analysis
- institutional positioning

Use cases:
- pre-session planning
- entry preparation
- risk reduction
- focus selection

Location:

```text
reports/premarket/
```

Latest version:

```text
reports/premarket-report.md
```

---

### Postmarket Report

Purpose:
Analyze the completed session after the market close.

Schedule:
Monday to Friday after the US market close.

Contains:
- market review
- leaders and weak names
- relative strength
- failed breakouts
- volatility expansion
- signal validation
- sector rotation

Use cases:
- swing trade preparation
- performance review
- watchlist updates
- risk reassessment

Location:

```text
reports/postmarket/
```

Latest version:

```text
reports/postmarket-report.md
```

---

### Weekly Institutional Report

Purpose:
Strategic institutional-level weekly review.

Schedule:
Every Saturday.

Contains:
- weekly winners and losers
- strategy review
- signal quality review
- regime evolution
- sector rotation
- macro risk analysis
- adaptive intelligence review

Use cases:
- strategic positioning
- outcome analysis
- portfolio rotation
- long-term regime understanding

Location:

```text
reports/weekly/
```

Latest version:

```text
reports/weekly-report.md
```

---

## Outcome Tracking

Outcome tracking data is stored under:

```text
reports/outcomes/
```

Purpose:
- measure signal quality
- analyze recommendation performance
- evaluate setup reliability
- compare regimes historically
- support adaptive intelligence

---

## Artifacts

Every workflow execution also uploads:

- dated report artifacts
- full report archive snapshots

GitHub Actions therefore acts as:
- historical archive
- audit trail
- institutional memory layer

---

## Quality Validation

All reports are validated before:

- repository commit
- Telegram delivery
- artifact upload

Validation script:

```bash
python scripts/validate_report_quality.py
```

Minimum score:

```text
75
```
