CORE_SYMBOLS = [
    "QQQ",
    "SPY",
]

GROWTH_SYMBOLS = [
    "AAPL",
    "MSFT",
    "NVDA",
    "META",
    "AMZN",
    "GOOGL",
    "AVGO",
    "AMD",
    "MU",
    "ADBE",
    "CRM",
]

QUALITY_SYMBOLS = [
    "CSCO",
]

METALS_SYMBOLS = [
    "GLD",
    "SLV",
]

SYMBOLS = (
    CORE_SYMBOLS
    + GROWTH_SYMBOLS
    + QUALITY_SYMBOLS
    + METALS_SYMBOLS
)

BENCHMARK_MAP = {
    "QQQ": "QQQ",
    "SPY": "SPY",

    "AAPL": "QQQ",
    "MSFT": "QQQ",
    "NVDA": "QQQ",
    "META": "QQQ",
    "AMZN": "QQQ",
    "GOOGL": "QQQ",
    "AVGO": "QQQ",
    "AMD": "QQQ",
    "MU": "QQQ",
    "ADBE": "QQQ",
    "CRM": "QQQ",
    "CSCO": "QQQ",

    "GLD": "GLD",
    "SLV": "GLD",
}

SYMBOL_GROUP_MAP = {
    "QQQ": "core",
    "SPY": "core",

    "AAPL": "growth",
    "MSFT": "growth",
    "NVDA": "growth",
    "META": "growth",
    "AMZN": "growth",
    "GOOGL": "growth",
    "AVGO": "growth",
    "AMD": "growth",
    "MU": "growth",
    "ADBE": "growth",
    "CRM": "growth",

    "CSCO": "quality",

    "GLD": "metals",
    "SLV": "metals",
}
