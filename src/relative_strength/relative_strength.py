from __future__ import annotations


def calculate_relative_strength(asset_return: float, benchmark_return: float) -> float:
    if benchmark_return == 0:
        return 1.0

    return round(asset_return / benchmark_return, 2)


def classify_relative_strength(rs_value: float) -> str:
    if rs_value >= 1.2:
        return "Leader"
    if rs_value >= 0.8:
        return "Neutral"
    return "Weak"
