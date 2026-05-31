"""Runtime approval gate for governance-sensitive decision paths.

This module provides a small public/runtime boundary that converts portfolio
state plus kill-switch evaluation into an explicit approval/block decision.
It exists so runtime callers do not need to remember every fail-closed rule
manually.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta
from typing import Any

from src.governance.kill_switch import evaluate_kill_switch_for_portfolio_state
from src.runtime.portfolio_state import PortfolioState


INVALID_GOVERNANCE_APPROVAL_REASON = "portfolio_governance_invalid"
KILL_SWITCH_APPROVAL_REASON = "kill_switch_active"
STALE_PORTFOLIO_STATE_REASON = "stale_portfolio_state"
DEFAULT_PORTFOLIO_STATE_MAX_AGE = timedelta(days=1)


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
    now: datetime | None = None,
    portfolio_state_max_age: timedelta = DEFAULT_PORTFOLIO_STATE_MAX_AGE,
) -> RuntimeGovernanceApproval:
    """Return whether runtime decision approval is allowed.

    Approval is deliberately stricter than raw kill-switch evaluation:

    - invalid portfolio governance always blocks approval
    - stale portfolio state always blocks approval
    - any active kill switch always blocks approval
    - approval is allowed only when all checks pass
    """

    kill_switch = evaluate_kill_switch_for_portfolio_state(
        portfolio_state=portfolio_state,
        vix=vix,
        severe_anomaly_count=severe_anomaly_count,
    )

    reasons: list[str] = []
    if not portfolio_state.governance_valid:
        reasons.append(INVALID_GOVERNANCE_APPROVAL_REASON)

    if is_portfolio_state_stale(
        portfolio_state=portfolio_state,
        now=now,
        max_age=portfolio_state_max_age,
    ):
        reasons.append(STALE_PORTFOLIO_STATE_REASON)

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


def is_portfolio_state_stale(
    *,
    portfolio_state: PortfolioState,
    now: datetime | None = None,
    max_age: timedelta = DEFAULT_PORTFOLIO_STATE_MAX_AGE,
) -> bool:
    """Return True when portfolio state is too old or has an invalid timestamp."""

    reference_time = now or datetime.now(UTC)
    if reference_time.tzinfo is None:
        reference_time = reference_time.replace(tzinfo=UTC)

    try:
        updated_at = datetime.fromisoformat(portfolio_state.updated_at)
    except ValueError:
        return True

    if updated_at.tzinfo is None:
        updated_at = updated_at.replace(tzinfo=UTC)

    if updated_at > reference_time:
        return True

    return reference_time - updated_at > max_age
