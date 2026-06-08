#!/usr/bin/env python3
"""Build a real-data historical backtest evidence package.

The script orchestrates the existing real-data path:

1. optional Polygon historical ingestion
2. BT9 real historical input-pack validation through the backtest runner
3. BT130 real-data backtest evidence generation
4. real-data evidence-gate validation
5. package manifest writing

It intentionally fails closed when a licensed/approved data source is missing.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from scripts.validate_real_data_backtest_evidence_gate import validate_real_data_backtest_evidence_artifact

APPROVED_DATA_SOURCES = {"polygon"}
DEFAULT_OUTPUT_DIR = Path("reports/backtests/real-data-evidence-pack")


@dataclass(frozen=True)
class RealDataBacktestEvidencePackage:
    status: str
    run_id: str
    data_source: str
    is_demo: bool
    symbols: list[str]
    date_range: dict[str, str]
    output_dir: str
    evidence_json_path: str
    evidence_markdown_path: str
    coverage_manifest_path: str
    survivorship_universe_path: str
    trade_plans_path: str
    bt130_gate_status: str
    block_reasons: list[str] = field(default_factory=list)
    command_log: list[str] = field(default_factory=list)
    evidence_gate_report: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--symbols", required=True, help="Comma-separated symbols, e.g. SPY,QQQ,AAPL")
    parser.add_argument("--start-date", required=True)
    parser.add_argument("--end-date", required=True)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--data-source", default="polygon", choices=sorted(APPROVED_DATA_SOURCES))
    parser.add_argument("--plans-file", default="data/trade_plans/historical_trade_plans.json")
    parser.add_argument("--bars-root", default="data/historical/bars/1day")
    parser.add_argument("--universe", default="data/universe/survivorship_universe.csv")
    parser.add_argument("--coverage-manifest", default="data/historical/metadata/coverage_manifest.json")
    parser.add_argument("--ingestion-output-root", default="data/historical")
    parser.add_argument("--ingestion-metadata-path", default="data/historical/metadata/ingestion_status.json")
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR))
    parser.add_argument("--max-bars", type=int, default=20)
    parser.add_argument("--skip-ingestion", action="store_true", help="Use already prepared historical bars and coverage manifest.")
    return parser.parse_args()


def _symbols(raw: str) -> list[str]:
    return [symbol.strip().upper() for symbol in raw.split(",") if symbol.strip()]


def _write_package(package: RealDataBacktestEvidencePackage, output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / "real-data-backtest-evidence-package.json"
    path.write_text(json.dumps(package.to_dict(), indent=2, sort_keys=True), encoding="utf-8")
    return path


def _run(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=ROOT_DIR, text=True, capture_output=True, check=False)


def _blocked_package(args: argparse.Namespace, reason: str, commands: list[str] | None = None) -> RealDataBacktestEvidencePackage:
    output_dir = Path(args.output_dir)
    return RealDataBacktestEvidencePackage(
        status="BLOCKED",
        run_id=args.run_id,
        data_source=args.data_source,
        is_demo=False,
        symbols=_symbols(args.symbols),
        date_range={"start": args.start_date, "end": args.end_date},
        output_dir=output_dir.as_posix(),
        evidence_json_path=(output_dir / "real-data-backtest-evidence.json").as_posix(),
        evidence_markdown_path=(output_dir / "real-data-backtest-evidence.md").as_posix(),
        coverage_manifest_path=args.coverage_manifest,
        survivorship_universe_path=args.universe,
        trade_plans_path=args.plans_file,
        bt130_gate_status="NOT_RUN",
        block_reasons=[reason],
        command_log=commands or [],
        evidence_gate_report=None,
    )


def _ingest_if_requested(args: argparse.Namespace, commands: list[str]) -> int | None:
    if args.skip_ingestion:
        commands.append("ingestion skipped; using prepared historical bars")
        return None
    if not os.getenv("POLYGON_API_KEY"):
        return 1

    command = [
        sys.executable,
        "scripts/ingest_historical_polygon.py",
        "--symbols",
        args.symbols,
        "--start-date",
        args.start_date,
        "--end-date",
        args.end_date,
        "--output-root",
        args.ingestion_output_root,
        "--metadata-path",
        args.ingestion_metadata_path,
        "--coverage-manifest-path",
        args.coverage_manifest,
    ]
    commands.append(" ".join(command))
    result = _run(command)
    commands.append(result.stdout.strip())
    if result.stderr.strip():
        commands.append(result.stderr.strip())
    return None if result.returncode == 0 else result.returncode


def build_package(args: argparse.Namespace) -> tuple[RealDataBacktestEvidencePackage, int]:
    commands: list[str] = []
    output_dir = Path(args.output_dir)
    evidence_json = output_dir / "real-data-backtest-evidence.json"
    evidence_md = output_dir / "real-data-backtest-evidence.md"

    if args.data_source not in APPROVED_DATA_SOURCES:
        package = _blocked_package(args, f"unapproved_data_source:{args.data_source}", commands)
        _write_package(package, output_dir)
        return package, 1

    ingestion_exit = _ingest_if_requested(args, commands)
    if ingestion_exit == 1 and not args.skip_ingestion and not os.getenv("POLYGON_API_KEY"):
        package = _blocked_package(args, "missing_POLYGON_API_KEY", commands)
        _write_package(package, output_dir)
        return package, 1
    if ingestion_exit is not None:
        package = _blocked_package(args, f"historical_ingestion_failed:{ingestion_exit}", commands)
        _write_package(package, output_dir)
        return package, 1

    backtest_command = [
        sys.executable,
        "scripts/run_historical_entry_exit_backtest.py",
        "--plans-file",
        args.plans_file,
        "--bars-root",
        args.bars_root,
        "--universe",
        args.universe,
        "--coverage-manifest",
        args.coverage_manifest,
        "--run-id",
        args.run_id,
        "--data-source",
        "real_data",
        "--real-data",
        "--max-bars",
        str(args.max_bars),
        "--json-output",
        evidence_json.as_posix(),
        "--markdown-output",
        evidence_md.as_posix(),
    ]
    commands.append(" ".join(backtest_command))
    backtest = _run(backtest_command)
    commands.append(backtest.stdout.strip())
    if backtest.stderr.strip():
        commands.append(backtest.stderr.strip())
    if backtest.returncode != 0:
        package = _blocked_package(args, f"real_data_backtest_failed:{backtest.returncode}", commands)
        _write_package(package, output_dir)
        return package, 1

    gate = validate_real_data_backtest_evidence_artifact(evidence_json)
    payload = json.loads(evidence_json.read_text(encoding="utf-8"))
    package = RealDataBacktestEvidencePackage(
        status="VALID" if gate.passed else "FAILED",
        run_id=args.run_id,
        data_source="polygon",
        is_demo=False,
        symbols=list(payload.get("symbol_universe", _symbols(args.symbols))),
        date_range=dict(payload.get("date_range", {"start": args.start_date, "end": args.end_date})),
        output_dir=output_dir.as_posix(),
        evidence_json_path=evidence_json.as_posix(),
        evidence_markdown_path=evidence_md.as_posix(),
        coverage_manifest_path=args.coverage_manifest,
        survivorship_universe_path=args.universe,
        trade_plans_path=args.plans_file,
        bt130_gate_status="PASSED" if gate.passed else "FAILED",
        block_reasons=[] if gate.passed else gate.invalid_fields + gate.missing_fields + gate.errors,
        command_log=commands,
        evidence_gate_report=gate.to_dict(),
    )
    _write_package(package, output_dir)
    return package, 0 if gate.passed else 1


def main() -> int:
    args = parse_args()
    package, exit_code = build_package(args)
    print(f"Real-data backtest evidence package status: {package.status}")
    print(f"Package: {Path(args.output_dir) / 'real-data-backtest-evidence-package.json'}")
    if package.block_reasons:
        print("Block reasons:")
        for reason in package.block_reasons:
            print(f"- {reason}")
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
