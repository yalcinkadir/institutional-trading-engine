from __future__ import annotations

from pathlib import Path


WORKFLOW = Path(".github/workflows/entry-exit-watcher.yml")


def test_entry_exit_watcher_workflow_uses_notification_cli() -> None:
    content = WORKFLOW.read_text(encoding="utf-8")

    assert "python scripts/send_notification.py" in content
    assert "--message-file reports/alerts/watcher-alert-summary.txt" in content
    assert "--message-file reports/watcher-failure-message.txt" in content
    assert "--cycle-id \"$WATCHER_CYCLE_ID\"" in content


def test_entry_exit_watcher_workflow_no_longer_uses_direct_telegram_curl() -> None:
    content = WORKFLOW.read_text(encoding="utf-8")

    assert "api.telegram.org" not in content
    assert "sendMessage" not in content
    assert "--data-urlencode text" not in content


def test_entry_exit_watcher_workflow_supports_webhook_secret() -> None:
    content = WORKFLOW.read_text(encoding="utf-8")

    assert "REPORT_WEBHOOK_URL: ${{ secrets.REPORT_WEBHOOK_URL }}" in content
    assert "--webhook" in content
