from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

from src.config.paper_observation_universe import (
    CORE_OBSERVATION_UNIVERSE,
    MACRO_CFD_OBSERVATION_UNIVERSE,
    OBSERVATION_UNIVERSE_VERSION,
)

ALLOWED_ASSET_EVENT_STATUSES = {"STARTED", "COMPLETED", "SKIPPED", "FAILED"}


@dataclass(frozen=True)
class PaperObservationAssetEvent:
    symbol: str
    status: str
    event_time_utc: str
    report_date: str
    group: str
    note: str = ""

    def to_dict(self) -> dict[str, str]:
        return asdict(self)


@dataclass(frozen=True)
class PaperObservationAssetTimeline:
    report_date: str
    universe_version: str
    events: list[PaperObservationAssetEvent] = field(default_factory=list)

    def to_dict(self) -> dict[str, object]:
        return {
            "report_date": self.report_date,
            "universe_version": self.universe_version,
            "events": [event.to_dict() for event in self.events],
        }

    @property
    def symbols(self) -> list[str]:
        return [event.symbol for event in self.events]


def build_asset_timeline_template(
    *,
    report_date: str,
    event_time_utc: str | None = None,
    include_macro_cfd: bool = True,
) -> PaperObservationAssetTimeline:
    timestamp = event_time_utc or datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    events: list[PaperObservationAssetEvent] = []
    events.extend(
        PaperObservationAssetEvent(
            symbol=symbol,
            status="STARTED",
            event_time_utc=timestamp,
            report_date=report_date,
            group="core",
            note="B1.1 paper observation asset queued for treatment.",
        )
        for symbol in CORE_OBSERVATION_UNIVERSE
    )
    if include_macro_cfd:
        events.extend(
            PaperObservationAssetEvent(
                symbol=symbol,
                status="STARTED",
                event_time_utc=timestamp,
                report_date=report_date,
                group="macro_cfd_watch",
                note="Separate macro/CFD watch asset queued for treatment.",
            )
            for symbol in MACRO_CFD_OBSERVATION_UNIVERSE
        )
    return PaperObservationAssetTimeline(
        report_date=report_date,
        universe_version=OBSERVATION_UNIVERSE_VERSION,
        events=events,
    )


def validate_asset_timeline(timeline: PaperObservationAssetTimeline) -> list[str]:
    issues: list[str] = []
    expected_core = set(CORE_OBSERVATION_UNIVERSE)
    expected_macro = set(MACRO_CFD_OBSERVATION_UNIVERSE)
    seen_core = {event.symbol for event in timeline.events if event.group == "core"}
    seen_macro = {event.symbol for event in timeline.events if event.group == "macro_cfd_watch"}

    missing_core = sorted(expected_core - seen_core)
    if missing_core:
        issues.append(f"missing core symbols: {', '.join(missing_core)}")

    unknown_symbols = sorted(
        event.symbol
        for event in timeline.events
        if event.symbol not in expected_core and event.symbol not in expected_macro
    )
    if unknown_symbols:
        issues.append(f"unknown symbols: {', '.join(unknown_symbols)}")

    invalid_statuses = sorted({event.status for event in timeline.events if event.status not in ALLOWED_ASSET_EVENT_STATUSES})
    if invalid_statuses:
        issues.append(f"invalid statuses: {', '.join(invalid_statuses)}")

    invalid_dates = sorted({event.symbol for event in timeline.events if event.report_date != timeline.report_date})
    if invalid_dates:
        issues.append(f"event report date mismatch: {', '.join(invalid_dates)}")

    return issues


def render_asset_timeline_markdown(timeline: PaperObservationAssetTimeline, *, issues: Iterable[str] = ()) -> str:
    issues = list(issues)
    lines = [
        "# B1.1 Paper Observation Asset Timeline",
        "",
        f"Report date: `{timeline.report_date}`",
        f"Universe version: `{timeline.universe_version}`",
        f"Status: **{'PASS' if not issues else 'FAIL'}**",
        "",
        "## Asset treatment events",
        "",
        "| Time UTC | Symbol | Group | Status | Note |",
        "|---|---|---|---|---|",
    ]
    for event in timeline.events:
        lines.append(
            f"| `{event.event_time_utc}` | `{event.symbol}` | `{event.group}` | `{event.status}` | {event.note or '-'} |"
        )
    lines.extend(["", "## Issues", ""])
    lines.extend(f"- {issue}" for issue in issues) if issues else lines.append("- none")
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "This timeline documents paper-observation treatment only. It does not authorize live trading, broker execution or real-money deployment.",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def write_asset_timeline(timeline: PaperObservationAssetTimeline, *, json_path: Path, markdown_path: Path) -> list[str]:
    issues = validate_asset_timeline(timeline)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    markdown_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(timeline.to_dict(), indent=2), encoding="utf-8")
    markdown_path.write_text(render_asset_timeline_markdown(timeline, issues=issues), encoding="utf-8")
    return issues
