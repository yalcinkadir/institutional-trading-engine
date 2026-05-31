"""Single source of truth for runtime governance thresholds.

SR6 centralizes kill-switch and risk-limit thresholds so governance tuning
cannot drift across runtime modules, tests or documentation.

These values are conservative public/demo defaults. They do not authorize live
trading and should not be interpreted as proprietary production risk limits.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class GovernanceThresholds:
    """Runtime governance thresholds used by kill-switch and risk-limit checks."""

    vix_kill_level: float = 40.0
    portfolio_drawdown_kill_percent: float = 20.0
    severe_anomaly_kill_count: int = 5
    max_drawdown_percent: float = 15.0
    max_daily_loss_percent: float = 5.0

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


DEFAULT_GOVERNANCE_THRESHOLDS = GovernanceThresholds()