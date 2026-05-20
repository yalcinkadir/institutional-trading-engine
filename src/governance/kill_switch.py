"""
Kill Switch — Governance Layer.

Evaluates whether the runtime should be halted entirely.

Rules:
  - VIX >= 40          → extreme_volatility
  - drawdown >= 20%    → portfolio_drawdown_limit
  - anomaly_count >= 5 → market_instability

VIX-None safety: if VIX is unavailable (e.g. Free Polygon tier),
the kill switch does NOT activate on volatility alone.
Unavailable VIX is logged as a warning, not treated as extreme.
"""

from __future__ import annotations


def evaluate_kill_switch(
    vix: float | None,
    drawdown_percent: float,
    severe_anomaly_count: int,
) -> dict:
    """
    Evaluate whether the runtime kill switch should activate.

    Args:
        vix:                  Current VIX level. None = unavailable (Free tier).
        drawdown_percent:     Current portfolio drawdown percent.
        severe_anomaly_count: Number of severe market anomalies detected.

    Returns:
        dict with keys:
          kill_switch (bool)  — True if runtime should halt.
          reasons (list[str]) — Why it was activated.
          vix_available (bool)— Whether VIX data was present.
    """
    activated = False
    reasons: list[str] = []
    vix_available = vix is not None

    # VIX check — skip gracefully when unavailable (Free Polygon tier)
    if vix_available and vix >= 40:
        activated = True
        reasons.append("extreme_volatility")

    if drawdown_percent >= 20:
        activated = True
        reasons.append("portfolio_drawdown_limit")

    if severe_anomaly_count >= 5:
        activated = True
        reasons.append("market_instability")

    return {
        "kill_switch": activated,
        "reasons": reasons,
        "vix_available": vix_available,
    }
