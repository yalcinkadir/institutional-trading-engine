from __future__ import annotations

import random


def run_monte_carlo_simulation(
    initial_value: float,
    expected_return_percent: float,
    volatility_percent: float,
    periods: int = 20,
    simulations: int = 1000,
    seed: int | None = 42,
) -> dict:
    if seed is not None:
        random.seed(seed)

    final_values: list[float] = []

    for _ in range(simulations):
        value = initial_value
        for _ in range(periods):
            simulated_return = random.gauss(
                expected_return_percent / 100,
                volatility_percent / 100,
            )
            value *= 1 + simulated_return
        final_values.append(round(value, 2))

    sorted_values = sorted(final_values)
    p5 = sorted_values[int(simulations * 0.05)]
    p50 = sorted_values[int(simulations * 0.50)]
    p95 = sorted_values[int(simulations * 0.95) - 1]

    return {
        "simulations": simulations,
        "periods": periods,
        "p5": p5,
        "p50": p50,
        "p95": p95,
        "average_final_value": round(sum(final_values) / len(final_values), 2),
    }
