from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum
from typing import Any, Mapping

from src.notifications.telegram_report_dispatcher import RESEARCH_ONLY_FOOTER, TelegramReportMessage


class ReportTemplateType(str, Enum):
    DAILY_EVIDENCE = "daily_evidence"
    FILL_QUALITY = "fill_quality"
    KILL_SWITCH = "kill_switch"
    BACKTEST_SUMMARY = "backtest_summary"


@dataclass(frozen=True)
class RenderedReportTemplate:
    report_type: ReportTemplateType
    title: str
    markdown: str

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["report_type"] = self.report_type.value
        return payload


_TEMPLATE_TITLES = {
    ReportTemplateType.DAILY_EVIDENCE: "Daily Evidence Report",
    ReportTemplateType.FILL_QUALITY: "Fill Quality Report",
    ReportTemplateType.KILL_SWITCH: "Kill Switch Report",
    ReportTemplateType.BACKTEST_SUMMARY: "Backtest Summary Report",
}


_KEY_METRICS = {
    ReportTemplateType.DAILY_EVIDENCE: ("overall_status", "components_expected", "components_present", "components_failed", "components_missing"),
    ReportTemplateType.FILL_QUALITY: ("status", "record_count", "fill_rate", "avg_abs_slippage_bps", "max_abs_slippage_bps", "avg_delay_seconds"),
    ReportTemplateType.KILL_SWITCH: ("status", "blocked", "reason_count"),
    ReportTemplateType.BACKTEST_SUMMARY: ("status", "passed", "trade_count", "expectancy_r", "max_drawdown_r", "oos_pass_rate", "capacity_status"),
}


def render_report_template(
    report_type: ReportTemplateType | str,
    payload: Mapping[str, Any],
    *,
    report_date: str,
) -> RenderedReportTemplate:
    template_type = ReportTemplateType(report_type)
    title = _TEMPLATE_TITLES[template_type]
    metrics = _extract_metrics(template_type, payload)
    status = _extract_status(payload, metrics)

    lines = [
        f"# {title}",
        "",
        f"Date: **{report_date}**",
        f"Status: **{status}**",
        "",
        "## Key Metrics",
        "",
    ]
    if metrics:
        lines.extend(f"- {key}: {_format_value(value)}" for key, value in metrics.items())
    else:
        lines.append("- none")

    lines.extend(
        [
            "",
            "## Operation Boundary",
            "",
            "- research_and_paper_observation_only",
            "- report_delivery_only",
            "- no_broker_execution",
            "- no_live_trading_authorization",
            "- no_private_edge_parameters",
            "",
            RESEARCH_ONLY_FOOTER,
        ]
    )
    return RenderedReportTemplate(template_type, title, "\n".join(lines).rstrip() + "\n")


def build_telegram_message_from_template(template: RenderedReportTemplate) -> TelegramReportMessage:
    return TelegramReportMessage(title=template.title, body=template.markdown, report_type=template.report_type.value)


def build_tg2_tg3_report_templates(
    payloads: Mapping[str, Mapping[str, Any]],
    *,
    report_date: str,
) -> list[RenderedReportTemplate]:
    return [
        render_report_template(report_type, payloads[report_type.value], report_date=report_date)
        for report_type in ReportTemplateType
        if report_type.value in payloads
    ]


def build_tg2_tg3_telegram_messages(
    payloads: Mapping[str, Mapping[str, Any]],
    *,
    report_date: str,
) -> list[TelegramReportMessage]:
    return [build_telegram_message_from_template(template) for template in build_tg2_tg3_report_templates(payloads, report_date=report_date)]


def _extract_metrics(template_type: ReportTemplateType, payload: Mapping[str, Any]) -> dict[str, Any]:
    raw_metrics = payload.get("metrics", {}) if isinstance(payload.get("metrics", {}), Mapping) else {}
    values: dict[str, Any] = {}

    if template_type == ReportTemplateType.DAILY_EVIDENCE:
        values["overall_status"] = raw_metrics.get("overall_status", _extract_status(payload, raw_metrics))
    elif template_type == ReportTemplateType.KILL_SWITCH:
        values["reason_count"] = len(payload.get("reasons", [])) if isinstance(payload.get("reasons", []), list) else 0

    source = {**payload, **raw_metrics, **values}
    allowed = _KEY_METRICS[template_type]
    return {key: source[key] for key in allowed if key in source}


def _extract_status(payload: Mapping[str, Any], metrics: Mapping[str, Any]) -> str:
    if "overall_status" in metrics:
        return str(metrics["overall_status"]).upper()
    if "status" in payload:
        status = payload["status"]
        return str(getattr(status, "value", status)).upper()
    if "passed" in payload:
        return "PASS" if bool(payload["passed"]) else "FAIL"
    return "UNKNOWN"


def _format_value(value: Any) -> str:
    if isinstance(value, bool):
        return str(value).lower()
    if isinstance(value, float):
        return f"{value:.4f}"
    return str(value)
