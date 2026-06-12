# Decision Report Scoring Provenance

Status date: 2026-06-12

Issue: #180

## Purpose

Decision report scores must not contain hidden placeholder or symbol-name-derived scoring components.

A numeric report score is only useful when its inputs are explicit and auditable.

## Current scoring inputs

Report-level score provenance is exported under:

```text
score_provenance
```

Each decision also carries its own:

```text
score_provenance
```

Allowed score inputs:

```text
market_state_base_score
scanner_trend_score
scanner_volume_score
scanner_volatility_score
scanner_setup_quality_score
scanner_liquidity_score
regime_alignment
asymmetry_score
data_confidence
historical_expectancy_adjustment
```

## Scanner metric fields

When available, decision reports read scanner-derived symbol evidence from one of these screener fields:

```text
scanner_metrics
scanner_metrics_map
symbol_metrics
metrics
```

Per-symbol scanner metrics may include:

```text
trend_score
volume_score
volatility_score
setup_quality_score
liquidity_score
```

Values may be expressed as `0.0..1.0` or `0..100` and are normalized into `0.0..1.0`.

## Missing scanner metrics

Missing scanner metrics are neutral:

```text
setup_score_source: market_context_neutral_no_placeholder
scanner_evidence_component: 0.0
placeholder_score_contribution: 0.0
```

This keeps report generation deterministic while preventing hidden placeholder values from contributing to readiness or confidence.

## Forbidden behavior

The following must remain disabled:

```text
symbol_name_score_enabled: false
placeholder_scoring_allowed: false
placeholder_score_contribution: 0.0
```

Symbol names must not be used as score inputs.
