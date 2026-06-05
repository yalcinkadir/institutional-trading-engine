#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict, dataclass, field
from datetime import date
from pathlib import Path
from typing import Any

REQUIRED_COLUMNS = {
    "symbol",
    "effective_from",
    "effective_to",
    "active",
    "asset_class",
    "exchange",
    "source",
    "status",
    "reason",
}
DEMO_MARKERS = {"demo", "synthetic", "public_safe", "placeholder", "example"}
TRUE_VALUES = {"true", "1", "yes", "y"}
FALSE_VALUES = {"false", "0", "no", "n"}


@dataclass(frozen=True)
class UniverseRow:
    symbol: str
    effective_from: str
    effective_to: str
    active: bool
    asset_class: str
    exchange: str
    source: str
    status: str
    reason: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class UniverseValidationReport:
    passed: bool
    universe_path: str
    symbols: list[str] = field(default_factory=list)
    active_symbols: list[str] = field(default_factory=list)
    row_count: int = 0
    failures: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _parse_date(value: str, *, field_name: str, row_number: int, failures: list[str], required: bool = True) -> str:
    text = value.strip()
    if not text:
        if required:
            failures.append(f"row_{row_number}_missing_{field_name}")
        return ""
    try:
        date.fromisoformat(text)
    except ValueError:
        failures.append(f"row_{row_number}_invalid_{field_name}:{text}")
    return text


def _parse_bool(value: str, *, row_number: int, failures: list[str]) -> bool:
    text = value.strip().lower()
    if text in TRUE_VALUES:
        return True
    if text in FALSE_VALUES:
        return False
    failures.append(f"row_{row_number}_invalid_active:{value}")
    return False


def _has_demo_marker(row: dict[str, str]) -> bool:
    text = " ".join(str(value).lower() for value in row.values())
    return any(marker in text for marker in DEMO_MARKERS)


def _row_active_for_date_range(row: UniverseRow, start_date: str, end_date: str) -> bool:
    if not row.active:
        return False
    try:
        row_start = date.fromisoformat(row.effective_from)
        row_end = date.fromisoformat(row.effective_to) if row.effective_to else date.max
        requested_start = date.fromisoformat(start_date)
        requested_end = date.fromisoformat(end_date)
    except ValueError:
        return False
    return row_start <= requested_end and row_end >= requested_start


def read_survivorship_universe(path: Path) -> tuple[list[UniverseRow], list[str]]:
    if not path.exists():
        return [], ["missing_universe_file"]
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        columns = set(reader.fieldnames or [])
        missing_columns = sorted(REQUIRED_COLUMNS - columns)
        failures = [f"missing_columns:{','.join(missing_columns)}"] if missing_columns else []
        rows = list(reader)
    if not rows:
        failures.append("empty_universe_file")
        return [], failures

    parsed_rows: list[UniverseRow] = []
    seen_symbols: set[str] = set()
    for row_number, row in enumerate(rows, start=2):
        symbol = str(row.get("symbol") or "").strip().upper()
        if not symbol:
            failures.append(f"row_{row_number}_missing_symbol")
            continue
        if symbol in seen_symbols:
            failures.append(f"duplicate_symbol:{symbol}")
        seen_symbols.add(symbol)
        if _has_demo_marker(row):
            failures.append(f"row_{row_number}_demo_marker")
        effective_from = _parse_date(str(row.get("effective_from") or ""), field_name="effective_from", row_number=row_number, failures=failures)
        effective_to = _parse_date(
            str(row.get("effective_to") or ""),
            field_name="effective_to",
            row_number=row_number,
            failures=failures,
            required=False,
        )
        if effective_from and effective_to and effective_to < effective_from:
            failures.append(f"row_{row_number}_effective_to_before_from:{symbol}")
        active = _parse_bool(str(row.get("active") or ""), row_number=row_number, failures=failures)
        asset_class = str(row.get("asset_class") or "").strip().lower()
        exchange = str(row.get("exchange") or "").strip().upper()
        source = str(row.get("source") or "").strip().lower()
        status = str(row.get("status") or "").strip().lower()
        reason = str(row.get("reason") or "").strip()
        for field_name, value in {
            "asset_class": asset_class,
            "exchange": exchange,
            "source": source,
            "status": status,
            "reason": reason,
        }.items():
            if not value:
                failures.append(f"row_{row_number}_missing_{field_name}:{symbol}")
        parsed_rows.append(
            UniverseRow(
                symbol=symbol,
                effective_from=effective_from,
                effective_to=effective_to,
                active=active,
                asset_class=asset_class,
                exchange=exchange,
                source=source,
                status=status,
                reason=reason,
            )
        )
    return parsed_rows, failures


def validate_survivorship_universe(
    *,
    universe_path: Path,
    requested_symbols: list[str] | None = None,
    start_date: str | None = None,
    end_date: str | None = None,
) -> UniverseValidationReport:
    rows, failures = read_survivorship_universe(universe_path)
    symbols = sorted(row.symbol for row in rows)
    requested = sorted({symbol.strip().upper() for symbol in (requested_symbols or []) if symbol.strip()})
    active_symbols: list[str] = []
    if start_date or end_date:
        if not start_date or not end_date:
            failures.append("date_range_requires_start_and_end")
        else:
            try:
                date.fromisoformat(start_date)
                date.fromisoformat(end_date)
                if end_date < start_date:
                    failures.append("requested_end_before_start")
            except ValueError:
                failures.append("invalid_requested_date_range")
            if not any(failure.startswith("invalid_requested") or failure == "requested_end_before_start" for failure in failures):
                active_symbols = sorted(row.symbol for row in rows if _row_active_for_date_range(row, start_date, end_date))
                for symbol in requested:
                    if symbol not in active_symbols:
                        failures.append(f"requested_symbol_not_active:{symbol}")
    else:
        active_symbols = sorted(row.symbol for row in rows if row.active)
        for symbol in requested:
            if symbol not in active_symbols:
                failures.append(f"requested_symbol_not_active:{symbol}")

    return UniverseValidationReport(
        passed=not failures,
        universe_path=universe_path.as_posix(),
        symbols=symbols,
        active_symbols=active_symbols,
        row_count=len(rows),
        failures=failures,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate survivorship universe contract.")
    parser.add_argument("--universe", default="data/universe/survivorship_universe.csv")
    parser.add_argument("--symbols", default="")
    parser.add_argument("--start-date")
    parser.add_argument("--end-date")
    parser.add_argument("--report-output", default="reports/backtests/uni1-survivorship-universe-gate.json")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    symbols = [symbol.strip().upper() for symbol in args.symbols.split(",") if symbol.strip()]
    report = validate_survivorship_universe(
        universe_path=Path(args.universe),
        requested_symbols=symbols,
        start_date=args.start_date,
        end_date=args.end_date,
    )
    output = Path(args.report_output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report.to_dict(), indent=2), encoding="utf-8")
    print(f"UNI1 survivorship universe gate status: {'PASS' if report.passed else 'FAIL'}")
    if report.failures:
        print("Failures:")
        for failure in report.failures:
            print(f"- {failure}")
    print(f"Gate report: {output.as_posix()}")
    return 0 if report.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
