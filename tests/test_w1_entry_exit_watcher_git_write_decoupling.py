from __future__ import annotations

from pathlib import Path


WORKFLOW = Path(".github/workflows/entry-exit-watcher.yml")


def _workflow_text() -> str:
    assert WORKFLOW.exists(), f"Missing workflow: {WORKFLOW}"
    return WORKFLOW.read_text(encoding="utf-8")


def test_w1_entry_exit_watcher_does_not_have_repo_write_permission() -> None:
    text = _workflow_text()

    assert "contents: write" not in text
    assert "contents: read" in text


def test_w1_entry_exit_watcher_does_not_commit_or_push_to_schedule_branch() -> None:
    text = _workflow_text()

    forbidden_fragments = (
        "git add ",
        "git commit",
        "git pull --rebase",
        "git push",
        "HEAD:${GITHUB_REF_NAME}",
    )

    for fragment in forbidden_fragments:
        assert fragment not in text


def test_w1_entry_exit_watcher_uses_artifacts_for_runtime_outputs() -> None:
    text = _workflow_text()

    assert "actions/upload-artifact@v4" in text
    assert "entry-exit-runtime-${{ github.run_id }}" in text
    assert "reports/alerts/" in text
    assert "reports/signals/" in text
    assert "data/" in text


def test_w1_entry_exit_watcher_has_isolated_concurrency_group() -> None:
    text = _workflow_text()

    assert "group: entry-exit-watcher-${{ github.ref }}" in text
    assert "group: repo-write-${{ github.ref }}" not in text
