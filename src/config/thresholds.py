"""Versioned public-demo decision thresholds.

IP3 rule: values in this public repository are demo defaults only. They are
part of the public framework contract, not proprietary production edge.
Changing one of these values changes the public demo strategy definition and
must invalidate prior public-demo backtest, walk-forward and lockbox evidence.

Real/private thresholds must be supplied outside the public repository through
the optional external edge provider boundary.
"""

from __future__ import annotations

from dataclasses import dataclass


THRESHOLDS_VERSION = "public-demo-2026.05.29-v1"
PUBLIC_DEMO_DEFAULTS = True


@dataclass(frozen=True)
class DecisionThresholds:
    """Public-demo cutoffs for decision quality and sizing."""

    # Public-demo risk tier cutoffs. Not production edge.
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

    # Public-demo hard reject floors. Not production edge.
    min_asymmetry: float = 0.40
    min_data_confidence: float = 0.50

    # Public-demo position sizing by risk tier. Not production edge.
    tier1_size: float = 1.0
    tier2_size: float = 0.5
    tier3_size: float = 0.25
    no_trade_size: float = 0.0

    version: str = THRESHOLDS_VERSION
    public_demo_defaults: bool = PUBLIC_DEMO_DEFAULTS


DEFAULT_THRESHOLDS = DecisionThresholds()
