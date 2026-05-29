# CL2 Scoring System Audit

Status date: 2026-05-29

CL2 makes score usage explicit and auditable. The main rule is simple: report-only scores may help humans read reports, but they must not be treated as Decision Engine approval, paper execution permission or live trading authorization.

## Core Module

```text
src/validation/scoring_audit.py
```

Main entry points:

```text
audit_score_systems(...)
render_score_audit_markdown(...)
```

## Registered Score Systems

```text
live_setup_scoring
```

Decision input produced by `src/setup_scoring.py`. It feeds `SetupCandidate.setup_score` and can be used by reporting, but its public constants are demo defaults only.

```text
decision_engine_tier_gate
```

Decision-authoritative gate produced by `src/decision_engine.py`. This is the downstream gate for risk tiering and paper/execution workflow eligibility.

```text
report_ranking_score
```

Presentation-only score used by reports and report builders. It is not decision-authoritative and must not feed paper/execution gates.

## Audit Rules

The audit fails if:

```text
score-system names are duplicated
no decision-authoritative score/gate is declared
a report-only score is marked decision-authoritative
a non-authoritative score feeds a paper/execution gate
a score system lacks module or field references
```

## Safety Boundary

CL2 does not prove edge. It prevents a dangerous category error: treating visual report ranking as if it were Decision Engine approval.

## Test Coverage

```bash
pytest tests/test_scoring_audit.py -q
```

Covered scenarios:

```text
public score registry passes cleanly
report ranking score remains non-authoritative
Decision Engine tier gate remains authoritative for paper/execution gating
invalid report-only authoritative score is rejected
non-authoritative paper/execution gate score is rejected
Markdown audit report renders the separation boundary
```
