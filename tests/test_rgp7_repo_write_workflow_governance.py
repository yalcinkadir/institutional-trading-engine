from __future__ import annotations

from pathlib import Path

WORKFLOW_DIR = Path(".github/workflows")
REPO_WRITE_COMMANDS = (
    "git push",
    "git commit",
    "git pull",
    "git rebase",
)
REPO_WIDE_CONCURRENCY_MARKERS = (
    "group: repo-write",
    "group: ${{ github.repository }}-repo-write",
    "group: ${{github.repository}}-repo-write",
)
PUSH_RETRY_MARKERS = (
    "retry",
    "for attempt in",
    "until git push",
    "git pull --rebase",
    "git fetch origin",
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


def _has_repo_wide_concurrency(content: str) -> bool:
    return any(marker in content for marker in REPO_WIDE_CONCURRENCY_MARKERS)


def _has_push_retry_strategy(content: str) -> bool:
    lowered = content.lower()
    return "git push" in lowered and any(marker in lowered for marker in PUSH_RETRY_MARKERS)


def test_repo_writing_workflows_are_serialized_or_retry_guarded() -> None:
    failures: list[str] = []

    for workflow_path in _workflow_files():
        content = workflow_path.read_text(encoding="utf-8")
        if not _is_repo_writing_workflow(content):
            continue

        if _has_repo_wide_concurrency(content) or _has_push_retry_strategy(content):
            continue

        failures.append(str(workflow_path))

    assert failures == [], (
        "Repo-writing workflows must use repo-wide concurrency group "
        "or a robust pull/rebase/push retry strategy: " + ", ".join(failures)
    )


def test_workflow_guard_scans_actual_workflow_directory() -> None:
    workflows = _workflow_files()

    assert workflows, "Expected at least one GitHub Actions workflow to be scanned"
    assert any(path.name == "ci.yml" for path in workflows)
