# B1.1 Evidence Operation Discipline + TG2/TG3 Integration

B1.1 is the active observation-only operating discipline for the evidence pipeline. It does not add strategy complexity and does not authorize live execution.

## Scope

B1.1 connects three already separated concerns:

1. daily evidence report status
2. daily reconciliation cleanliness
3. TG2/TG3 research-only reporting delivery

The implementation adds:

```text
src/operations/evidence_operation_discipline.py
src/reporting/tg2_tg3_report_templates.py
tests/test_b11_evidence_operation_discipline.py
```

## Gates

The B1.1 operation record fails closed when:

- the observation mode is live, real-money or production-execution oriented
- the daily evidence report is missing
- the daily evidence report fails
- the reconciliation component is missing or failed
- required TG3 report templates are not rendered
- Telegram dispatch records are supplied but do not contain the TG1 research-only footer

## TG3 report templates

TG3 provides public-safe, research-only templates for:

- Daily Evidence
- Fill Quality
- Kill Switch
- Backtest Summary

Each template includes an explicit operation boundary:

- research and paper-observation only
- report delivery only
- no broker execution
- no live trading authorization
- no private edge parameters

## TG2 Telegram integration

TG2 uses the existing TG1 dispatcher boundary. Telegram dispatch is safe only when messages remain research-only and include:

```text
Research / Paper Observation Only. No live trading authorization.
```

Dry-run dispatch is sufficient for CI. Actual Telegram sending remains dependent on explicit runtime configuration and valid secrets.

## Test command

```bash
pytest tests/test_b11_evidence_operation_discipline.py -q
```

## Safety boundary

B1.1 is operational discipline only. It does not prove production edge, submit broker orders, enable live trading, expose private thresholds or replace the required 3-6 month observation period.
