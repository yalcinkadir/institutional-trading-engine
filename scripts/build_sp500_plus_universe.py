"""Build a 500+ active starter universe from S&P 500 constituents plus ETFs.

This creates a broad active universe for current scans and forward paper
observation. It is intentionally marked as ACTIVE_STARTER because it is not a
survivorship-safe historical dataset. For 10+ year backtests, replace or enrich
this file with point-in-time constituent history and delisted tickers from a
vetted source such as Norgate, CRSP or Sharadar.

Usage:
    python scripts/build_sp500_plus_universe.py \
        --output data/universe/survivorship_universe.csv

The script downloads the S&P 500 component table from Wikipedia via pandas and
adds a curated ETF set covering broad market, sectors, industries, factors,
size buckets, bonds, commodities and volatility proxies.
"""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

import pandas as pd

SP500_URL = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
DEFAULT_OUTPUT = Path("data/universe/survivorship_universe.csv")
DEFAULT_MANIFEST = Path("data/universe/universe_source_manifest.md")
DEFAULT_ACTIVE_FROM = "2026-05-24"

# Kept explicit and deterministic so review can see what gets added.
ETF_SYMBOLS: tuple[str, ...] = (
    # Broad US equity
    "SPY", "IVV", "VOO", "SPLG", "RSP", "VTI", "ITOT", "SCHB", "IWB", "IWM",
    "IJH", "IJR", "MDY", "QQQ", "QQQM", "DIA", "IWC", "VB", "VO", "VV",
    # SPDR sectors
    "XLB", "XLC", "XLE", "XLF", "XLI", "XLK", "XLP", "XLRE", "XLU", "XLV", "XLY",
    # Vanguard sectors
    "VAW", "VOX", "VCR", "VDC", "VDE", "VFH", "VHT", "VIS", "VGT", "VNQ", "VPU",
    # iShares sectors / industries
    "IYW", "IYF", "IYH", "IYC", "IYK", "IYE", "IYM", "IYR", "IYT", "IDU",
    "SMH", "SOXX", "XSD", "PSI", "IGV", "SKYY", "CIBR", "HACK", "FDN", "ARKK",
    "ARKW", "ARKG", "BOTZ", "ROBO", "FINX", "KWEB", "CLOU", "WCLD", "FIVG", "SNSR",
    "XHB", "ITB", "XRT", "KRE", "KBE", "KIE", "IAI", "IHI", "XBI", "IBB",
    "PJP", "IHF", "XOP", "OIH", "AMLP", "TAN", "ICLN", "PBW", "URA", "COPX",
    "GDX", "GDXJ", "SIL", "SLX", "XME", "MOO", "WOOD", "JETS", "ITA", "PPA",
    # Factors and style
    "MTUM", "QUAL", "VLUE", "USMV", "SIZE", "SPLV", "SPHQ", "VUG", "VTV", "IWF",
    "IWD", "IVE", "IVW", "IWO", "IWN", "VBK", "VBR", "VOT", "VOE", "SCHG", "SCHV",
    # Dividend / income equity
    "VIG", "VYM", "SCHD", "DGRO", "NOBL", "SDY", "HDV", "DVY", "SPYD", "JEPI",
    "JEPQ", "DIVO", "QYLD", "XYLD", "RYLD",
    # International equity
    "VEA", "IEFA", "EFA", "EEM", "VWO", "IEMG", "VXUS", "ACWI", "URTH", "EWJ",
    "EWU", "EWG", "EWQ", "EWI", "EWP", "EWA", "EWC", "EWH", "EWT", "EWY",
    "INDA", "MCHI", "FXI", "ASHR", "EWZ", "EWW", "EZA", "TUR", "VGK", "FEZ",
    # Bonds / credit / rates
    "AGG", "BND", "TLT", "IEF", "IEI", "SHY", "BIL", "SGOV", "MUB", "LQD",
    "HYG", "JNK", "EMB", "BNDX", "TIP", "VTIP", "MBB", "VCIT", "VCSH", "VCLT",
    # Commodities / macro proxies
    "GLD", "IAU", "SLV", "USO", "UNG", "DBA", "DBC", "PDBC", "CPER", "WEAT",
    "CORN", "SOYB", "UUP", "FXE", "FXY", "FXB", "CYB",
    # Volatility / inverse / leveraged proxies for regime research only
    "VXX", "UVXY", "SVXY", "SH", "SDS", "PSQ", "QID", "SQQQ", "TQQQ", "UPRO", "SPXU",
)


