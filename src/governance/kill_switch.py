"""
Kill Switch — Governance Layer.

Evaluates whether the runtime should be halted entirely.

Thresholds are intentionally imported from
`src.governance.governance_thresholds` so the kill-switch logic has a single
source of truth instead of local magic numbers.

VIX-None safety: if VIX is unavailable (e.g. Free Polygon tier), the kill switch
does NOT activate on volatility alone. Unavailable VIX is logged as a warning,
not treated as extreme.
"""

from __future__ import annotations

from src.governance.governance_thresholds import (
    DEFAULT_GOVERNANCE_THRESHOLDS,
    GovernanceThresholds,
)
from src.runtime.portfolio_state import PortfolioState


INVALID_PORTFOLIO_GOVERNANCE_REASON = "invalid_portfolio_governance_state"


def evaluate_kill_switch(
    vix: float | None,
    drawdown_percent: float,
    severe_anomaly_count: int,
    thresholds: GovernanceThresholds = DEFAULT_GOVERNANCE_THRESHOLDS,
) -> dict:
    """
    Evaluate whether the runtime kill switch should activate.

    Args:
        vix:                  Current VIX level. None = unavailable.
        drawdown_percent:     Current portfolio drawdown percent.
        severe_anomaly_count: Number of severe market anomalies detected.
        thresholds:           Shared governance threshold source.

    Returns:
        dict with keys:
          kill_switch (bool)   — True if runtime should halt.
          reasons (list[str])  — Why it was activated.
          vix_available (bool) — Whether VIX data was present.
    """
    activated = False
    reasons: list[str] = []
    vix_available = vix is not None

    if vix_available and vix >= thresholds.vix_kill_level:
        activated = True
        reasons.append("extreme_volatility")

    if drawdown_percent >= thresholds.portfolio_drawdown_kill_percent:
        activated = True
        reasons.append("portfolio_drawdown_limit")

    if severe_anomaly_count >= thresholds.severe_anomaly_kill_count:
        activated = True
        reasons.append("market_instability")

    return {
        "kill_switch": activated,
        "reasons": reasons,
        "vix_available": vix_available,
    }


def evaluate_kill_switch_for_portfolio_state(
    *,
    portfolio_state: PortfolioState,
    vix: float | None,
    severe_anomaly_count: int,
    thresholds: GovernanceThresholds = DEFAULT_GOVERNANCE_THRESHOLDS,
) -> dict:
    """Evaluate kill-switch state from a trusted portfolio-state object.

    This wrapper is the fail-closed governance boundary for runtime callers.
    The legacy numeric function intentionally remains available for pure unit
    checks, but runtime code should use this function so `governance_valid=False`
    cannot be accidentally converted into a harmless `0.0` drawdown input.
    """

    result = evaluate_kill_switch(
        vix=vix,
        drawdown_percent=portfolio_state.drawdown_percent,
        severe_anomaly_count=severe_anomaly_count,
        thresholds=thresholds,
    )

    if not portfolio_state.governance_valid:
        reasons = list(result["reasons"])
        if INVALID_PORTFOLIO_GOVERNANCE_REASON not in reasons:
            reasons.insert(0, INVALID_PORTFOLIO_GOVERNANCE_REASON)
        result = {
            **result,
            "kill_switch": True,
            "reasons": reasons,
        }

    return {
        **result,
        "portfolio_governance_valid": portfolio_state.governance_valid,
        "portfolio_state_source": portfolio_state.source,
        "portfolio_state_warnings": list(portfolio_state.warnings),
    }
