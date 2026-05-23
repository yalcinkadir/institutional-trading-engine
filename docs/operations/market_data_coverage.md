# Market Data Coverage Expansion

P32 expands the default market-data universe for broader Decision-Support context.

The goal is to reduce Nasdaq/mega-cap technology bias and improve risk-regime interpretation without adding broker API integration.

## Scope

- No broker API integration
- No order execution
- No trading authorization
- Polygon market-data symbols only
- Broader cross-asset and sector context

## Universe Groups

Implemented in:

```text
src/config.py
```

### Core Index ETFs

```text
SPY, QQQ, IWM, DIA
```

Purpose:

```text
Broad market, Nasdaq, small caps, Dow proxy
```

### Rates / Bonds

```text
TLT, IEF, SHY
```

Purpose:

```text
Long-duration, intermediate-duration and short-duration Treasury context
```

### Dollar Proxy

```text
UUP
```

Purpose:

```text
ETF-based US dollar proxy when native DXY is not part of the standard equity/ETF universe
```

### Sector ETFs

```text
XLK, XLF, XLE, XLV, XLY, XLP, XLI, XLU, XLB, XLRE
```

Purpose:

```text
Technology, financials, energy, healthcare, discretionary, staples, industrials, utilities, materials and real estate context
```

### Mega Caps

```text
AAPL, MSFT, NVDA, AMZN, GOOGL, META, TSLA
```

Purpose:

```text
Large-cap leadership and Nasdaq-heavy market leadership context
```

### Semiconductors

```text
SMH, MU, AMD, AVGO
```

Purpose:

```text
Semiconductor leadership and relative strength context
```

### Commodities

```text
GLD, SLV, USO
```

Purpose:

```text
Gold, silver and oil proxy context
```

## Benchmark Mapping

Every symbol must have a benchmark in `BENCHMARK_MAP`.

Examples:

```text
TLT → IEF
UUP → UUP
XLF → SPY
AAPL → QQQ
AMD → SMH
SLV → GLD
USO → USO
```

## Validation

Tests:

```bash
pytest tests/test_symbol_universe.py
```

The tests verify:

- required universe groups exist
- required symbols are present
- no duplicate symbols exist
- every symbol has group metadata
- every symbol has a benchmark mapping
- every benchmark exists in the universe
- sector coverage is broad and not tech-only
- UUP is available as dollar proxy

## Operational Impact

P32 improves:

- market breadth analysis
- risk-on / risk-off interpretation
- sector rotation context
- bond/rates context
- dollar context
- commodity proxy context

## Non-Goals

- Broker integration
- Real order routing
- Account synchronization
- Live execution
- Trading approval
