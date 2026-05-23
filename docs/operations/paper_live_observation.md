# Paper-Live Observation

P26 adds a paper-live observation layer before any trading decision.

It reads local artifacts and produces an operational readiness report.

It does not call a broker and does not place trades.

---

## Local Command

```bash
python scripts/run_paper_live_observation.py \
  --signals-file reports/signals/latest-signals.json \
  --lifecycle-file data/signal_lifecycle.jsonl \
  --alerts-file reports/alerts/latest-alerts.json \
  --min-lifecycle-events 5
```

Require alert evidence:

```bash
python scripts/run_paper_live_observation.py \
  --signals-file reports/signals/latest-signals.json \
  --lifecycle-file data/signal_lifecycle.jsonl \
  --alerts-file reports/alerts/latest-alerts.json \
  --min-lifecycle-events 5 \
  --require-alerts
```

Default outputs:

```text
reports/paper-live/paper-live-observation.json
reports/paper-live/paper-live-observation.md
```

---

## GitHub Actions Workflow

```text
Actions → Paper Live Observation → Run workflow
```

Recommended first run:

```text
signals_file: reports/signals/latest-signals.json
lifecycle_file: data/signal_lifecycle.jsonl
alerts_file: reports/alerts/latest-alerts.json
min_lifecycle_events: 5
require_alerts: false
```

Artifact:

```text
paper-live-observation-artifacts
```

Expected report files:

```text
reports/paper-live/paper-live-observation.json
reports/paper-live/paper-live-observation.md
```

---

## Gates

P26 validates:

```text
signals_file_present
signals_loaded
lifecycle_file_readable
minimum_lifecycle_events
terminal_events_observed
alerts_observed, only when require_alerts=true
```

---

## Report Summary

The report includes:

```text
ready_for_review
signal_count
buy_watch_count
lifecycle_event_count
terminal_event_count
alert_count
lifecycle_event_types
gates
```

---

## Terminal Events

Terminal/meaningful lifecycle events include:

```text
STOP_HIT
TARGET_1_HIT
TARGET_2_HIT
EXPIRED
CANCELLED_BY_REGIME_CHANGE
REGIME_INVALIDATION_EXIT
```

---

## Interpretation

```text
ready_for_review=false
```

means paper-live evidence is insufficient.

```text
ready_for_review=true
```

means artifacts are present and observation gates passed. It still does not authorize trading.

---

## Strict Guardrail

```text
Paper-live observation is decision-support evidence only.
No broker execution.
No automatic live orders.
No real trading decision without review.
```

---

## Next Step After P26

After enough green paper-live observation runs:

```text
review paper-live reports
inspect false breakouts and terminal event distribution
review notification reliability
review governance state
only then discuss whether live decision-support scheduling is acceptable
```
