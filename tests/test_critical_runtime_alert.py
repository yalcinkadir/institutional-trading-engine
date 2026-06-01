from pathlib import Path

from src.notifications.critical_runtime_alert import (
    CriticalRuntimeAlert,
    build_critical_runtime_alert_message,
    deliver_critical_runtime_alert_before_repo_persistence,
)
from src.notifications.telegram_report_dispatcher import (
    RESEARCH_ONLY_FOOTER,
    TelegramDispatchStatus,
)


def test_critical_stop_alert_message_is_research_only_and_order_safe() -> None:
    message = build_critical_runtime_alert_message(
        CriticalRuntimeAlert(
            alert_type="STOP",
            signal_id="sig-001",
            symbol="AAPL",
            reason="stop lifecycle threshold reached",
        )
    )
    rendered = message.render()

    assert "RGP5 Critical STOP Runtime Alert" in rendered
    assert "Signal ID: sig-001" in rendered
    assert "Symbol: AAPL" in rendered
    assert "Execution: none" in rendered
    assert "Repository persistence: after alert delivery only" in rendered
    assert RESEARCH_ONLY_FOOTER in rendered


def test_critical_alert_is_persisted_before_repository_persistence_failure(tmp_path: Path) -> None:
    output_path = tmp_path / "critical-alert.json"

    def failing_repository_persistence() -> None:
        assert output_path.exists()
        raise RuntimeError("git push failed")

    result = deliver_critical_runtime_alert_before_repo_persistence(
        CriticalRuntimeAlert(
            alert_type="EXIT",
            signal_id="sig-002",
            symbol="MSFT",
            reason="exit lifecycle status reached",
        ),
        alert_result_path=output_path,
        repository_persistence=failing_repository_persistence,
    )

    assert output_path.exists()
    assert result.alert_type == "EXIT"
    assert result.symbol == "MSFT"
    assert result.dispatch_status == TelegramDispatchStatus.DRY_RUN.value
    assert result.alert_persisted_before_repo is True
    assert result.repository_persisted is False
    assert result.repository_error == "git push failed"
    assert "DRY_RUN" in output_path.read_text(encoding="utf-8")


def test_repository_persistence_runs_after_alert_result_exists(tmp_path: Path) -> None:
    output_path = tmp_path / "critical-alert.json"
    observed_order: list[str] = []

    def repository_persistence() -> None:
        if output_path.exists():
            observed_order.append("alert_persisted_first")
        observed_order.append("repo_persisted")

    result = deliver_critical_runtime_alert_before_repo_persistence(
        CriticalRuntimeAlert(
            alert_type="STOP",
            signal_id="sig-003",
            symbol="NVDA",
            reason="stop lifecycle status reached",
        ),
        alert_result_path=output_path,
        repository_persistence=repository_persistence,
    )

    assert observed_order == ["alert_persisted_first", "repo_persisted"]
    assert result.alert_persisted_before_repo is True
    assert result.repository_persisted is True
    assert result.repository_error is None


def test_non_stop_exit_alert_type_is_rejected(tmp_path: Path) -> None:
    try:
        deliver_critical_runtime_alert_before_repo_persistence(
            CriticalRuntimeAlert(
                alert_type="INFO",
                signal_id="sig-004",
                symbol="QQQ",
                reason="not critical",
            ),
            alert_result_path=tmp_path / "critical-alert.json",
        )
    except ValueError as exc:
        assert "STOP or EXIT" in str(exc)
    else:
        raise AssertionError("Expected non-critical alert type to be rejected")
