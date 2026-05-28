"""Telegram report dispatcher with research-only guardrails.

TG1 deliberately separates report delivery from trading execution. It prepares
and validates Telegram messages for research / paper-observation reporting only.
The default transport is dry-run/in-memory friendly so CI does not require
Telegram secrets or network access.
"""

from __future__ import annotations

import json
import re
import urllib.parse
import urllib.request
from dataclasses import asdict, dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Protocol


RESEARCH_ONLY_FOOTER = "Research / Paper Observation Only. No live trading authorization."


class TelegramDispatchStatus(str, Enum):
    SENT = "SENT"
    DRY_RUN = "DRY_RUN"
    BLOCKED = "BLOCKED"


class TelegramGuardrailSeverity(str, Enum):
    WARNING = "warning"
    ERROR = "error"


FORBIDDEN_LIVE_TRADING_PATTERNS: tuple[str, ...] = (
    r"\bbuy\s+now\b",
    r"\bsell\s+now\b",
    r"\bstrong\s+buy\b",
    r"\bstrong\s+sell\b",
    r"\blive\s+trade\b",
    r"\blive\s+trading\s+authorized\b",
    r"\bexecute\s+order\b",
    r"\bplace\s+order\b",
    r"\border\s+button\b",
    r"\bclick\s+to\s+trade\b",
    r"\bauto[-_ ]?execution\b",
)

FORBIDDEN_PRIVATE_EDGE_PATTERNS: tuple[str, ...] = (
    r"\balpha[_-]?weight[s]?\b",
    r"\bprivate[_-]?edge\b",
    r"\bproprietary[_-]?edge\b",
    r"\bsecret[_-]?threshold\b",
    r"\bproduction[_-]?threshold\b",
    r"\blive[_-]?(signal|entry)?[_-]?threshold\b",
    r"\bhidden[_-]?edge\b",
    r"\bedge[_-]?formula\b",
    r"\bmodel[_-]?weight[_-]?secret\b",
)


@dataclass(frozen=True)
class TelegramReportMessage:
    title: str
    body: str
    report_type: str
    footer: str = RESEARCH_ONLY_FOOTER
    include_timestamp: bool = False

    def render(self) -> str:
        parts = [f"*{self.title.strip()}*", "", self.body.strip(), "", self.footer.strip()]
        return "\n".join(part for part in parts if part != "")


@dataclass(frozen=True)
class TelegramGuardrailFinding:
    severity: TelegramGuardrailSeverity
    code: str
    match: str
    message: str

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["severity"] = self.severity.value
        return payload


@dataclass(frozen=True)
class TelegramDispatchConfig:
    report_only: bool = True
    dry_run: bool = True
    parse_mode: str = "Markdown"
    max_message_chars: int = 4096
    require_footer: bool = True
    block_live_trading_language: bool = True
    block_private_edge_terms: bool = True


@dataclass(frozen=True)
class TelegramDispatchResult:
    status: TelegramDispatchStatus
    sent: bool
    message: str
    findings: list[TelegramGuardrailFinding] = field(default_factory=list)
    transport_response: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "status": self.status.value,
            "sent": self.sent,
            "message": self.message,
            "findings": [finding.to_dict() for finding in self.findings],
            "transport_response": self.transport_response,
        }


class TelegramTransport(Protocol):
    def send_message(self, *, text: str, parse_mode: str) -> dict[str, Any]:
        """Send a Telegram message and return provider response metadata."""


class DryRunTelegramTransport:
    def send_message(self, *, text: str, parse_mode: str) -> dict[str, Any]:
        return {
            "ok": True,
            "dry_run": True,
            "parse_mode": parse_mode,
            "message_length": len(text),
        }


@dataclass(frozen=True)
class HttpTelegramTransport:
    bot_token: str
    chat_id: str
    timeout_seconds: int = 10

    def send_message(self, *, text: str, parse_mode: str) -> dict[str, Any]:
        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        payload = urllib.parse.urlencode(
            {
                "chat_id": self.chat_id,
                "text": text,
                "parse_mode": parse_mode,
                "disable_web_page_preview": "true",
            }
        ).encode("utf-8")
        request = urllib.request.Request(url, data=payload, method="POST")
        with urllib.request.urlopen(request, timeout=self.timeout_seconds) as response:  # nosec B310 - explicit Telegram API endpoint
            response_text = response.read().decode("utf-8")
        return json.loads(response_text)


