from __future__ import annotations

from pathlib import Path

import yaml


WORKFLOW_PATH = Path(".github/workflows/institutional-reports.yml")


def _workflow() -> dict:
    return yaml.safe_load(WORKFLOW_PATH.read_text(encoding="utf-8"))


def _report_steps() -> list[dict]:
    return _workflow()["jobs"]["report"]["steps"]


def _step_by_name(name: str) -> dict:
    for step in _report_steps():
        if step.get("name") == name:
            return step
    raise AssertionError(f"Workflow step not found: {name}")


def _step_index(name: str) -> int:
    for index, step in enumerate(_report_steps()):
        if step.get("name") == name:
            return index
    raise AssertionError(f"Workflow step not found: {name}")


def test_p114_generate_report_step_does_not_mask_nonzero_exit() -> None:
    step = _step_by_name("Generate report (+ signals)")
    run_script = step.get("run", "")

    assert "python scripts/generate_report.py" in run_script
    assert "|| true" not in run_script
    assert "set +e" not in run_script
    assert step.get("continue-on-error") is not True


def test_p114_workflow_stops_before_copy_validation_and_commit_when_report_generation_fails() -> None:
    generate_index = _step_index("Generate report (+ signals)")

    assert generate_index < _step_index("Validate report quality")
    assert generate_index < _step_index("Validate paper observation health")
    assert generate_index < _step_index("Commit all outputs to repository")

    run_script = _step_by_name("Generate report (+ signals)").get("run", "")
    generate_line = "python scripts/generate_report.py --type \"$GENERATOR_TYPE\" --output \"$REPORT_FILE\""
    copy_line = "cp \"$REPORT_FILE\" \"$LATEST_FILE\""

    assert generate_line in run_script
    assert copy_line in run_script
    assert run_script.index(generate_line) < run_script.index(copy_line)
