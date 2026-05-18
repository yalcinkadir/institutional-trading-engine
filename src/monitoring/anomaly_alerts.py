from __future__ import annotations


def detect_operational_anomalies(metrics: dict[str, float]) -> dict:
    alerts: list[str] = []

    latency = metrics.get("latency_ms", 0)
    failure_rate = metrics.get("failure_rate_percent", 0)
    cache_hit_rate = metrics.get("cache_hit_rate_percent", 100)

    if latency > 5000:
        alerts.append("high_latency")

    if failure_rate > 10:
        alerts.append("high_failure_rate")

    if cache_hit_rate < 40:
        alerts.append("low_cache_efficiency")

    severity = "NORMAL"

    if len(alerts) >= 3:
        severity = "CRITICAL"
    elif len(alerts) == 2:
        severity = "HIGH"
    elif len(alerts) == 1:
        severity = "MODERATE"

    return {
        "severity": severity,
        "alerts": alerts,
    }
