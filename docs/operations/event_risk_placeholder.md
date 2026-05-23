# Event Risk Placeholder

P33 adds explicit metadata for event-risk assessments.

Implemented in:

```text
src/event_risk_engine.py
tests/test_event_risk_engine.py
```

Assessment fields:

```text
event_risk_available
event_risk_source
event_risk_confidence
event_risk_is_placeholder
```

Default metadata:

```text
event_risk_available=false
event_risk_source=static_placeholder
event_risk_confidence=low
event_risk_is_placeholder=true
```

Default warning:

```text
event_risk_not_backed_by_live_calendar_feed
```

Test command:

```bash
pytest tests/test_event_risk_engine.py
```
