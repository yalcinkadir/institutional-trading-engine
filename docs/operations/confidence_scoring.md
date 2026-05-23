# Confidence Score Cleanup

P36 separates confidence scoring into three independent layers.

## Layers

```text
asset setup score
market health score
regime alignment score
```

## Formula

```text
confidence = setup_score * 0.45 + market_health_score * 0.35 + regime_alignment_score * 0.20
```

The result is clamped to the 0..100 range.

## Regime Alignment Mapping

```text
Tier 1   100
Tier 2    65
Tier 3    35
No Trade   0
```

## Implementation

```text
src/decision_confidence.py
tests/test_decision_confidence.py
```

## Test Command

```bash
pytest tests/test_decision_confidence.py
```

## Notes

VIX and market breadth are not direct inputs to this helper.
They belong inside market health and should not be counted again here.

## Boundary

P36 changes decision-support confidence scoring only.
It does not add broker connectivity or order execution.
