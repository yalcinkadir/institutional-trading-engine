"""Runtime approval gate for governance-sensitive decision paths.

This module provides a small public/runtime boundary that converts portfolio
state plus kill-switch evaluation into an explicit approval/block decision.
It exists so runtime callers do not need to remember every fail-closed rule
manually.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from src.governance.kill_switch import evaluate_kill_switch_for_portfolio_state
from src.runtime.portfolio_state import PortfolioState


INVALID_GOVERNANCE_APPROVAL_REASON = "portfolio_governance_invalid"
KILL_SWITCH_APPROVAL_REASON = "kill_switch_active"


@dataclass(frozen=True)
class RuntimeGovernanceApproval:
    """Final governance approval result for runtime decision paths."""

    approved: bool
    reasons: list[str] = field(default_factory=list)
    kill_switch: dict[str, Any] = field(default_factory=dict)

    @property
    def blocked(self) -> bool:
        return not self.approved

    def to_dict(self) -> dict[str, Any]:
        return {
            "approved": self.approved,
            "blocked": self.blocked,
            "reasons": list(self.reasons),
            "kill_switch": dict(self.kill_switch),
        }


def evaluate_runtime_governance_approval(
    *,
    portfolio_state: PortfolioState,
    vix: float | None,
    severe_anomaly_count: int,
) -> RuntimeGovernanceApproval:
    """Return whether runtime decision approval is allowed.

    Approval is deliberately stricter than raw kill-switch evaluation:

    - invalid portfolio governance always blocks approval
    - any active kill switch always blocks approval
    - approval is allowed only when both checks pass
    """

    kill_switch = evaluate_kill_switch_for_portfolio_state(
        portfolio_state=portfolio_state,
        vix=vix,
        severe_anomaly_count=severe_anomaly_count,
    )

    reasons: list[str] = []
    if not portfolio_state.governance_valid:
        reasons.append(INVALID_GOVERNANCE_APPROVAL_REASON)

    if kill_switch["kill_switch"]:
        reasons.append(KILL_SWITCH_APPROVAL_REASON)
        for reason in kill_switch["reasons"]:
            if reason not in reasons:
                reasons.append(str(reason))

    return RuntimeGovernanceApproval(
        approved=not reasons,
        reasons=reasons,
        kill_switch=kill_switch,
    )
