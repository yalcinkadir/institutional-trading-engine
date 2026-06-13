from __future__ import annotations

from pathlib import Path


WORKFLOW = Path(".github/workflows/entry-exit-watcher.yml")


def test_209_watcher_skip_writes_blocking_runtime_health_artifact() -> None:
    workflow = WORKFLOW.read_text(encoding="utf-8")

    assert "reports/runtime/entry_exit_watcher_runtime_health.json" in workflow
    assert '"status": "BLOCKED"' in workflow
    assert '"runtime_state": "SKIPPED"' in workflow
    assert '"skip": True' in workflow
    assert '"live_trading_authorized": False' in workflow
    assert '"broker_execution_mode": "paper_only"' in workflow
    assert "write_skip_health" in workflow


def test_209_missing_api_key_and_missing_signals_file_have_distinct_skip_reasons() -> None:
    workflow = WORKFLOW.read_text(encoding="utf-8")

    assert 'WATCHER_SKIP_REASON="missing_polygon_api_key"' in workflow
    assert 'WATCHER_SKIP_REASON="signals_file_not_found"' in workflow
    assert "POLYGON_API_KEY secret is missing." in workflow
    assert "signals file not found at $SIGNALS_FILE" in workflow


def test_209_watcher_skip_runtime_health_is_uploaded_and_notified() -> None:
    workflow = WORKFLOW.read_text(encoding="utf-8")

    assert "reports/runtime/" in workflow
    assert "Send watcher skip notification" in workflow
    assert "watcher-skip-message.txt" in workflow
    assert "Health: reports/runtime/entry_exit_watcher_runtime_health.json" in workflow


def test_209_watcher_skip_does_not_pretend_runtime_executed() -> None:
    workflow = WORKFLOW.read_text(encoding="utf-8")

    assert "WATCHER_SKIP=true" in workflow
    assert "if: env.WATCHER_SKIP != 'true'" in workflow
    assert "python scripts/run_entry_exit_watcher.py --signals-file" in workflow
