from __future__ import annotations

from pathlib import Path

import yaml


WORKFLOW = Path(".github/workflows/edge-evidence-from-polygon-artifact.yml")


def _load_workflow() -> dict:
    return yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))


def test_edge_evidence_from_polygon_artifact_workflow_exists() -> None:
    assert WORKFLOW.exists()


def test_edge_evidence_from_polygon_artifact_workflow_inputs() -> None:
    data = _load_workflow()
    inputs = data["on"]["workflow_dispatch"]["inputs"]

    assert inputs["run_id"]["required"] is True
    assert inputs["artifact_pattern"]["default"] == "polygon-edge-runtime-dataset-combined*"
    assert inputs["plans_path"]["default"] == "data/trade_plans/historical_trade_plans.json"
    assert inputs["minimum_assets"]["default"] == "500"


def test_edge_evidence_from_polygon_artifact_workflow_downloads_combined_artifact() -> None:
    content = WORKFLOW.read_text(encoding="utf-8")

    assert "gh run download" in content
    assert "polygon-edge-runtime-dataset-combined*" in content
    assert "runtime_artifacts/polygon_combined_input" in content


def test_edge_evidence_from_polygon_artifact_workflow_resolves_dataset_paths() -> None:
    content = WORKFLOW.read_text(encoding="utf-8")

    assert "survivorship_universe.csv" in content
    assert "historical_bars" in content
    assert "POLYGON_EDGE_UNIVERSE" in content
    assert "POLYGON_EDGE_BARS_ROOT" in content


def test_edge_evidence_from_polygon_artifact_workflow_uploads_reports_and_fails_closed() -> None:
    content = WORKFLOW.read_text(encoding="utf-8")

    assert "scripts/run_edge_evidence_backtest.py" in content
    assert "actions/upload-artifact@v4" in content
    assert "edge-evidence-from-polygon-artifact" in content
    assert "Fail if edge evidence gates failed" in content
    assert "steps.edge_backtest.outcome == 'failure'" in content
