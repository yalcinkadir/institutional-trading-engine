"""Versioned decision thresholds.

Decision cutoffs are part of the evidence contract. Changing one of these
values changes the strategy definition and must invalidate prior backtest,
walk-forward and lockbox evidence.
"""

from __future__ import annotations

from dataclasses import dataclass


THRESHOLDS_VERSION = "2026.05.25-v1"


@dataclass(frozen=True)
class DecisionThresholds:
    """Centralized cutoffs for decision quality and sizing."""

    # Risk tier cutoffs
    tier1_setup_score: float = 80.0
    tier1_regime_alignment: float = 0.75
    tier1_asymmetry: float = 0.70
    tier1_data_confidence: float = 0.80

    tier2_setup_score: float = 65.0
    tier2_regime_alignment: float = 0.55
    tier2_asymmetry: float = 0.55
    tier2_data_confidence: float = 0.65

    tier3_setup_score: float = 50.0
    tier3_regime_alignment: float = 0.40
    tier3_asymmetry: float = 0.40
    tier3_data_confidence: float = 0.50

    # Hard reject floors
    min_asymmetry: float = 0.40
    min_data_confidence: float = 0.50

    # Position sizing by risk tier
    tier1_size: float = 1.0
    tier2_size: float = 0.5
    tier3_size: float = 0.25
    no_trade_size: float = 0.0

    version: str = THRESHOLDS_VERSION


DEFAULT_THRESHOLDS = DecisionThresholds()
