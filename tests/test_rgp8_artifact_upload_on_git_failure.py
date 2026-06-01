from __future__ import annotations

from pathlib import Path

WORKFLOW_DIR = Path(".github/workflows")
REPO_WRITE_COMMANDS = (
    "git push",
    "git commit",
    "git pull",
    "git rebase",
)
ARTIFACT_UPLOAD_MARKERS = (
    "actions/upload-artifact",
    "uses: actions/upload-artifact",
)
ALWAYS_UPLOAD_MARKERS = (
    "if: always()",
    "if: ${{ always() }}",
    "if: ${{always()}}",
)
EVIDENCE_ARTIFACT_MARKERS = (
    "alert",
    "alerts",
    "evidence",
    "manifest",
    "report",
    "runtime",
)


def _workflow_files() -> list[Path]:
    return sorted(
        path
        for pattern in ("*.yml", "*.yaml")
        for path in WORKFLOW_DIR.glob(pattern)
    )


def _is_repo_writing_workflow(content: str) -> bool:
    lowered = content.lower()
    return any(command in lowered for command in REPO_WRITE_COMMANDS)


def _has_always_artifact_upload(content: str) -> bool:
    lowered = content.lower()
    return (
        any(marker in lowered for marker in ARTIFACT_UPLOAD_MARKERS)
        and any(marker in lowered for marker in ALWAYS_UPLOAD_MARKERS)
        and any(marker in lowered for marker in EVIDENCE_ARTIFACT_MARKERS)
    )


def test_repo_writing_workflows_upload_alert_or_evidence_artifacts_even_on_failure() -> None:
    failures: list[str] = []

    for workflow_path in _workflow_files():
        content = workflow_path.read_text(encoding="utf-8")
        if not _is_repo_writing_workflow(content):
            continue

        if _has_always_artifact_upload(content):
            continue

        failures.append(str(workflow_path))

    assert failures == [], (
        "Repo-writing workflows must upload alert/evidence artifacts with if: always() "
        "so git persistence failures cannot erase runtime evidence: " + ", ".join(failures)
    )


def test_rgp8_guard_accepts_workflow_with_always_uploaded_evidence_artifact() -> None:
    workflow = """
    name: runtime evidence writer
    concurrency:
      group: ${{ github.repository }}-repo-write
    jobs:
      write:
        steps:
          - run: git push
          - name: Upload runtime evidence artifact
            if: always()
            uses: actions/upload-artifact@v4
            with:
              name: runtime-evidence-alerts
              path: artifacts/evidence/
    """

    assert _is_repo_writing_workflow(workflow) is True
    assert _has_always_artifact_upload(workflow) is True


def test_rgp8_guard_rejects_repo_write_without_always_artifact_upload() -> None:
    workflow = """
    name: unsafe repo writer
    jobs:
      write:
        steps:
          - run: git commit -am update && git push
    """

    assert _is_repo_writing_workflow(workflow) is True
    assert _has_always_artifact_upload(workflow) is False
