from __future__ import annotations


def compare_shadow_models(primary: dict, shadow: dict) -> dict:
    primary_score = float(primary.get("score", 0))
    shadow_score = float(shadow.get("score", 0))

    delta = round(primary_score - shadow_score, 2)

    if abs(delta) <= 5:
        classification = "Aligned"
    elif abs(delta) <= 15:
        classification = "Moderate Divergence"
    else:
        classification = "High Divergence"

    return {
        "primary_score": primary_score,
        "shadow_score": shadow_score,
        "delta": delta,
        "classification": classification,
    }
