from __future__ import annotations

import warnings

DEPRECATED_ASSET_SCORE_PATH = True
CANONICAL_REPORT_SCORE_PATH = "src.reporting.decision_report"


def calculate_asset_score(
    trend_score: int,
    relative_strength_score: int,
    volume_score: int,
    volatility_score: int,
    risk_score: int,
) -> dict:
    """Deprecated research-only asset score helper.

    The active decision-report score path is `src.reporting.decision_report`,
    which exports explicit `score_provenance` and disables placeholder/symbol-name
    score contribution.
    """

    warnings.warn(
        "src.scoring.asset_score.calculate_asset_score is deprecated; "
        f"use {CANONICAL_REPORT_SCORE_PATH}",
        DeprecationWarning,
        stacklevel=2,
    )

    total = (
        trend_score
        + relative_strength_score
        + volume_score
        + volatility_score
        + risk_score
    )

    total = max(0, min(total, 100))

    if total >= 85:
        status = "Strong Ready"
    elif total >= 75:
        status = "Ready"
    elif total >= 60:
        status = "Watch"
    elif total >= 45:
        status = "Neutral"
    else:
        status = "Weak"

    return {
        "score": total,
        "status": status,
        "deprecated": True,
        "canonical_path": CANONICAL_REPORT_SCORE_PATH,
        "usage": "research_only_legacy_compatibility",
    }
