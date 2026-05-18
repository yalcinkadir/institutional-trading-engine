from __future__ import annotations


def combine_distributed_analysis(results: list[dict]) -> dict:
    combined_score = 0.0

    for result in results:
        combined_score += float(result.get("score", 0))

    average_score = 0
    if results:
        average_score = round(combined_score / len(results), 2)

    if average_score >= 80:
        classification = "Strong Opportunity"
    elif average_score >= 60:
        classification = "Constructive"
    elif average_score >= 40:
        classification = "Mixed"
    else:
        classification = "Weak"

    return {
        "average_score": average_score,
        "classification": classification,
        "sources": len(results),
    }
