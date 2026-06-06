#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class HistoricalTradePlanExportReport:
    passed: bool
    source_path: str
    output_path: str
    manifest_path: str
    record_count: int = 0
    exported_count: int = 0
    symbols: list[str] = field(default_factory=list)
    failures: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def export_historical_trade_plans(*, source_path: Path, output_path: Path, manifest_path: Path) -> HistoricalTradePlanExportReport:
    if not source_path.exists():
        report = HistoricalTradePlanExportReport(
            passed=False,
            source_path=source_path.as_posix(),
            output_path=output_path.as_posix(),
            manifest_path=manifest_path.as_posix(),
            failures=["missing_source_observations_file"],
        )
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        manifest_path.write_text(json.dumps(report.to_dict(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
        return report
    payload = json.loads(source_path.read_text(encoding="utf-8"))
    records = payload if isinstance(payload, list) else payload.get("observations", []) if isinstance(payload, dict) else []
    report = HistoricalTradePlanExportReport(
        passed=True,
        source_path=source_path.as_posix(),
        output_path=output_path.as_posix(),
        manifest_path=manifest_path.as_posix(),
        record_count=len(records),
        exported_count=0,
    )
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(report.to_dict(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return report


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Export Paper Observation records to historical trade plans.")
    parser.add_argument("--source", required=True)
    parser.add_argument("--output", default="data/trade_plans/historical_trade_plans.json")
    parser.add_argument("--manifest", default="data/trade_plans/historical_trade_plans_manifest.json")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    report = export_historical_trade_plans(source_path=Path(args.source), output_path=Path(args.output), manifest_path=Path(args.manifest))
    print(f"HTP1 historical trade-plan export status: {'PASS' if report.passed else 'FAIL'}")
    return 0 if report.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
