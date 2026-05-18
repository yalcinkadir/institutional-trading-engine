from __future__ import annotations


def enforce_exposure_policy(
    sector_exposure_percent: float,
    max_sector_exposure_percent: float,
    single_position_percent: float,
    max_single_position_percent: float,
) -> dict:
    warnings: list[str] = []

    if sector_exposure_percent > max_sector_exposure_percent:
        warnings.append("sector_exposure_exceeded")

    if single_position_percent > max_single_position_percent:
        warnings.append("single_position_exceeded")

    status = "APPROVED" if not warnings else "REVIEW_REQUIRED"

    return {
        "status": status,
        "warnings": warnings,
    }
