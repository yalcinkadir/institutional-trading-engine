# Adaptive Scoring Feedback Loop

## Purpose

The Adaptive Scoring Feedback Loop closes the learning cycle between historical signal outcomes and future market screening decisions.

The goal is not to create a black-box trading model.

The goal is to make the Decision Engine more adaptive while remaining:

- deterministic
- explainable
- testable
- auditable
- conservative

The system learns from historical outcomes only when those outcomes come from signals that actually triggered.

---

## Core Rule

```text
A signal is not a trade until its entry trigger is hit.
```

Therefore:

```text
PENDING / EXPIRED / UNTRIGGERED signals are not counted as losing trades.
```

They are useful signal-quality data, but they are not used as executed trade outcomes for expectancy scoring.

---

## End-to-End Flow

```text
reports/signals/YYYY-MM-DD-signals.json
    ↓
entry_exit_watcher.py
    ↓
data/signal_lifecycle.jsonl
reports/alerts/YYYY-MM-DD-alerts.json
    ↓
generate_outcomes.py
    ↓
reports/outcomes/outcome-history.json
    ↓
expectancy_adjuster.py
    ↓
decision_report.py
    ↓
setup_score / position_size adjustments
    ↓
report_formatter.py
    ↓
generate_report.py
    ↓
data/scoring_adjustment_history.json
```

This creates the closed loop:

```text
Signal → Lifecycle → Outcome → Expectancy → Score Adjustment → Audit History → Future Signal
```

---

## Key Files

### Outcome History

```text
reports/outcomes/outcome-history.json
```

Stores historical lifecycle-aware outcomes.

Used by:

```text
src/scoring/expectancy_adjuster.py
```

---

### Expectancy Adjuster

```text
src/scoring/expectancy_adjuster.py
```

Responsibilities:

- read `outcome-history.json`
- ignore non-trading lifecycle statuses
- build setup/regime/entry profiles
- apply conservative score and size adjustments
- return deterministic adjustment metadata

Profile hierarchy:

```text
1. market_state::setup_type::entry_type
2. market_state::setup_type
3. setup_type
```

The most specific profile wins if it has enough samples.

---

### Decision Report Integration

```text
src/reporting/decision_report.py
```

Responsibilities:

- create Decision Engine candidates
- apply expectancy-based score adjustments before ranking
- apply size multipliers after candidate evaluation
- expose all adjustment metadata in the decision payload

Important:

```text
Positive expectancy does not override partial data quality.
```

If market data quality is PARTIAL, positive score boosts are ignored.

Negative expectancy remains effective because it is a risk reduction.

---

### Report Formatter

```text
src/reporting/report_formatter.py
```

Responsibilities:

- show base vs adjusted setup score
- show profile key
- show score delta
- show size multiplier
- show sample size / win rate / expectancy

This ensures every adaptive adjustment is visible in the human-readable report.

---

### Adjustment History

```text
src/scoring/adjustment_history.py
data/scoring_adjustment_history.json
```

Responsibilities:

- persist only real score/size adjustments
- skip no-op profiles
- deduplicate same run/symbol/profile records
- retain a bounded history
- make adaptive scoring auditable

---

## Adjustment Rules

Minimum sample size:

```text
5 evaluated triggered outcomes
```

No profile with enough samples:

```text
score_delta = 0
size_multiplier = 1.0
```

Positive expectancy:

```text
expectancy >= 1.0 and win_rate >= 0.52
→ score +4
→ size ×1.05
```

Strong positive expectancy:

```text
expectancy >= 3.0 and win_rate >= 0.60
→ score +8
→ size ×1.15
```

Weak expectancy:

```text
expectancy < -0.5
→ score -6
→ size ×0.75
```

Negative expectancy:

```text
expectancy <= -2.0 or win_rate <= 0.35
→ score -12
→ size ×0.50
```

---

## Data Quality Guardrail

Positive expectancy is ignored when current data quality is not LIVE.

Reason:

```text
Historical edge should not make the system aggressive when current input quality is degraded.
```

Negative expectancy is still applied.

Reason:

```text
Risk reduction remains valid even during degraded data conditions.
```

---

## Example Adjustment Record

```json
{
  "timestamp_utc": "2026-05-20T21:00:00+00:00",
  "run_id": "postmarket-2026-05-20T21:00:00Z",
  "report_type": "postmarket",
  "symbol": "NVDA",
  "setup_type": "momentum_breakout",
  "market_state": "low_vol_bull",
  "entry_type": "break_above",
  "profile_key": "regime_setup_entry::low_vol_bull::momentum_breakout::break_above",
  "source": "regime_setup_entry",
  "sample_size": 6,
  "win_rate": 0.67,
  "expectancy": 2.0,
  "base_score": 82,
  "score_delta": 4,
  "final_score": 86,
  "base_size": 1.0,
  "size_multiplier": 1.05,
  "final_size": 1.05,
  "recommendation": "maintain_or_slightly_increase",
  "reason": "positive_expectancy",
  "decision": "approved",
  "risk_tier": "tier_1"
}
```

---

## Testing

Relevant tests:

```bash
pytest tests/test_expectancy_adjuster.py
pytest tests/test_decision_report_expectancy_integration.py
pytest tests/test_adjustment_history.py
```

Covered behavior:

- missing history returns no adjustment
- insufficient samples return no adjustment
- positive expectancy increases score/size
- strong positive expectancy increases more
- negative expectancy reduces score/size
- expired/untriggered statuses are ignored
- fallback from entry-specific to broader profiles
- decision report actually applies adjustments
- partial data blocks positive boosts
- adjustment history persists and deduplicates records

---

## Current Limitations

The feedback loop is intentionally conservative.

Current limitations:

- no Bayesian confidence model yet
- no regime-similarity memory yet
- no decay weighting by recency yet
- no per-symbol profile weighting yet
- no portfolio-level adjustment yet
- no dashboard visualization yet
- no Postgres persistence yet

These are future enhancements.

The current version is a deterministic, auditable adaptive scoring layer.