def dispatch_telegram_report(
    message: TelegramReportMessage,
    *,
    config: TelegramDispatchConfig | None = None,
    transport: TelegramTransport | None = None,
) -> TelegramDispatchResult:
    active_config = config or TelegramDispatchConfig()
    rendered = message.render()
    findings = validate_telegram_report_message(rendered, config=active_config)
    has_errors = any(finding.severity == TelegramGuardrailSeverity.ERROR for finding in findings)

    if has_errors:
        return TelegramDispatchResult(
            status=TelegramDispatchStatus.BLOCKED,
            sent=False,
            message=rendered,
            findings=findings,
            transport_response=None,
        )

    if active_config.dry_run:
        dry_transport = transport or DryRunTelegramTransport()
        response = dry_transport.send_message(text=rendered, parse_mode=active_config.parse_mode)
        return TelegramDispatchResult(
            status=TelegramDispatchStatus.DRY_RUN,
            sent=False,
            message=rendered,
            findings=findings,
            transport_response=response,
        )

    if transport is None:
        raise ValueError("transport is required when dry_run=False")

    response = transport.send_message(text=rendered, parse_mode=active_config.parse_mode)
    return TelegramDispatchResult(
        status=TelegramDispatchStatus.SENT,
        sent=True,
        message=rendered,
        findings=findings,
        transport_response=response,
    )


def validate_telegram_report_message(
    text: str,
    *,
    config: TelegramDispatchConfig | None = None,
) -> list[TelegramGuardrailFinding]:
    active_config = config or TelegramDispatchConfig()
    findings: list[TelegramGuardrailFinding] = []

    if active_config.report_only and active_config.require_footer and RESEARCH_ONLY_FOOTER not in text:
        findings.append(
            TelegramGuardrailFinding(
                severity=TelegramGuardrailSeverity.ERROR,
                code="missing_research_only_footer",
                match="footer",
                message="Telegram report must include research-only/no-live-trading footer",
            )
        )

    if len(text) > active_config.max_message_chars:
        findings.append(
            TelegramGuardrailFinding(
                severity=TelegramGuardrailSeverity.ERROR,
                code="telegram_message_too_long",
                match=str(len(text)),
                message="Telegram message exceeds configured maximum length",
            )
        )

    if active_config.block_live_trading_language:
        findings.extend(
            _match_patterns(
                text,
                FORBIDDEN_LIVE_TRADING_PATTERNS,
                code="live_trading_language_blocked",
                message="Telegram report contains live-trading or order-action language",
            )
        )

    if active_config.block_private_edge_terms:
        findings.extend(
            _match_patterns(
                text,
                FORBIDDEN_PRIVATE_EDGE_PATTERNS,
                code="private_edge_term_blocked",
                message="Telegram report contains private-edge terminology",
            )
        )

    return findings


def build_report_message_from_file(
    report_path: Path | str,
    *,
    title: str,
    report_type: str,
    max_body_chars: int = 3500,
) -> TelegramReportMessage:
    path = Path(report_path)
    body = path.read_text(encoding="utf-8")
    if len(body) > max_body_chars:
        body = body[: max_body_chars - 80].rstrip() + "\n\n[truncated for Telegram]"
    return TelegramReportMessage(title=title, body=body, report_type=report_type)


def write_telegram_dispatch_result(result: TelegramDispatchResult, output_path: Path | str) -> None:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result.to_dict(), indent=2, sort_keys=True), encoding="utf-8")


def _match_patterns(
    text: str,
    patterns: tuple[str, ...],
    *,
    code: str,
    message: str,
) -> list[TelegramGuardrailFinding]:
    findings: list[TelegramGuardrailFinding] = []
    for pattern in patterns:
        for match in re.finditer(pattern, text, flags=re.IGNORECASE):
            findings.append(
                TelegramGuardrailFinding(
                    severity=TelegramGuardrailSeverity.ERROR,
                    code=code,
                    match=match.group(0),
                    message=message,
                )
            )
    return findings
