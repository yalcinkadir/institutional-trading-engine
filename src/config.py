"""Scanner universe configuration.

The default universe intentionally covers more than US mega-cap technology so
market-regime analysis can observe cross-asset, dollar, rates, sector and
commodity behavior without using broker APIs.
"""

CORE_INDEX_SYMBOLS = [
    "SPY",
    "QQQ",
    "IWM",
    "DIA",
]

RATES_BONDS_SYMBOLS = [
    "TLT",
    "IEF",
    "SHY",
]

DOLLAR_PROXY_SYMBOLS = [
    "UUP",
]

SECTOR_SYMBOLS = [
    "XLK",
    "XLF",
    "XLE",
    "XLV",
    "XLY",
    "XLP",
    "XLI",
    "XLU",
    "XLB",
    "XLRE",
]

MEGA_CAP_SYMBOLS = [
    "AAPL",
    "MSFT",
    "NVDA",
    "AMZN",
    "GOOGL",
    "META",
    "TSLA",
]

SEMICONDUCTOR_SYMBOLS = [
    "SMH",
    "MU",
    "AMD",
    "AVGO",
]

COMMODITY_SYMBOLS = [
    "GLD",
    "SLV",
    "USO",
]

LEGACY_QUALITY_SYMBOLS = [
    "CSCO",
]

SYMBOL_UNIVERSE_GROUPS = {
    "core_indices": CORE_INDEX_SYMBOLS,
    "rates_bonds": RATES_BONDS_SYMBOLS,
    "dollar_proxy": DOLLAR_PROXY_SYMBOLS,
    "sectors": SECTOR_SYMBOLS,
    "mega_caps": MEGA_CAP_SYMBOLS,
    "semiconductors": SEMICONDUCTOR_SYMBOLS,
    "commodities": COMMODITY_SYMBOLS,
    "legacy_quality": LEGACY_QUALITY_SYMBOLS,
}

SYMBOLS = [
    symbol
    for group_symbols in SYMBOL_UNIVERSE_GROUPS.values()
    for symbol in group_symbols
]

BENCHMARK_MAP = {
    # Core index benchmarks
    "SPY": "SPY",
    "QQQ": "QQQ",
    "IWM": "SPY",
    "DIA": "SPY",

    # Rates / bonds benchmark against intermediate duration Treasuries
    "TLT": "IEF",
    "IEF": "IEF",
    "SHY": "IEF",

    # Dollar proxy benchmarked against itself because DXY is not a Polygon ETF symbol
    "UUP": "UUP",

    # Sectors benchmark against broad market
    "XLK": "SPY",
    "XLF": "SPY",
    "XLE": "SPY",
    "XLV": "SPY",
    "XLY": "SPY",
    "XLP": "SPY",
    "XLI": "SPY",
    "XLU": "SPY",
    "XLB": "SPY",
    "XLRE": "SPY",

    # Mega caps benchmark against Nasdaq 100
    "AAPL": "QQQ",
    "MSFT": "QQQ",
    "NVDA": "QQQ",
    "AMZN": "QQQ",
    "GOOGL": "QQQ",
    "META": "QQQ",
    "TSLA": "QQQ",

    # Semiconductors benchmark against SMH
    "SMH": "SMH",
    "MU": "SMH",
    "AMD": "SMH",
    "AVGO": "SMH",

    # Commodities benchmark against GLD unless oil-specific
    "GLD": "GLD",
    "SLV": "GLD",
    "USO": "USO",

    # Legacy quality / network infrastructure
    "CSCO": "QQQ",
}

SYMBOL_GROUP_MAP = {
    symbol: group_name
    for group_name, group_symbols in SYMBOL_UNIVERSE_GROUPS.items()
    for symbol in group_symbols
}
