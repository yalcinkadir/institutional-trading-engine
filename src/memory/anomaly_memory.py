from __future__ import annotations


def detect_market_anomalies(events: list[dict]) -> dict:
    anomalies = [event for event in events if event.get("anomaly") is True]

    severe = [
        event
        for event in anomalies
        if event.get("severity") in {"high", "critical"}
    ]

    return {
        "anomaly_count": len(anomalies),
        "severe_count": len(severe),
        "classification": classify_anomaly_environment(len(severe)),
    }


def classify_anomaly_environment(severe_count: int) -> str:
    if severe_count >= 5:
        return "Extreme Instability"
    if severe_count >= 3:
        return "Elevated Instability"
    if severe_count >= 1:
        return "Watchlist Environment"
    return "Stable"
