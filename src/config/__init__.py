"""Configuration package."""

CORE_INDEX_SYMBOLS = ["SPY", "QQQ", "IWM", "DIA"]
RATES_BONDS_SYMBOLS = ["TLT", "IEF", "SHY"]
DOLLAR_PROXY_SYMBOLS = ["UUP"]
SECTOR_SYMBOLS = ["XLK", "XLF", "XLE", "XLV", "XLY", "XLP", "XLI", "XLU", "XLB", "XLRE"]
MEGA_CAP_SYMBOLS = ["AAPL", "MSFT", "NVDA", "AMZN", "GOOGL", "META", "TSLA"]
SEMICONDUCTOR_SYMBOLS = ["SMH", "MU", "AMD", "AVGO"]
COMMODITY_SYMBOLS = ["GLD", "SLV", "USO"]
LEGACY_QUALITY_SYMBOLS = ["CSCO"]

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

SYMBOLS = [symbol for group_symbols in SYMBOL_UNIVERSE_GROUPS.values() for symbol in group_symbols]

BENCHMARK_MAP = {
    "SPY": "SPY",
    "QQQ": "QQQ",
    "IWM": "SPY",
    "DIA": "SPY",
    "TLT": "IEF",
    "IEF": "IEF",
    "SHY": "IEF",
    "UUP": "UUP",
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
    "AAPL": "QQQ",
    "MSFT": "QQQ",
    "NVDA": "QQQ",
    "AMZN": "QQQ",
    "GOOGL": "QQQ",
    "META": "QQQ",
    "TSLA": "QQQ",
    "SMH": "SMH",
    "MU": "SMH",
    "AMD": "SMH",
    "AVGO": "SMH",
    "GLD": "GLD",
    "SLV": "GLD",
    "USO": "USO",
    "CSCO": "QQQ",
}

SYMBOL_GROUP_MAP = {
    symbol: group_name
    for group_name, group_symbols in SYMBOL_UNIVERSE_GROUPS.items()
    for symbol in group_symbols
}
