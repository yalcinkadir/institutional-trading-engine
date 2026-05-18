from __future__ import annotations


def evaluate_walk_forward(
    training_scores: list[float],
    validation_scores: list[float],
) -> dict:
    training_avg = round(sum(training_scores) / max(len(training_scores), 1), 2)
    validation_avg = round(sum(validation_scores) / max(len(validation_scores), 1), 2)

    degradation = round(training_avg - validation_avg, 2)

    if degradation <= 5:
        classification = "Robust"
    elif degradation <= 15:
        classification = "Moderate Overfit Risk"
    else:
        classification = "High Overfit Risk"

    return {
        "training_average": training_avg,
        "validation_average": validation_avg,
        "degradation": degradation,
        "classification": classification,
    }
