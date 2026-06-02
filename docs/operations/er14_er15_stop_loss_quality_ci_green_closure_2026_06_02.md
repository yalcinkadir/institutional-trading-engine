# ER14 / ER15 Stop-Loss Quality CI-Green Closure — 2026-06-02

Status: closed / CI-green by user confirmation

## Scope

```text
ER14 — Long-only stop logic lacks explicit short guard
ER15 — ATR fallback stops may lack max-distance cap comparable to swing stop cap
```

## TEST1 workflow

```text
real stop-loss files inspected
guard test added
minimal implementation added
existing tests run
text compatibility fix applied
CI confirmed green
documentation updated after green validation
```

## Findings

ER14:

```text
The stop-loss quality engine was documented as long-side, but unsupported short-side requests were not explicitly rejected.
```

ER15:

```text
Swing-low structure stops had a max ATR-distance quality check, but scanner-provided stops and ATR fallback stops did not share a central max-distance guard.
```

## Implemented remediation

```text
SUPPORTED_SIDE = "long"
MAX_ATR_STOP_DISTANCE = 2.0
side="long" default added to derive_stop_loss_quality
unsupported non-long side fails closed with unsupported_side:<side>
scanner-provided stops farther than max ATR distance fail closed
ATR fallback stop uses MAX_ATR_STOP_DISTANCE and declares max 2.0 ATR in reason
existing scanner-provided valid stop reason remains backward compatible
```

## Files

```text
src/signals/stop_loss_quality.py
tests/test_er14_er15_stop_loss_quality_guard.py
tests/test_stop_loss_quality.py
```

## Guard coverage

```text
tests/test_er14_er15_stop_loss_quality_guard.py
```

Validated behavior:

```text
short-side stop requests are explicitly rejected until supported
scanner-provided stops exceeding max ATR distance are rejected
ATR fallback stop declares and respects max 2.0 ATR distance
existing stop-loss quality tests remain green
```

## CI confirmation

The user confirmed CI is green after ER14/ER15 implementation and compatibility fix.

Recommended verification commands:

```bash
pytest tests/test_er14_er15_stop_loss_quality_guard.py -q
pytest tests/test_stop_loss_quality.py -q
pytest -q
```

## Safety boundary

This closure does not authorize live trading, broker execution, capital allocation or production deployment.

The system remains research / decision-support / paper-observation only.
