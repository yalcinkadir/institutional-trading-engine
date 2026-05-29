import subprocess
import sys
from pathlib import Path

from src.config.paper_observation_universe import (
    CORE_OBSERVATION_UNIVERSE,
    EXCLUDED_OBSERVATION_GROUPS,
    MACRO_CFD_OBSERVATION_UNIVERSE,
    format_observation_universe,
)
from src.notifications.paper_observation_notification import (
    PaperObservationNotification,
    build_paper_observation_notification_message,
)
from src.notifications.telegram_report_dispatcher import (
    RESEARCH_ONLY_FOOTER,
    TelegramDispatchStatus,
    dispatch_telegram_report,
)

SCRIPT = Path("scripts/send_paper_observation_notification.py")


def test_observation_universe_is_fixed_for_b11() -> None:
    assert CORE_OBSERVATION_UNIVERSE == (
        "QQQ",
        "SPY",
        "AAPL",
        "MSFT",
        "NVDA",
        "META",
        "GOOGL",
        "AMZN",
        "MU",
        "AMD",
        "V",
        "INTC",
    )
    assert MACRO_CFD_OBSERVATION_UNIVERSE == ("NDQ100", "XAG")
    assert "crypto" in EXCLUDED_OBSERVATION_GROUPS
    assert "options_data" in EXCLUDED_OBSERVATION_GROUPS


def test_notification_message_is_research_only_and_safe() -> None:
    message = build_paper_observation_notification_message(
        PaperObservationNotification(report_date="2026-05-29", status="STARTED")
    )
    result = dispatch_telegram_report(message)

    assert result.status == TelegramDispatchStatus.DRY_RUN
    assert result.sent is False
    assert result.findings == []
    assert RESEARCH_ONLY_FOOTER in result.message
    assert "Execution: none" in result.message
    assert "Real-money authorization: not granted" in result.message
    assert "QQQ" in result.message
    assert "XAG" in result.message


def test_unknown_notification_status_is_rejected() -> None:
    try:
        build_paper_observation_notification_message(
            PaperObservationNotification(report_date="2026-05-29", status="EXECUTE")
        )
    except ValueError as exc:
        assert "STARTED" in str(exc)
    else:
        raise AssertionError("Expected invalid status to be rejected")


def test_cli_sends_dry_run_notification(tmp_path: Path) -> None:
    output_json = tmp_path / "paper-observation-notification.json"
    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--report-date",
            "2026-05-29",
            "--status",
            "STARTED",
            "--output-json",
            str(output_json),
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    assert "Paper observation notification status: DRY_RUN" in result.stdout
    assert output_json.exists()
    assert "DRY_RUN" in output_json.read_text(encoding="utf-8")


def test_format_observation_universe_contains_exclusions() -> None:
    rendered = format_observation_universe()

    assert "Core:" in rendered
    assert "Macro/CFD watch:" in rendered
    assert "Excluded for B1.1:" in rendered
    assert "new_strategies" in rendered
