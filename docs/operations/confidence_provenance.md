# Confidence Provenance Boundary

Status date: 2026-06-12

Issue: #196

## Canonical path

The canonical confidence implementation is:

```text
src.decision_confidence.calculate_confidence_score
```

## Components

Canonical confidence uses three explicit components:

```text
setup_score
market_health_score
independent_regime_alignment_score
```

Weights:

```text
asset_setup: 0.45
market_health: 0.35
regime_alignment: 0.20
```

## Double-counting guard

`risk_tier` must not be used as independent regime evidence.

Reason:

```text
risk_tier is already derived from setup, regime, asymmetry and data-confidence inputs
```

When risk-tier information must influence confidence, it is represented only as:

```text
risk_tier_discount
```

and provenance must show:

```text
used_as_independent_regime_evidence: false
```

## Deprecated compatibility paths

The following helpers are retained only for historical compatibility:

```text
src.scoring.confidence_score.calculate_confidence_score
src.scoring.asset_score.calculate_asset_score
```

They emit `DeprecationWarning` and return metadata:

```text
deprecated: true
usage: research_only_legacy_compatibility
canonical_path: <canonical replacement>
```

## Required provenance fields

Confidence output must include:

```text
canonical_confidence_path
components
risk_tier_used_as_regime_alignment
double_counting_guard
legacy_tier_regime_mapping
```

## Boundary

This document defines confidence evidence quality only. It does not change execution behavior.
