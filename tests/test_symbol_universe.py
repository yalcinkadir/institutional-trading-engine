from __future__ import annotations

from src.config import BENCHMARK_MAP, SYMBOL_GROUP_MAP, SYMBOL_UNIVERSE_GROUPS, SYMBOLS


EXPECTED_SYMBOLS = {
    "SPY", "QQQ", "IWM", "DIA",
    "TLT", "IEF", "SHY",
    "UUP",
    "XLK", "XLF", "XLE", "XLV", "XLY", "XLP", "XLI", "XLU", "XLB", "XLRE",
    "AAPL", "MSFT", "NVDA", "AMZN", "GOOGL", "META", "TSLA",
    "SMH", "MU", "AMD", "AVGO",
    "GLD", "SLV", "USO",
}

EXPECTED_GROUPS = {
    "core_indices",
    "rates_bonds",
    "dollar_proxy",
    "sectors",
    "mega_caps",
    "semiconductors",
    "commodities",
}

REQUIRED_SECTOR_ETFS = {
    "XLK", "XLF", "XLE", "XLV", "XLY", "XLP", "XLI", "XLU", "XLB", "XLRE",
}


def test_symbol_universe_contains_required_groups() -> None:
    assert EXPECTED_GROUPS.issubset(SYMBOL_UNIVERSE_GROUPS.keys())


def test_symbol_universe_contains_minimum_required_symbols() -> None:
    assert EXPECTED_SYMBOLS.issubset(set(SYMBOLS))


def test_symbol_universe_has_no_duplicates() -> None:
    assert len(SYMBOLS) == len(set(SYMBOLS))


def test_every_symbol_has_group_metadata() -> None:
    assert set(SYMBOLS) == set(SYMBOL_GROUP_MAP.keys())


def test_every_symbol_has_benchmark_mapping() -> None:
    assert set(SYMBOLS).issubset(BENCHMARK_MAP.keys())


def test_every_benchmark_is_in_universe() -> None:
    assert set(BENCHMARK_MAP.values()).issubset(set(SYMBOLS))


def test_sector_universe_is_broad_not_tech_only() -> None:
    sectors = set(SYMBOL_UNIVERSE_GROUPS["sectors"])
    assert REQUIRED_SECTOR_ETFS.issubset(sectors)


def test_cross_asset_symbols_are_present() -> None:
    assert {"TLT", "IEF", "SHY"}.issubset(set(SYMBOLS))
    assert {"GLD", "SLV", "USO"}.issubset(set(SYMBOLS))


def test_dollar_proxy_is_available_without_native_dxy_requirement() -> None:
    assert SYMBOL_UNIVERSE_GROUPS["dollar_proxy"] == ["UUP"]
    assert SYMBOL_GROUP_MAP["UUP"] == "dollar_proxy"
    assert BENCHMARK_MAP["UUP"] == "UUP"


def test_key_risk_regime_groups_are_not_empty() -> None:
    for group in ["core_indices", "rates_bonds", "dollar_proxy", "sectors", "commodities"]:
        assert SYMBOL_UNIVERSE_GROUPS[group]
