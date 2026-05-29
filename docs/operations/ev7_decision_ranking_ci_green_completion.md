# EV7 Decision Ranking CI-Green Completion

Status date: 2026-05-29

## Result

EV7 Decision Engine WATCH / REDUCED_SIZE ranking remediation is confirmed CI-green.

```text
EV7 tier-aware decision ranking: implemented
Targeted decision-engine regression tests: passed
Main CI: green
Live trading authorization: unchanged; not granted by code
```

## Completed scope

### EV7 — Tier-3 reduced-size ranking inversion

`rank_candidates` no longer lets a Tier-3 candidate with `REDUCED_SIZE` outrank a clean Tier-3 `WATCH` candidate just because `REDUCED_SIZE` previously had a globally higher priority than `WATCH`.

The ranking rule is now tier-aware:

```text
APPROVED candidates remain highest priority.
REDUCED_SIZE Tier-1 / Tier-2 candidates can still rank above Tier-3 WATCH.
Clean Tier-3 WATCH ranks above Tier-3 REDUCED_SIZE.
NO_TRADE and BLOCKED remain below tradable/watch candidates.
```

## Regression coverage

```text
tests/test_decision_engine.py
```

Added EV7 regression cases:

```text
test_ev7_tier3_reduced_size_does_not_outrank_clean_tier3_watch
test_ev7_reduced_tier2_can_still_rank_above_tier3_watch
```

## CI coverage

The main CI workflow includes a dedicated EV7 regression step:

```text
pytest tests/test_decision_engine.py -q
```

## Operational boundary

This fix improves ranking safety and candidate ordering. It does not prove trading edge, enable broker execution, authorize live trading, replace the 3-6 month paper-observation period, or approve real-money deployment.

## Next block

The next recommended remediation is one of:

```text
EV10 profit_factor=inf degradation handling
EV11 conservative missing-indicator scoring fallbacks
EV8 walk-forward naming / train-test semantics clarification
```
