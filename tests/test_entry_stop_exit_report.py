from __future__ import annotations

import json
from pathlib import Path

from src.feedback.entry_stop_exit_report import (
    build_entry_stop_exit_feedback_report,
    save_entry_stop_exit_feedback_report,
)


def test_build_entry_stop_exit_feedback_report() -> None:
    report = build_entry_stop_exit_feedback_report([
        {"entry_type": "breakout", "outcome": "TARGET_1_HIT"},
    ])

    assert report.total_records == 1
    assert report.overall.target_1_hits == 1


def test_save_entry_stop_exit_feedback_report(tmp_path: Path) -> None:
    json_path, markdown_path = save_entry_stop_exit_feedback_report(
        [
            {"entry_type": "breakout", "outcome": "TARGET_1_HIT"},
            {"entry_type": "breakout", "outcome": "STOP_HIT"},
        ],
        output_dir=tmp_path,
        stem="test-feedback",
    )

    assert json_path.exists()
    assert markdown_path.exists()

    payload = json.loads(json_path.read_text(encoding="utf-8"))
    markdown = markdown_path.read_text(encoding="utf-8")

    assert payload["total_records"] == 2
    assert payload["overall"]["entry_hits"] == 2
    assert "# Entry / Stop / Exit Feedback" in markdown
    assert "**breakout**" in markdown
