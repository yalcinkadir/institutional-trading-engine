# VIX / Market Regime Policy

Status date: 2026-06-11

Issue: #187

## Purpose

Market regime evidence must never silently degrade into an unexplained `Unknown` state.

If VIX is available, the system uses direct VIX evidence. If VIX is unavailable but the configured volatility proxy is available, the system uses degraded proxy evidence. If neither VIX nor proxy evidence is available, or index trend inputs are unavailable, the market regime is explicitly blocked.

## Canonical VIX source

```text
I:VIX
```

Provider:

```text
Polygon.io daily aggregates
```

## Default volatility proxy

```text
VIXY
```

Config override:

```text
VOLATILITY_PROXY_SYMBOL
```

## Policy outcomes

### VIX available

```text
regime_policy.status: LIVE
regime_policy.source: polygon
regime_policy.fallback_used: false
regime_policy.confidence: FULL
regime_policy.action: ALLOW
```

### VIX unavailable, proxy available

```text
regime_policy.status: DEGRADED
regime_policy.source: polygon_proxy
regime_policy.fallback_used: true
regime_policy.confidence: DEGRADED
regime_policy.action: DEGRADE
regime_input.vix.status: PROXY_DEGRADED
```

Proxy evidence is not full VIX validation. It may support degraded Paper Observation reporting, but it must not be promoted as fully validated VIX evidence.

### VIX unavailable, proxy unavailable

```text
regime: BLOCKED_MARKET_REGIME_UNAVAILABLE
regime_policy.status: BLOCKED
regime_policy.action: BLOCK
regime_policy.confidence: BLOCKED
regime_validation_status: BLOCKED
```

### Index trend unavailable

```text
regime: BLOCKED_MARKET_REGIME_UNAVAILABLE
regime_policy.status: BLOCKED
regime_policy.action: BLOCK
regime_policy.confidence: BLOCKED
```

## Required payload fields

Every market regime summary must include:

```text
regime
regime_validation_status
regime_policy
regime_input
```

`regime_policy` must include:

```text
status
source
fallback_used
confidence
action
reason
vix_status
vix_validation_status
index_trend_status
proxy_symbol
```

## Forbidden behavior

Reports must not emit unexplained:

```text
regime: Unknown
```

When inputs are missing, the state must be one of:

```text
DEGRADED
BLOCKED_MARKET_REGIME_UNAVAILABLE
```

## Safety boundary

This policy only governs market-regime evidence quality.

It does not authorize broker execution, production deployment, capital allocation or live trading.
