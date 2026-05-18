from __future__ import annotations


def evaluate_compliance(
    leverage: float,
    max_leverage: float,
    restricted_assets: list[str],
    portfolio_assets: list[str],
) -> dict:
    violations: list[str] = []

    if leverage > max_leverage:
        violations.append("leverage_limit_exceeded")

    restricted_matches = [
        asset for asset in portfolio_assets if asset in restricted_assets
    ]

    if restricted_matches:
        violations.append("restricted_assets_detected")

    status = "COMPLIANT" if not violations else "NON_COMPLIANT"

    return {
        "status": status,
        "violations": violations,
        "restricted_matches": restricted_matches,
    }
