from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.sector_rotation import (  # noqa: E402
    SectorPerformance,
    evaluate_sector_rotation,
)


def test_risk_on_offensive_leadership_detected_when_growth_sectors_dominate():
    sectors = [
        SectorPerformance("XLK", 0.12, 0.88, True, True),
        SectorPerformance("SMH", 0.18, 0.92, True, True),
        SectorPerformance("QQQ", 0.11, 0.84, True, True),
        SectorPerformance("XLY", 0.07, 0.74, True, True),
        SectorPerformance("IWM", 0.05, 0.71, True, True),
        SectorPerformance("XLI", 0.03, 0.66, True, True),
    ]

    result = evaluate_sector_rotation(sectors)

    assert result.rotation_state == "risk_on_offensive_leadership"
    assert result.participation_quality == "broad_participation"
    assert "technology_and_ai_leadership_confirmed" in result.confirmations


def test_defensive_rotation_detected_when_offensive_sectors_break_down():
    sectors = [
        SectorPerformance("XLU", 0.09, 0.78, True, True),
        SectorPerformance("XLP", 0.07, 0.74, True, True),
        SectorPerformance("XLV", 0.06, 0.71, True, True),
        SectorPerformance("SMH", -0.12, 0.34, False, False),
        SectorPerformance("XLK", -0.08, 0.39, False, False),
        SectorPerformance("QQQ", -0.06, 0.41, False, False),
    ]

    result = evaluate_sector_rotation(sectors)

    assert result.rotation_state == "defensive_rotation"
    assert "capital_rotating_to_defense" in result.warnings
    assert "semiconductor_leadership_breakdown" in result.warnings
