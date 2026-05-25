from __future__ import annotations

from pathlib import Path

import yaml


def _load_workflow() -> dict:
    workflow = Path(".github/workflows/polygon-artifact-consolidation.yml")
    return yaml.safe_load(workflow.read_text(encoding="utf-8"))


def _workflow_on(data: dict) -> dict:
    return data.get("on", data.get(True, {}))


def test_polygon_artifact_consolidation_workflow_has_manual_inputs() -> None:
    data = _load_workflow()
    inputs = _workflow_on(data)["workflow_dispatch"]["inputs"]

    assert inputs["run_ids"]["required"] is True
    assert inputs["artifact_pattern"]["default"] == "polygon-edge-runtime-dataset*"
    assert inputs["output_name"]["default"] == "polygon-edge-runtime-dataset-combined"
    assert inputs["minimum_bar_files"]["default"] == "500"


def test_polygon_artifact_consolidation_workflow_downloads_by_run_id() -> None:
    data = _load_workflow()
    steps = data["jobs"]["consolidate-polygon-artifacts"]["steps"]
    download_step = next(step for step in steps if step["name"] == "Download Polygon batch artifacts")

    assert "GH_TOKEN" in download_step["env"]
    assert "RUN_IDS" in download_step["env"]
    assert "gh run download" in download_step["run"]
    assert "--pattern" in download_step["run"]


def test_polygon_artifact_consolidation_workflow_uploads_combined_artifact() -> None:
    data = _load_workflow()
    steps = data["jobs"]["consolidate-polygon-artifacts"]["steps"]
    upload_step = next(step for step in steps if step["name"] == "Upload combined Polygon runtime dataset")

    assert upload_step["uses"] == "actions/upload-artifact@v4"
    assert "runtime_artifacts/polygon_combined/" in upload_step["with"]["path"]
