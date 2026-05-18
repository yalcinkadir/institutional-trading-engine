from __future__ import annotations


def audit_decisions(decisions: list[dict]) -> dict:
    if not decisions:
        return {
            "decisions": 0,
            "average_quality": 0,
            "audit_status": "No Data",
        }

    qualities = [decision.get("quality_score", 0) for decision in decisions]
    average_quality = round(sum(qualities) / len(qualities), 2)

    if average_quality >= 80:
        status = "Institutional Grade"
    elif average_quality >= 65:
        status = "Good"
    elif average_quality >= 50:
        status = "Needs Improvement"
    else:
        status = "Weak"

    return {
        "decisions": len(decisions),
        "average_quality": average_quality,
        "audit_status": status,
    }
