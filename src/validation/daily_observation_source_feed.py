from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

SOURCE_FILE_NAMES = (
    "paper_observations.json",
    "backtest_results.json",
    "forward_results.json",
    "regime_observations.json",
    "position_snapshots.json",
)

FEED_VERSION = "2026.05.26-v1"


@dataclass(frozen=True)
class PersistedObservationFile:
    filename: str
    incoming_records: int
    existing_records: int
    appended_records: int
    total_records: int
    path: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class DailyObservationSourceFeedReport:
    passed: bool
    feed_version: str
    incoming_dir: str
    feed_dir: str
    report_date: str
    files: list[PersistedObservationFile] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "passed": self.passed,
            "feed_version": self.feed_version,
            "incoming_dir": self.incoming_dir,
            "feed_dir": self.feed_dir,
            "report_date": self.report_date,
            "files": [item.to_dict() for item in self.files],
            "errors": list(self.errors),
        }


def persist_daily_observation_sources(
    incoming_dir: Path,
    feed_dir: Path,
    *,
    report_date: str,
) -> DailyObservationSourceFeedReport:
    """Append incoming daily observation source records into a persisted source feed.

    The persisted feed is stored as normalized JSON arrays using the same source filenames
    that the daily evidence input builder expects. Records are de-duplicated by a stable
    content hash and annotated with feed metadata. Missing incoming files fail closed.
    """
    errors: list[str] = []
    incoming_payloads: dict[str, list[dict[str, Any]]] = {}

    for filename in SOURCE_FILE_NAMES:
        path = incoming_dir / filename
        if not path.exists():
            errors.append(f"missing incoming source file: {filename}")
            continue
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"invalid json in {filename}: {exc.msg}")
            continue
        if not isinstance(payload, list):
            errors.append(f"incoming source file {filename} must contain a list")
            continue
        if not payload:
            errors.append(f"incoming source file {filename} must not be empty")
            continue
        invalid_indices = [index for index, item in enumerate(payload) if not isinstance(item, dict)]
        if invalid_indices:
            errors.append(f"incoming source file {filename} has non-object records: {invalid_indices}")
            continue
        incoming_payloads[filename] = payload

    if errors:
        return DailyObservationSourceFeedReport(
            passed=False,
            feed_version=FEED_VERSION,
            incoming_dir=str(incoming_dir),
            feed_dir=str(feed_dir),
            report_date=report_date,
            errors=errors,
        )

    feed_dir.mkdir(parents=True, exist_ok=True)
    persisted_files: list[PersistedObservationFile] = []

    for filename in SOURCE_FILE_NAMES:
        output_path = feed_dir / filename
        existing_records = _load_existing_records(output_path)
        existing_ids = {_stable_record_id(record) for record in existing_records}
        incoming_records = incoming_payloads[filename]
        appended: list[dict[str, Any]] = []

        for record in incoming_records:
            annotated = _annotate_record(record, report_date=report_date)
            record_id = _stable_record_id(annotated)
            if record_id in existing_ids:
                continue
            existing_ids.add(record_id)
            appended.append(annotated)

        combined = existing_records + appended
        output_path.write_text(json.dumps(combined, indent=2), encoding="utf-8")
        persisted_files.append(
            PersistedObservationFile(
                filename=filename,
                incoming_records=len(incoming_records),
                existing_records=len(existing_records),
                appended_records=len(appended),
                total_records=len(combined),
                path=str(output_path),
            )
        )

    return DailyObservationSourceFeedReport(
        passed=True,
        feed_version=FEED_VERSION,
        incoming_dir=str(incoming_dir),
        feed_dir=str(feed_dir),
        report_date=report_date,
        files=persisted_files,
    )


def render_daily_observation_source_feed_markdown(report: DailyObservationSourceFeedReport) -> str:
    lines = [
        "# Daily Observation Source Feed",
        "",
        f"Status: **{'PASS' if report.passed else 'FAIL'}**",
        f"Feed version: `{report.feed_version}`",
        f"Report date: **{report.report_date}**",
        f"Incoming dir: `{report.incoming_dir}`",
        f"Feed dir: `{report.feed_dir}`",
        "",
        "## Files",
        "",
        "| File | Incoming | Existing | Appended | Total | Path |",
        "|---|---:|---:|---:|---:|---|",
    ]
    for item in report.files:
        lines.append(
            f"| `{item.filename}` | {item.incoming_records} | {item.existing_records} | "
            f"{item.appended_records} | {item.total_records} | `{item.path}` |"
        )
    lines.extend(["", "## Errors", ""])
    if report.errors:
        for error in report.errors:
            lines.append(f"- {error}")
    else:
        lines.append("- none")
    return "\n".join(lines).rstrip() + "\n"


def write_daily_observation_source_feed_report(
    report: DailyObservationSourceFeedReport,
    *,
    json_path: Path,
    markdown_path: Path,
) -> None:
    json_path.parent.mkdir(parents=True, exist_ok=True)
    markdown_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(report.to_dict(), indent=2), encoding="utf-8")
    markdown_path.write_text(render_daily_observation_source_feed_markdown(report), encoding="utf-8")


def _load_existing_records(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []
    if not isinstance(payload, list):
        return []
    return [item for item in payload if isinstance(item, dict)]


def _annotate_record(record: dict[str, Any], *, report_date: str) -> dict[str, Any]:
    annotated = dict(record)
    annotated.setdefault("source", "daily_observation_source_feed")
    annotated["feed_version"] = FEED_VERSION
    annotated["feed_report_date"] = report_date
    return annotated


def _stable_record_id(record: dict[str, Any]) -> str:
    comparable = {key: value for key, value in record.items() if key not in {"feed_version", "feed_report_date"}}
    raw = json.dumps(comparable, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()
