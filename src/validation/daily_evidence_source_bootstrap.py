from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import date, timedelta
from pathlib import Path
from typing import Any

SOURCE_BOOTSTRAP_VERSION = "2026.05.26-v1"


@dataclass(frozen=True)
class BootstrappedSourceFile:
    filename: str
    records: int
    path: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class DailyEvidenceSourceBootstrapReport:
    passed: bool
    bootstrap_version: str
    observation_only: bool
    report_date: str
    output_dir: str
    files: list[BootstrappedSourceFile] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "passed": self.passed,
            "bootstrap_version": self.bootstrap_version,
            "observation_only": self.observation_only,
            "report_date": self.report_date,
            "output_dir": self.output_dir,
            "files": [item.to_dict() for item in self.files],
            "warnings": list(self.warnings),
        }


def bootstrap_daily_evidence_sources(output_dir: Path, *, report_date: str | date) -> DailyEvidenceSourceBootstrapReport:
    normalized_date = _normalize_date(report_date)
    output_dir.mkdir(parents=True, exist_ok=True)
    payloads = _build_payloads(normalized_date)

    files: list[BootstrappedSourceFile] = []
    for filename, records in payloads.items():
        path = output_dir / filename
        path.write_text(json.dumps(records, indent=2), encoding="utf-8")
        files.append(BootstrappedSourceFile(filename=filename, records=len(records), path=str(path)))

    return DailyEvidenceSourceBootstrapReport(
        passed=True,
        bootstrap_version=SOURCE_BOOTSTRAP_VERSION,
        observation_only=True,
        report_date=normalized_date,
        output_dir=str(output_dir),
        files=files,
        warnings=[
            "observation-only bootstrap seed; not statistically meaningful forward evidence",
            "do not use this seed to authorize live capital",
            "replace with real daily observation sources as soon as available",
        ],
    )


def render_daily_evidence_source_bootstrap_markdown(report: DailyEvidenceSourceBootstrapReport) -> str:
    lines = [
        "# Daily Evidence Source Bootstrap",
        "",
        f"Status: **{'PASS' if report.passed else 'FAIL'}**",
        f"Bootstrap version: `{report.bootstrap_version}`",
        f"Report date: **{report.report_date}**",
        f"Observation-only: **{str(report.observation_only).lower()}**",
        f"Output dir: `{report.output_dir}`",
        "",
        "## Files",
        "",
        "| File | Records | Path |",
        "|---|---:|---|",
    ]
    for item in report.files:
        lines.append(f"| `{item.filename}` | {item.records} | `{item.path}` |")
    lines.extend(["", "## Warnings", ""])
    for warning in report.warnings:
        lines.append(f"- {warning}")
    return "\n".join(lines).rstrip() + "\n"


def write_daily_evidence_source_bootstrap_report(
    report: DailyEvidenceSourceBootstrapReport,
    *,
    json_path: Path,
    markdown_path: Path,
) -> None:
    json_path.parent.mkdir(parents=True, exist_ok=True)
    markdown_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(report.to_dict(), indent=2), encoding="utf-8")
    markdown_path.write_text(render_daily_evidence_source_bootstrap_markdown(report), encoding="utf-8")


def _build_payloads(report_date: str) -> dict[str, list[dict[str, Any]]]:
    end = date.fromisoformat(report_date)
    forward_values = [0.25, 0.15, -0.10, 0.30, 0.05, -0.05, 0.20, 0.10, 0.35, -0.15,
                      0.25, 0.15, -0.10, 0.30, 0.05, -0.05, 0.20, 0.10, 0.35, -0.15]
    backtest_values = forward_values * 2
    return {
        "paper_observations.json": _paper_observations(end, forward_values),
        "backtest_results.json": [{"result_r": value, "source": "observation_only_bootstrap"} for value in backtest_values],
        "forward_results.json": [{"result_r": value, "source": "observation_only_bootstrap"} for value in forward_values],
        "regime_observations.json": _regime_observations(end, 24),
        "position_snapshots.json": _position_snapshots(),
    }


def _paper_observations(end: date, values: list[float]) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for index, value in enumerate(values):
        observation_date = (end - timedelta(days=len(values) - index - 1)).isoformat()
        action = "ENTER" if value > 0 else "SKIP"
        records.append(
            {
                "observation_date": observation_date,
                "expected_action": action,
                "paper_action": action,
                "expected_result_r": value,
                "paper_result_r": value,
                "resolved": True,
                "source": "observation_only_bootstrap",
            }
        )
    return records


def _regime_observations(end: date, length: int) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for index in range(length):
        records.append(
            {
                "date": (end - timedelta(days=length - index - 1)).isoformat(),
                "regime_label": "neutral",
                "volatility_pct": 0.18 + (index % 3) * 0.001,
                "corr": 0.42 + (index % 2) * 0.002,
                "drawdown_pct": 0.02 + (index % 4) * 0.001,
                "source": "observation_only_bootstrap",
            }
        )
    return records


def _position_snapshots() -> list[dict[str, Any]]:
    return [
        {
            "symbol": "AAPL",
            "sector": "Technology",
            "portfolio_weight": 0.5,
            "paper_r": 0.2,
            "beta": 1.1,
            "market_r": 0.1,
            "factor_exposures": {"momentum": 0.4, "quality": 0.2},
            "factor_returns": {"momentum": 0.2, "quality": 0.1},
            "source": "observation_only_bootstrap",
        },
        {
            "symbol": "MSFT",
            "sector": "Technology",
            "portfolio_weight": 0.5,
            "paper_r": 0.15,
            "beta": 1.0,
            "market_r": 0.1,
            "factor_exposures": {"momentum": 0.3, "quality": 0.3},
            "factor_returns": {"momentum": 0.2, "quality": 0.1},
            "source": "observation_only_bootstrap",
        },
    ]


def _normalize_date(value: str | date) -> str:
    if isinstance(value, date):
        return value.isoformat()
    return date.fromisoformat(str(value)).isoformat()
