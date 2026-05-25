from __future__ import annotations

from pathlib import Path


WORKFLOW = Path(".github/workflows/edge-evidence-from-polygon-artifact.yml")


def _content() -> str:
    return WORKFLOW.read_text(encoding="utf-8")


def test_edge_evidence_from_polygon_artifact_workflow_exists() -> None:
    assert WORKFLOW.exists()


def test_edge_evidence_from_polygon_artifact_workflow_inputs() -> None:
    content = _content()

    assert "workflow_dispatch" in content
    assert "run_id:" in content
    assert "required: true" in content
    assert "default: \"polygon-edge-runtime-dataset-combined*\"" in content
    assert "default: \"data/trade_plans/historical_trade_plans.json\"" in content
    assert "default: \"500\"" in content


def test_edge_evidence_from_polygon_artifact_workflow_downloads_combined_artifact() -> None:
    content = _content()

    assert "gh run download" in content
    assert "polygon-edge-runtime-dataset-combined*" in content
    assert "runtime_artifacts/polygon_combined_input" in content


def test_edge_evidence_from_polygon_artifact_workflow_resolves_dataset_paths() -> None:
    content = _content()

    assert "survivorship_universe.csv" in content
    assert "historical_bars" in content
    assert "POLYGON_EDGE_UNIVERSE" in content
    assert "POLYGON_EDGE_BARS_ROOT" in content


def test_edge_evidence_from_polygon_artifact_workflow_uploads_reports_and_fails_closed() -> None:
    content = _content()

    assert "scripts/run_edge_evidence_backtest.py" in content
    assert "actions/upload-artifact@v4" in content
    assert "edge-evidence-from-polygon-artifact" in content
    assert "Fail if edge evidence gates failed" in content
    assert "steps.edge_backtest.outcome == 'failure'" in content
