from pathlib import Path

import pytest

from src.notifications.telegram_report_dispatcher import (
    RESEARCH_ONLY_FOOTER,
    TelegramDispatchConfig,
    TelegramDispatchStatus,
    TelegramReportMessage,
    build_report_message_from_file,
    dispatch_telegram_report,
    validate_telegram_report_message,
    write_telegram_dispatch_result,
)


class RecordingTransport:
    def __init__(self) -> None:
        self.calls: list[dict[str, str]] = []

    def send_message(self, *, text: str, parse_mode: str) -> dict[str, object]:
        self.calls.append({"text": text, "parse_mode": parse_mode})
        return {"ok": True, "message_id": 123}


def test_dispatcher_dry_run_allows_research_only_report() -> None:
    message = TelegramReportMessage(
        title="Daily Evidence",
        body="Status: PASS\nExecution quality: WATCH",
        report_type="daily_evidence",
    )

    result = dispatch_telegram_report(message)

    assert result.status == TelegramDispatchStatus.DRY_RUN
    assert result.sent is False
    assert RESEARCH_ONLY_FOOTER in result.message
    assert result.findings == []
    assert result.transport_response and result.transport_response["dry_run"] is True


def test_dispatcher_blocks_order_action_language() -> None:
    blocked_phrase = "place" + " " + "order"
    message = TelegramReportMessage(
        title="Report",
        body=f"Do not allow: {blocked_phrase}",
        report_type="research_report",
    )

    result = dispatch_telegram_report(message)

    assert result.status == TelegramDispatchStatus.BLOCKED
    assert result.sent is False
    assert any(finding.code == "live_trading_language_blocked" for finding in result.findings)


def test_dispatcher_blocks_private_edge_terms() -> None:
    blocked_term = "alpha" + "_" + "weights"
    message = TelegramReportMessage(
        title="Report",
        body=f"Do not allow: {blocked_term}",
        report_type="research_report",
    )

    result = dispatch_telegram_report(message)

    assert result.status == TelegramDispatchStatus.BLOCKED
    assert any(finding.code == "private_edge_term_blocked" for finding in result.findings)


def test_validator_blocks_missing_footer_when_required() -> None:
    findings = validate_telegram_report_message(
        "Plain report without footer",
        config=TelegramDispatchConfig(require_footer=True),
    )

    assert any(finding.code == "missing_research_only_footer" for finding in findings)


def test_dispatcher_uses_real_transport_when_send_enabled() -> None:
    transport = RecordingTransport()
    message = TelegramReportMessage(
        title="Fill Quality",
        body="Status: PASS",
        report_type="fill_quality",
    )

    result = dispatch_telegram_report(
        message,
        config=TelegramDispatchConfig(dry_run=False),
        transport=transport,
    )

    assert result.status == TelegramDispatchStatus.SENT
    assert result.sent is True
    assert len(transport.calls) == 1
    assert transport.calls[0]["parse_mode"] == "Markdown"


def test_dispatcher_requires_transport_when_send_enabled() -> None:
    message = TelegramReportMessage(
        title="Report",
        body="Status: PASS",
        report_type="daily_evidence",
    )

    with pytest.raises(ValueError):
        dispatch_telegram_report(message, config=TelegramDispatchConfig(dry_run=False))


def test_build_report_message_from_file_truncates_body(tmp_path: Path) -> None:
    report_path = tmp_path / "report.md"
    report_path.write_text("A" * 5000, encoding="utf-8")

    message = build_report_message_from_file(
        report_path,
        title="Long Report",
        report_type="daily_evidence",
        max_body_chars=200,
    )

    assert "[truncated for Telegram]" in message.body
    assert len(message.body) <= 200


def test_write_dispatch_result(tmp_path: Path) -> None:
    result = dispatch_telegram_report(
        TelegramReportMessage(title="Report", body="Status: PASS", report_type="test")
    )
    output_path = tmp_path / "dispatch" / "result.json"

    write_telegram_dispatch_result(result, output_path)

    assert output_path.exists()
    assert "DRY_RUN" in output_path.read_text(encoding="utf-8")
