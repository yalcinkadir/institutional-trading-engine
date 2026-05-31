from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
WORKFLOW_DIR = REPO_ROOT / ".github" / "workflows"
SHARED_REPO_WRITE_GROUP = "group: repo-write-${{ github.ref }}"
REBASE_BEFORE_PUSH = 'git pull --rebase origin "${GITHUB_REF_NAME}"'


def _workflow_files() -> list[Path]:
    return sorted(WORKFLOW_DIR.glob("*.yml")) + sorted(WORKFLOW_DIR.glob("*.yaml"))


def test_repo_writing_workflows_use_shared_serialization_group() -> None:
    offenders: list[str] = []

    for workflow in _workflow_files():
        content = workflow.read_text(encoding="utf-8")
        if "git push origin" not in content:
            continue

        if SHARED_REPO_WRITE_GROUP not in content or "cancel-in-progress: false" not in content:
            offenders.append(workflow.name)

    assert offenders == []


def test_repo_writing_workflows_rebase_before_push() -> None:
    offenders: list[str] = []

    for workflow in _workflow_files():
        content = workflow.read_text(encoding="utf-8")
        if "git push origin" not in content:
            continue
        if REBASE_BEFORE_PUSH not in content:
            offenders.append(workflow.name)

    assert offenders == []