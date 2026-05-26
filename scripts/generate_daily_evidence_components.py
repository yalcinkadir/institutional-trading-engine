#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from datetime import date, timedelta
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.validation.monte_carlo_robustness import (  # noqa: E402
    MonteCarloRobustnessConfig,
    run_monte_carlo_robustness,
    write_monte_carlo_robustness_report,
)
from src.validation.paper_observation_reconciliation import (  # noqa: E402
    PaperObservationConfig,
    reconcile_paper_observation,
    write_paper_observation_report,
)
from src.validation.performance_drift_detection import (  # noqa: E402
    PerformanceDriftConfig,
    detect_performance_drift,
    write_performance_drift_report,
)
from src.validation.position_risk_attribution import (  # noqa: E402
    PositionRiskAttributionConfig,
    attribute_position_risk,
    write_position_risk_attribution_report,
)
from src.validation.regime_change_detection import (  # noqa: E402
    RegimeChangeConfig,
    detect_regime_change,
    write_regime_change_report,
)
from src.validation.sequential_edge_decay import (  # noqa: E402
    SequentialEdgeDecayConfig,
    run_sequential_edge_decay_test,
    write_sequential_edge_decay_report,
)


COMPONENT_FILENAMES = {
    "reconciliation": "paper_observation_reconciliation",
    "performance_drift": "performance_drift_detection",
    "edge_decay": "sequential_edge_decay",
    "regime_change": "regime_change_detection",
    "risk_attribution": "position_risk_attribution",
    "monte_carlo": "monte_carlo_robustness",
}

