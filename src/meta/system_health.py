from __future__ import annotations


def evaluate_system_health(
    successful_runs: int,
    failed_runs: int,
    average_report_quality_score: float,
    data_fallback_rate: float,
) -> dict:
    total_runs = successful_runs + failed_runs
    uptime_score = 100 if total_runs == 0 else round((successful_runs / total_runs) * 100, 2)

    health_score = uptime_score * 0.4
    health_score += average_report_quality_score * 0.4
    health_score += max(0, 100 - data_fallback_rate) * 0.2
    health_score = round(max(0, min(health_score, 100)), 2)

    if health_score >= 85:
        status = "Healthy"
    elif health_score >= 70:
        status = "Stable"
    elif health_score >= 50:
        status = "Degraded"
    else:
        status = "Critical"

    return {
        "health_score": health_score,
        "uptime_score": uptime_score,
        "status": status,
    }
