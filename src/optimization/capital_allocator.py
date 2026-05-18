from __future__ import annotations


def allocate_capital(
    total_capital: float,
    allocations: dict[str, float],
) -> dict:
    distributed = {
        asset: round(total_capital * weight, 2)
        for asset, weight in allocations.items()
    }

    return {
        "total_capital": total_capital,
        "allocations": distributed,
    }
