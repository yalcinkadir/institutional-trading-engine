# Regime Change Detection

Phase B4 adds a deterministic regime-change detector for forward paper observation.

The goal is to flag when market state changes enough that historical setup expectations should be treated with caution.

## Inputs

The detector accepts records with:

```text
regime or regime_label or state
volatility or volatility_percent or vix
correlation or cross_asset_correlation
drawdown or drawdown_pct
```

## Metrics

The report calculates:

```text
observations
lookback_window
latest_regime
previous_regime
label_change_count
label_change_rate
volatility_previous
volatility_latest
volatility_jump
correlation_previous
correlation_latest
correlation_jump
drawdown_previous
drawdown_latest
drawdown_jump
change_score
state
```

## States

```text
stable
regime_change_watch
regime_change_alert
unknown_regime
```

## Gates

Default fail-closed gates:

```text
min_observations = 20
max_change_score = 0.65
max_label_change_rate = 0.35
max_volatility_jump = 0.50
max_correlation_jump = 0.35
max_drawdown_jump = 0.08
require_latest_regime_known = true
```

A failure means forward evidence should be interpreted conservatively until the regime stabilizes.

## Outputs

The module can write:

```text
regime_change_detection.json
regime_change_detection.md
```

## Operational Rule

This is an evidence-quality and risk-context gate. A pass does not approve live capital. A regime-change alert should block escalation and trigger manual review.
