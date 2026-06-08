from __future__ import annotations

from pathlib import Path


WORKFLOW_PATH = Path(".github/workflows/daily-evidence-report.yml")


def _workflow() -> str:
    return WORKFLOW_PATH.read_text(encoding="utf-8")


def _index(text: str, needle: str) -> int:
    position = text.find(needle)
    assert position >= 0, f"Missing expected workflow fragment: {needle}"
    return position


def test_scheduled_daily_evidence_builds_sources_before_persistence() -> None:
    workflow = _workflow()

    scheduled_source_step = _index(workflow, "Build scheduled paper observation incoming sources")
    persist_step = _index(workflow, "Persist daily observation sources")

    assert scheduled_source_step < persist_step
    assert "if: ${{ github.event_name == 'schedule' }}" in workflow
    assert "python scripts/build_daily_paper_observation_sources.py" in workflow
    assert '--source-dir "reports/daily_paper_observation_raw"' in workflow
    assert "--output-dir reports/daily_observation_incoming" in workflow
    assert "--report-dir reports/daily_paper_observation_source" in workflow


def test_scheduled_daily_evidence_reviews_raw_source_cadence() -> None:
    workflow = _workflow()

    source_step = _index(workflow, "Build scheduled paper observation incoming sources")
    cadence_step = _index(workflow, "Review scheduled paper observation cadence")
    failure_step = _index(workflow, "Fail workflow on scheduled paper cadence failure")

    assert source_step < cadence_step < failure_step
    assert "id: scheduled-cadence" in workflow
    assert "python scripts/review_daily_observation_cadence.py" in workflow
    assert '--raw-source-dir "reports/daily_paper_observation_raw"' in workflow
    assert "steps.scheduled-cadence.outputs.exit_code != '0'" in workflow


def test_scheduled_daily_evidence_artifact_upload_fails_loudly() -> None:
    workflow = _workflow()

    upload_step = _index(workflow, "Upload daily evidence artifact")
    assert upload_step > _index(workflow, "Persist daily observation sources")
    assert "if-no-files-found: error" in workflow
    assert "reports/daily_paper_observation_source/" in workflow
    assert "reports/daily_observation_cadence/" in workflow
    assert "reports/daily_observation_source_feed/" in workflow
    assert "reports/daily_evidence/" in workflow


def test_scheduled_daily_evidence_no_longer_relies_on_dispatch_only_source_build() -> None:
    workflow = _workflow()

    schedule_source_condition = "if: ${{ github.event_name == 'schedule' }}"
    dispatch_source_condition = "if: ${{ github.event_name == 'workflow_dispatch' && github.event.inputs.use_real_paper_observation_source == 'true' }}"

    assert schedule_source_condition in workflow
    assert dispatch_source_condition in workflow
    assert _index(workflow, "Build scheduled paper observation incoming sources") < _index(
        workflow,
        "Build real paper observation incoming sources",
    )
