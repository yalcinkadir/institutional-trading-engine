from __future__ import annotations

import pytest

from src.scoring.asset_score import calculate_asset_score
from src.scoring.confidence_score import calculate_confidence_score


def test_196_legacy_confidence_score_is_deprecated_and_not_canonical() -> None:
    with pytest.warns(DeprecationWarning):
        result = calculate_confidence_score(
            setup_score=80,
            market_health_score=70,
            vix=14,
            breadth_percent=72,
        )

    assert result["deprecated"] is True
    assert result["usage"] == "research_only_legacy_compatibility"
    assert result["canonical_path"] == "src.decision_confidence.calculate_confidence_score"


def test_196_legacy_asset_score_is_deprecated_and_not_canonical() -> None:
    with pytest.warns(DeprecationWarning):
        result = calculate_asset_score(
            trend_score=20,
            relative_strength_score=20,
            volume_score=20,
            volatility_score=20,
            risk_score=10,
        )

    assert result["deprecated"] is True
    assert result["usage"] == "research_only_legacy_compatibility"
    assert result["canonical_path"] == "src.reporting.decision_report"
