#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.operations.paper_observation_evidence_gate import validate_paper_observation_evidence_artifact


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate paper observation evidence artifact schema.")
    parser.add_argument("--artifact", default="reports/paper-live/paper-live-observation.json")
    parser.add_argument("--report-output", default="reports/paper-live/paper-observation-evidence-gate.json")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    report = validate_paper_observation_evidence_artifact(Path(args.artifact))
    output = Path(args.report_output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report.to_dict(), indent=2), encoding="utf-8")

    status = "PASS" if report.passed else "FAIL"
    print(f"Paper observation evidence gate status: {status}")
    print(f"Artifact: {report.artifact_path}")
    if report.missing_fields:
        print(f"Missing fields: {', '.join(report.missing_fields)}")
    if report.invalid_fields:
        print(f"Invalid fields: {', '.join(report.invalid_fields)}")
    if report.errors:
        print(f"Errors: {', '.join(report.errors)}")
    print(f"Gate report: {args.report_output}")
    return 0 if report.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
