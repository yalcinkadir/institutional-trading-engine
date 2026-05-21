"""Entry / Stop / Exit feedback aggregation.

Aggregates historical outcome records by decision-quality dimensions such as
entry_type, setup_type, stop_model and exit_model.

The module is intentionally source-agnostic: records can come from historical
validation, lifecycle outcomes, JSONL files or future database rows.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Iterable, Literal


GroupField = Literal[
    "entry_type",
    "setup_type",
    "stop_model",
    "exit_model",
    "market_regime",
    "risk_state",
    "volatility_regime",
]
DEFAULT_GROUP_FIELDS: tuple[GroupField, ...] = (
    "entry_type",
    "setup_type",
    "stop_model",
    "exit_model",
)
REGIME_AWARE_GROUP_FIELDS: tuple[GroupField, ...] = (
    "entry_type",
    "setup_type",
    "stop_model",
    "exit_model",
    "market_regime",
    "risk_state",
    "volatility_regime",
)
REGIME_ONLY_GROUP_FIELDS: tuple[GroupField, ...] = (
    "market_regime",
    "risk_state",
    "volatility_regime",
)

ENTRY_HIT_STATUSES = {"ENTRY_TRIGGERED", "TARGET_1_HIT", "TARGET_2_HIT", "STOP_HIT"}
TARGET_1_STATUSES = {"TARGET_1_HIT", "TARGET_2_HIT"}
TARGET_2_STATUSES = {"TARGET_2_HIT"}
STOP_STATUSES = {"STOP_HIT"}
EXPIRED_STATUSES = {"EXPIRED", "EXPIRED_WITHOUT_ENTRY"}
FALSE_BREAKOUT_STATUSES = {"FALSE_BREAKOUT"}


@dataclass(frozen=True)
class EntryStopExitStats:
    group_field: str
    group_value: str
    total: int = 0
    entry_hits: int = 0
    stop_hits: int = 0
    target_1_hits: int = 0
    target_2_hits: int = 0
    expired_without_entry: int = 0
    false_breakouts: int = 0
    entry_hit_rate: float = 0.0
    stop_hit_rate: float = 0.0
    target_1_hit_rate: float = 0.0
    target_2_hit_rate: float = 0.0
    expired_without_entry_rate: float = 0.0
    false_breakout_rate: float = 0.0


@dataclass(frozen=True)
class EntryStopExitFeedbackReport:
    total_records: int
    overall: EntryStopExitStats
    grouped: dict[str, list[EntryStopExitStats]] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "total_records": self.total_records,
            "overall": asdict(self.overall),
            "grouped": {
                key: [asdict(item) for item in values]
                for key, values in self.grouped.items()
            },
        }


def _safe_label(value: Any, *, default: str = "unknown") -> str:
    if value is None:
        return default
    text = str(value).strip()
    return text if text else default


def _status(record: dict[str, Any]) -> str:
    for key in ("outcome", "final_status", "status", "event_type"):
        value = record.get(key)
        if value:
            return str(value).strip().upper()
    return "UNKNOWN"


def _bool(record: dict[str, Any], key: str) -> bool:
    return bool(record.get(key) is True)


def _entry_hit(record: dict[str, Any], status: str) -> bool:
    return _bool(record, "entry_hit") or status in ENTRY_HIT_STATUSES


def _target_1_hit(record: dict[str, Any], status: str) -> bool:
    return _bool(record, "target_1_hit") or status in TARGET_1_STATUSES


def _target_2_hit(record: dict[str, Any], status: str) -> bool:
    return _bool(record, "target_2_hit") or status in TARGET_2_STATUSES


def _stop_hit(record: dict[str, Any], status: str) -> bool:
    return _bool(record, "stop_hit") or status in STOP_STATUSES


def _expired_without_entry(record: dict[str, Any], status: str) -> bool:
    if _bool(record, "expired_without_entry"):
        return True
    return status in EXPIRED_STATUSES and not _entry_hit(record, status)


def _false_breakout(record: dict[str, Any], status: str) -> bool:
    if _bool(record, "false_breakout"):
        return True
    return status in FALSE_BREAKOUT_STATUSES or (
        _entry_hit(record, status)
        and _stop_hit(record, status)
        and not _target_1_hit(record, status)
    )


def _rate(count: int, total: int) -> float:
    if total <= 0:
        return 0.0
    return round(count / total, 4)


def _build_stats(group_field: str, group_value: str, records: list[dict[str, Any]]) -> EntryStopExitStats:
    total = len(records)
    entry_hits = 0
    stop_hits = 0
    target_1_hits = 0
    target_2_hits = 0
    expired_without_entry = 0
    false_breakouts = 0

    for record in records:
        status = _status(record)
        if _entry_hit(record, status):
            entry_hits += 1
        if _stop_hit(record, status):
            stop_hits += 1
        if _target_1_hit(record, status):
            target_1_hits += 1
        if _target_2_hit(record, status):
            target_2_hits += 1
        if _expired_without_entry(record, status):
            expired_without_entry += 1
        if _false_breakout(record, status):
            false_breakouts += 1

    return EntryStopExitStats(
        group_field=group_field,
        group_value=group_value,
        total=total,
        entry_hits=entry_hits,
        stop_hits=stop_hits,
        target_1_hits=target_1_hits,
        target_2_hits=target_2_hits,
        expired_without_entry=expired_without_entry,
        false_breakouts=false_breakouts,
        entry_hit_rate=_rate(entry_hits, total),
        stop_hit_rate=_rate(stop_hits, total),
        target_1_hit_rate=_rate(target_1_hits, total),
        target_2_hit_rate=_rate(target_2_hits, total),
        expired_without_entry_rate=_rate(expired_without_entry, total),
        false_breakout_rate=_rate(false_breakouts, total),
    )


def aggregate_entry_stop_exit_feedback(
    records: Iterable[dict[str, Any]],
    *,
    group_fields: Iterable[GroupField] = DEFAULT_GROUP_FIELDS,
) -> EntryStopExitFeedbackReport:
    """Aggregate Entry / Stop / Exit feedback from historical records."""
    rows = [dict(record) for record in records if isinstance(record, dict)]
    overall = _build_stats("overall", "all", rows)

    grouped: dict[str, list[EntryStopExitStats]] = {}
    for field in group_fields:
        buckets: dict[str, list[dict[str, Any]]] = {}
        for record in rows:
            label = _safe_label(record.get(field))
            buckets.setdefault(label, []).append(record)

        grouped[str(field)] = sorted(
            (_build_stats(str(field), label, bucket) for label, bucket in buckets.items()),
            key=lambda item: (-item.total, item.group_value),
        )

    return EntryStopExitFeedbackReport(
        total_records=len(rows),
        overall=overall,
        grouped=grouped,
    )


def aggregate_regime_aware_entry_stop_exit_feedback(
    records: Iterable[dict[str, Any]],
) -> EntryStopExitFeedbackReport:
    """Aggregate feedback using model and regime dimensions."""
    return aggregate_entry_stop_exit_feedback(
        records,
        group_fields=REGIME_AWARE_GROUP_FIELDS,
    )


def format_entry_stop_exit_feedback_markdown(report: EntryStopExitFeedbackReport) -> str:
    """Format feedback report as Markdown for weekly reports or artifacts."""
    lines = [
        "# Entry / Stop / Exit Feedback",
        "",
        f"Total records: **{report.total_records}**",
        "",
        "## Overall",
        _format_stats_line(report.overall),
        "",
    ]

    for group_field, stats in report.grouped.items():
        lines.append(f"## By {group_field}")
        if not stats:
            lines.append("- No data")
        else:
            for item in stats:
                lines.append(_format_stats_line(item))
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def _pct(value: float) -> str:
    return f"{value * 100:.1f}%"


def _format_stats_line(stats: EntryStopExitStats) -> str:
    return (
        f"- **{stats.group_value}** "
        f"n={stats.total} | "
        f"entry {_pct(stats.entry_hit_rate)} | "
        f"stop {_pct(stats.stop_hit_rate)} | "
        f"T1 {_pct(stats.target_1_hit_rate)} | "
        f"T2 {_pct(stats.target_2_hit_rate)} | "
        f"expired {_pct(stats.expired_without_entry_rate)} | "
        f"false breakout {_pct(stats.false_breakout_rate)}"
    )
