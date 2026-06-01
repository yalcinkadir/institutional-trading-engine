# ER3 / ER4 CI-Green Closure — 2026-06-01

Status: closed / CI-green by user confirmation

## Scope

This closure note records the validated completion of two external-review remediation items:

```text
ER3 — Notional / Buying-Power Capped Position Sizing
ER4 — Portfolio State Atomic Persistence and Fail-Closed Invalid Loads
```

## TEST1 workflow evidence

The remediation followed TEST1 Evidence-Oriented TDD Policy:

```text
1. Guard tests first
2. Minimal code fix second
3. Targeted test execution
4. Relevant module tests
5. Full suite confirmation
6. Documentation after green validation
```

## ER3 result

Finding:

```text
Position sizing capped risk amount but not notional exposure.
Tight stops could create unintended leverage.
```

Implemented behavior:

```text
buying_power and max_notional cap shares
zero or negative notional cap produces zero shares
returned result includes notional and notional_cap
```

Files:

```text
src/trading/risk_engine.py
tests/test_risk_engine_notional_cap.py
```

Relevant commits:

```text
3510da3f10906375007e0990678b01ee72208503
e8786a3e1d758c46d5cee5d1ad7fffcf1fa15236
```

Status:

```text
CLOSED_CI_GREEN
```

## ER4 result

Finding:

```text
Portfolio state persistence used direct writes and invalid JSON could crash instead of failing closed.
```

Implemented behavior:

```text
PortfolioStateStore.save writes through tmp file and os.replace
invalid/corrupt portfolio_state.json returns fail-closed state
non-object state returns fail-closed state
missing required fields return fail-closed state
non-finite numeric values return fail-closed state
governance_valid is false for invalid state
```

Files:

```text
src/runtime/portfolio_state.py
tests/test_er4_portfolio_state_fail_closed_atomic_guard.py
tests/test_portfolio_state.py
```

Relevant commits:

```text
fe68220d5b95f9b6c73262443bcb3cc2f728be6c
1958882b474265add2ef97861d991113ad428e11
694df2f91cc2e4c33c0235435511fc79236f8bee
```

Status:

```text
CLOSED_CI_GREEN
```

## CI confirmation

The user confirmed that the last test run is green after the final remediation commits.

Recommended verification commands:

```bash
pytest tests/test_risk_engine_notional_cap.py -q
pytest tests/test_er4_portfolio_state_fail_closed_atomic_guard.py -q
pytest tests/test_portfolio_state.py -q
pytest -q
```

## Safety boundary

This closure does not authorize live trading, broker execution, capital allocation or production deployment.

The system remains research / decision-support / paper-observation only.
