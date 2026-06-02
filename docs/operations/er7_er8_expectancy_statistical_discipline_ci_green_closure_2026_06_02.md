# ER7 / ER8 Expectancy Statistical Discipline CI-Green Closure — 2026-06-02

Status: closed / CI-green by user confirmation

## Scope

```text
ER7 — sample discipline for expectancy-based adjustment
ER8 — positive asymmetric expectancy handling
```

## TEST1 workflow

```text
real files inspected
guard test added
minimal implementation added
existing tests reconciled
CI confirmed green
documentation updated after green validation
```

## Implemented remediation

The expectancy adjuster now separates score evidence from size evidence.

```text
MIN_SAMPLES = 5
MIN_SIZE_ADJUSTMENT_SAMPLES = 20
```

Below the stronger size-evidence floor, score can still react to evidence, but the multiplier remains neutral.

Positive asymmetric expectancy is no longer blocked solely by low win rate when expectancy is materially positive.

## Files

```text
src/scoring/expectancy_adjuster.py
tests/test_er7_er8_expectancy_statistical_discipline.py
tests/test_expectancy_adjuster.py
reports/premarket-report.md
```

## Guard coverage

```text
tests/test_er7_er8_expectancy_statistical_discipline.py
```

Validated behavior:

```text
positive profiles below size-evidence floor can score while multiplier remains neutral
negative profiles below size-evidence floor can reduce score while multiplier remains neutral
positive asymmetric profiles are not blocked only because win rate is low
```

Existing expectancy tests now also cover:

```text
6 samples: score adjustment allowed, multiplier neutral
20 samples: score adjustment allowed, multiplier can change
```

## CI confirmation

The user confirmed CI is green after implementation, test reconciliation and artifact hygiene fix.

Recommended verification commands:

```bash
pytest tests/test_er7_er8_expectancy_statistical_discipline.py -q
pytest tests/test_expectancy_adjuster.py -q
pytest tests/test_artifact_hygiene.py -q
pytest -q
```

## Safety boundary

This closure does not authorize live trading, broker execution, capital allocation or production deployment.

The system remains research / decision-support / paper-observation only.
