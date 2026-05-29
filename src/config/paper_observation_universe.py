from __future__ import annotations

CORE_OBSERVATION_UNIVERSE: tuple[str, ...] = (
    "QQQ",
    "SPY",
    "AAPL",
    "MSFT",
    "NVDA",
    "META",
    "GOOGL",
    "AMZN",
    "MU",
    "AMD",
    "V",
    "INTC",
)

MACRO_CFD_OBSERVATION_UNIVERSE: tuple[str, ...] = (
    "NDQ100",
    "XAG",
)

EXCLUDED_OBSERVATION_GROUPS: tuple[str, ...] = (
    "small_illiquid_equities",
    "new_asset_classes",
    "options_data",
    "crypto",
    "new_strategies",
)

OBSERVATION_UNIVERSE_VERSION = "2026.05.29-b1.1-core-v1"


def format_observation_universe() -> str:
    return "\n".join(
        [
            f"Core: {', '.join(CORE_OBSERVATION_UNIVERSE)}",
            f"Macro/CFD watch: {', '.join(MACRO_CFD_OBSERVATION_UNIVERSE)}",
            f"Excluded for B1.1: {', '.join(EXCLUDED_OBSERVATION_GROUPS)}",
            f"Universe version: {OBSERVATION_UNIVERSE_VERSION}",
        ]
    )