@dataclass(frozen=True)
class UniverseRow:
    symbol: str
    active_from: str
    active_to: str = ""
    delisting_reason: str = ""
    successor_symbol: str = ""
    final_close_price: str = ""
    notes: str = ""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build S&P 500 + ETF active universe")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--active-from", default=DEFAULT_ACTIVE_FROM)
    return parser.parse_args()


def normalize_symbol(symbol: str) -> str:
    # Polygon-style common stock symbols often use '-' for share classes, while
    # Yahoo/Wikipedia often use '.'. The engine stores canonical plain tickers;
    # data adapters can translate per vendor.
    return symbol.strip().upper().replace(".", ".")


def load_sp500_rows(active_from: str) -> list[UniverseRow]:
    tables = pd.read_html(SP500_URL)
    constituents = tables[0]
    if "Symbol" not in constituents.columns:
        raise RuntimeError("Could not find Symbol column in S&P 500 table")

    rows: list[UniverseRow] = []
    for _, record in constituents.iterrows():
        symbol = normalize_symbol(str(record["Symbol"]))
        date_added = str(record.get("Date added", "")).strip()
        # We keep the real S&P add date when available, but this is still not a
        # full historical lifecycle dataset because removed constituents are not
        # represented. The notes field makes that explicit.
        rows.append(
            UniverseRow(
                symbol=symbol,
                active_from=date_added if date_added and date_added != "nan" else active_from,
                notes="source=wikipedia_sp500_current;classification=active_starter_not_survivorship_safe",
            )
        )
    return rows


def build_universe(active_from: str) -> list[UniverseRow]:
    by_symbol: dict[str, UniverseRow] = {}
    for row in load_sp500_rows(active_from):
        by_symbol[row.symbol] = row
    for symbol in ETF_SYMBOLS:
        by_symbol.setdefault(
            normalize_symbol(symbol),
            UniverseRow(
                symbol=normalize_symbol(symbol),
                active_from=active_from,
                notes="source=curated_etf_overlay;classification=active_starter_etf",
            ),
        )
    return [by_symbol[symbol] for symbol in sorted(by_symbol)]


def write_csv(rows: list[UniverseRow], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "symbol",
                "active_from",
                "active_to",
                "delisting_reason",
                "successor_symbol",
                "final_close_price",
                "notes",
            ],
        )
        writer.writeheader()
        for row in rows:
            writer.writerow(row.__dict__)


def write_manifest(rows: list[UniverseRow], manifest: Path, output: Path) -> None:
    manifest.parent.mkdir(parents=True, exist_ok=True)
    sp500_count = sum("wikipedia_sp500_current" in row.notes for row in rows)
    etf_count = sum("curated_etf_overlay" in row.notes for row in rows)
    manifest.write_text(
        "# Universe Source Manifest\n\n"
        f"Generated at: {datetime.now(UTC).isoformat().replace('+00:00', 'Z')}\n\n"
        f"Output: `{output}`\n\n"
        f"Total symbols: **{len(rows)}**\n\n"
        f"S&P 500 current constituents: **{sp500_count}**\n\n"
        f"Curated ETF overlay: **{etf_count}**\n\n"
        "## Important limitation\n\n"
        "This is an active starter universe. It is useful for current scans and forward paper observation. "
        "It is not sufficient for long historical backtests because it does not include all removed or delisted historical constituents.\n\n"
        "For serious 10+ year backtesting, enrich this dataset with point-in-time membership and delisted ticker lifecycles from a vetted provider.\n",
        encoding="utf-8",
    )


def main() -> int:
    args = parse_args()
    rows = build_universe(args.active_from)
    write_csv(rows, args.output)
    write_manifest(rows, args.manifest, args.output)
    print(f"Wrote {len(rows)} symbols to {args.output}")
    if len(rows) < 500:
        raise SystemExit("Universe has fewer than 500 symbols")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