INPUT_FILENAMES = {
    "paper_records": "paper_observation_records.json",
    "backtest_records": "backtest_records.json",
    "forward_records": "forward_records.json",
    "regime_records": "regime_records.json",
    "position_records": "position_records.json",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Generate Phase B1-B6 component evidence reports by running the real validation modules. "
            "Use --input-dir for actual observation inputs or --use-smoke-fixture for deterministic workflow smoke evidence."
        )
    )
    parser.add_argument("--input-dir", type=Path, help="Directory containing component input JSON files.")
    parser.add_argument("--output-dir", type=Path, required=True, help="Directory where component JSON/Markdown reports are written.")
    parser.add_argument("--report-date", default=None, help="Report date YYYY-MM-DD. Defaults to UTC/current date when omitted.")
    parser.add_argument(
        "--use-smoke-fixture",
        action="store_true",
        help="Generate deterministic smoke inputs when real observation input files are not available yet.",
    )
    parser.add_argument(
        "--min-observation-days",
        type=int,
        default=1,
        help="Minimum B1 observation days required for the generated daily component report.",
    )
    parser.add_argument(
        "--simulations",
        type=int,
        default=250,
        help="Monte Carlo simulations for the generated component report.",
    )
    parser.add_argument(
        "--observation-only",
        action="store_true",
        help="Write reports and keep the run green when component gates fail during bootstrap observation mode.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    report_date = args.report_date or date.today().isoformat()
    inputs = _load_inputs(args.input_dir) if args.input_dir else {}
    if args.use_smoke_fixture:
        inputs = {**_build_smoke_inputs(report_date), **inputs}

    missing = [key for key in INPUT_FILENAMES if key not in inputs]
    if missing:
        print(
            "Missing evidence input files: "
            + ", ".join(INPUT_FILENAMES[key] for key in missing)
            + ". Provide --input-dir with real inputs or use --use-smoke-fixture.",
            file=sys.stderr,
        )
        return 2

    output_dir: Path = args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    reports = {
        "reconciliation": reconcile_paper_observation(
            inputs["paper_records"],
            config=PaperObservationConfig(min_observation_days=args.min_observation_days),
            observation_only=True,
        ),
        "performance_drift": detect_performance_drift(
            inputs["backtest_records"],
            inputs["forward_records"],
            config=PerformanceDriftConfig(min_backtest_observations=20, min_forward_observations=10),
        ),
        "edge_decay": run_sequential_edge_decay_test(
            inputs["forward_records"],
            config=SequentialEdgeDecayConfig(min_observations=20),
        ),
        "regime_change": detect_regime_change(
            inputs["regime_records"],
            config=RegimeChangeConfig(min_observations=20),
        ),
        "risk_attribution": attribute_position_risk(
            inputs["position_records"],
            config=PositionRiskAttributionConfig(),
        ),
        "monte_carlo": run_monte_carlo_robustness(
            inputs["forward_records"],
            config=MonteCarloRobustnessConfig(
                min_observations=20,
                simulations=args.simulations,
                min_permutation_p_value=0.0,
            ),
        ),
    }

    _write_reports(reports, output_dir=output_dir)
    failed = [name for name, report in reports.items() if not report.passed]
    print(f"Generated {len(reports)} daily evidence component reports in {output_dir}")
    if failed:
        print("Failed components: " + ", ".join(failed))
        if args.observation_only:
            print("Observation-only mode: failed component gates are recorded but do not fail the workflow.")
            return 0
        return 1
    print("All generated daily evidence components passed")
    return 0


def _load_inputs(input_dir: Path | None) -> dict[str, Any]:
    if input_dir is None:
        return {}
    inputs: dict[str, Any] = {}
    for key, filename in INPUT_FILENAMES.items():
        path = input_dir / filename
        if path.exists():
            inputs[key] = json.loads(path.read_text(encoding="utf-8"))
    return inputs


def _write_reports(reports: dict[str, Any], *, output_dir: Path) -> None:
    writers = {
        "reconciliation": write_paper_observation_report,
        "performance_drift": write_performance_drift_report,
        "edge_decay": write_sequential_edge_decay_report,
        "regime_change": write_regime_change_report,
        "risk_attribution": write_position_risk_attribution_report,
        "monte_carlo": write_monte_carlo_robustness_report,
    }
    for name, report in reports.items():
        stem = COMPONENT_FILENAMES[name]
        writers[name](
            report,
            json_path=output_dir / f"{stem}.json",
            markdown_path=output_dir / f"{stem}.md",
        )


def _build_smoke_inputs(report_date: str) -> dict[str, Any]:
    forward_values = _result_sequence(40)
    backtest_values = _result_sequence(80)
    paper_records = _paper_records(report_date, forward_values[:20])
    return {
        "paper_records": paper_records,
        "backtest_records": [{"result_r": value} for value in backtest_values],
        "forward_records": [{"result_r": value, "paper_r": value} for value in forward_values],
        "regime_records": _regime_records(report_date, 24),
        "position_records": _position_records(),
    }


def _result_sequence(length: int) -> list[float]:
    pattern = [0.7, -0.25, 0.55, 0.2, -0.15]
    return [pattern[index % len(pattern)] for index in range(length)]


def _paper_records(report_date: str, values: list[float]) -> list[dict[str, Any]]:
    end = date.fromisoformat(report_date)
    records: list[dict[str, Any]] = []
    for index, value in enumerate(values):
        observation_date = (end - timedelta(days=len(values) - index - 1)).isoformat()
        action = "ENTER" if value > 0 else "SKIP"
        records.append(
            {
                "observation_date": observation_date,
                "expected_action": action,
                "paper_action": action,
                "expected_r": value,
                "paper_r": value,
                "resolved": True,
            }
        )
    return records


def _regime_records(report_date: str, length: int) -> list[dict[str, Any]]:
    end = date.fromisoformat(report_date)
    records: list[dict[str, Any]] = []
    for index in range(length):
        records.append(
            {
                "date": (end - timedelta(days=length - index - 1)).isoformat(),
                "regime": "neutral",
                "volatility": 0.18 + (index % 3) * 0.001,
                "correlation": 0.42 + (index % 2) * 0.002,
                "drawdown": 0.02 + (index % 4) * 0.001,
            }
        )
    return records


def _position_records() -> list[dict[str, Any]]:
    return [
        {
            "symbol": "AAPL",
            "sector": "Technology",
            "weight": 0.5,
            "result_r": 0.6,
            "beta": 1.1,
            "market_return_r": 0.1,
            "factor_exposures": {"momentum": 0.4, "quality": 0.2},
            "factor_returns": {"momentum": 0.2, "quality": 0.1},
        },
        {
            "symbol": "MSFT",
            "sector": "Technology",
            "weight": 0.5,
            "result_r": 0.4,
            "beta": 1.0,
            "market_return_r": 0.1,
            "factor_exposures": {"momentum": 0.3, "quality": 0.3},
            "factor_returns": {"momentum": 0.2, "quality": 0.1},
        },
    ]


if __name__ == "__main__":
    raise SystemExit(main())
