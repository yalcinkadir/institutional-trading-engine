"""Report helpers for Entry / Stop / Exit feedback."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable

from src.feedback.entry_stop_exit_feedback import (
    EntryStopExitFeedbackReport,
    aggregate_entry_stop_exit_feedback,
    format_entry_stop_exit_feedback_markdown,
)


def build_entry_stop_exit_feedback_report(
    records: Iterable[dict[str, Any]],
) -> EntryStopExitFeedbackReport:
    """Build a feedback report from historical outcome records."""
    return aggregate_entry_stop_exit_feedback(records)


def save_entry_stop_exit_feedback_report(
    records: Iterable[dict[str, Any]],
    *,
    output_dir: Path,
    stem: str = "entry-stop-exit-feedback",
) -> tuple[Path, Path]:
    """Persist feedback report as JSON and Markdown."""
    output_dir.mkdir(parents=True, exist_ok=True)
    report = build_entry_stop_exit_feedback_report(records)

    json_path = output_dir / f"{stem}.json"
    markdown_path = output_dir / f"{stem}.md"

    json_path.write_text(json.dumps(report.to_dict(), indent=2), encoding="utf-8")
    markdown_path.write_text(format_entry_stop_exit_feedback_markdown(report), encoding="utf-8")

    return json_path, markdown_path
