from __future__ import annotations

from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
WORKFLOW = REPO_ROOT / ".github" / "workflows" / "institutional-reports.yml"

LATEST_HEALTH_JSON = "reports/validation/latest-paper-observation-health.json"
DATED_HEALTH_JSON = "reports/validation/paper_observation_health.json"
HEALTH_MARKDOWN = "reports/validation/paper_observation_health.md"


def _workflow_text() -> str:
    return WORKFLOW.read_text(encoding="utf-8")


def _workflow() -> dict:
    return yaml.safe_load(_workflow_text())


def test_institutional_reports_uploads_latest_paper_observation_health_json() -> None:
    text = _workflow_text()

    assert "python scripts/validate_paper_observation_health.py" in text
    assert "--signals-file reports/signals/latest-signals.json" in text
    assert "--report-dir reports/validation" in text
    assert "--run-timestamp \"$HEALTH_RUN_TIMESTAMP\"" in text
    assert "--workflow-name \"${GITHUB_WORKFLOW}\"" in text
    assert "--commit-sha \"${GITHUB_SHA}\"" in text
    assert LATEST_HEALTH_JSON in text
    assert DATED_HEALTH_JSON in text
    assert HEALTH_MARKDOWN in text


def test_paper_observation_health_artifact_step_is_retained_and_strict() -> None:
    workflow = _workflow()
    jobs = workflow.get("jobs", {})
    assert jobs, "institutional reports workflow must define jobs"

    upload_steps = []
    for job in jobs.values():
        for step in job.get("steps", []):
            if step.get("uses") == "actions/upload-artifact@v4":
                with_block = step.get("with", {}) or {}
                name = str(with_block.get("name", ""))
                path = str(with_block.get("path", ""))
                if "paper-observation-health" in name or LATEST_HEALTH_JSON in path:
                    upload_steps.append(step)

    assert upload_steps, "paper observation health upload artifact step is required"
    assert len(upload_steps) == 1, "health artifact upload should have one canonical step"

    step = upload_steps[0]
    with_block = step.get("with", {}) or {}
    assert str(step.get("if", "")).strip() == "always()"
    assert "paper-observation-health" in str(with_block.get("name", ""))
    path_block = str(with_block.get("path", ""))
    assert DATED_HEALTH_JSON in path_block
    assert HEALTH_MARKDOWN in path_block
    assert LATEST_HEALTH_JSON in path_block
    assert str(with_block.get("if-no-files-found", "")).lower() == "error"
    assert str(with_block.get("retention-days", "")) == "90"


def test_latest_health_artifact_contract_is_inspectable_without_committed_reports() -> None:
    text = _workflow_text()

    assert "HEALTH_RUN_TIMESTAMP" in text
    assert "GITHUB_WORKFLOW" in text
    assert "GITHUB_SHA" in text
    assert "latest-paper-observation-health.json" in text
    assert "if-no-files-found: error" in text
