from __future__ import annotations


def evaluate_event_risk(events: list[dict]) -> dict:
    risk_score = 100
    warnings: list[str] = []

    for event in events:
        severity = event.get("severity", "low")
        name = event.get("event", "Unknown")

        if severity == "high":
            risk_score -= 25
            warnings.append(f"High risk event: {name}")
        elif severity == "medium":
            risk_score -= 10
            warnings.append(f"Medium risk event: {name}")

    risk_score = max(risk_score, 0)

    if risk_score >= 80:
        classification = "Low Event Risk"
    elif risk_score >= 55:
        classification = "Moderate Event Risk"
    else:
        classification = "High Event Risk"

    return {
        "event_risk_score": risk_score,
        "classification": classification,
        "warnings": warnings,
    }
