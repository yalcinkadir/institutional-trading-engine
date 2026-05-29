import json
import subprocess
import sys
from pathlib import Path

from src.config.paper_observation_universe import CORE_OBSERVATION_UNIVERSE, MACRO_CFD_OBSERVATION_UNIVERSE
from src.validation.paper_observation_asset_timeline import (
    PaperObservationAssetEvent,
    PaperObservationAssetTimeline,
    build_asset_timeline_template,
    render_asset_timeline_markdown,
    validate_asset_timeline,
    write_asset_timeline,
)

SCRIPT = Path("scripts/generate_paper_observation_asset_timeline.py")


def test_asset_timeline_template_contains_all_core_and_macro_assets() -> None:
    timeline = build_asset_timeline_template(
        report_date="2026-05-29",
        event_time_utc="2026-05-29T21:30:00+00:00",
    )

    assert [event.symbol for event in timeline.events if event.group == "core"] == list(CORE_OBSERVATION_UNIVERSE)
    assert [event.symbol for event in timeline.events if event.group == "macro_cfd_watch"] == list(
        MACRO_CFD_OBSERVATION_UNIVERSE
    )
    assert all(event.status == "STARTED" for event in timeline.events)
    assert validate_asset_timeline(timeline) == []


def test_asset_timeline_validation_fails_when_core_asset_is_missing() -> None:
    timeline = PaperObservationAssetTimeline(
        report_date="2026-05-29",
        universe_version="test",
        events=[
            PaperObservationAssetEvent(
                symbol="QQQ",
                status="STARTED",
                event_time_utc="2026-05-29T21:30:00+00:00",
                report_date="2026-05-29",
                group="core",
            )
        ],
    )

    issues = validate_asset_timeline(timeline)

    assert any("missing core symbols" in issue for issue in issues)


def test_asset_timeline_markdown_is_visible_and_safe() -> None:
    timeline = build_asset_timeline_template(
        report_date="2026-05-29",
        event_time_utc="2026-05-29T21:30:00+00:00",
    )

    markdown = render_asset_timeline_markdown(timeline)

    assert "# B1.1 Paper Observation Asset Timeline" in markdown
    assert "| Time UTC | Symbol | Group | Status | Note |" in markdown
    assert "`AAPL`" in markdown
    assert "`NDQ100`" in markdown
    assert "does not authorize live trading" in markdown


def test_write_asset_timeline_creates_json_and_markdown(tmp_path: Path) -> None:
    timeline = build_asset_timeline_template(
        report_date="2026-05-29",
        event_time_utc="2026-05-29T21:30:00+00:00",
    )
    json_path = tmp_path / "timeline.json"
    markdown_path = tmp_path / "timeline.md"

    issues = write_asset_timeline(timeline, json_path=json_path, markdown_path=markdown_path)

    assert issues == []
    assert json.loads(json_path.read_text(encoding="utf-8"))["report_date"] == "2026-05-29"
    assert "AAPL" in markdown_path.read_text(encoding="utf-8")


def test_asset_timeline_cli_generates_artifacts(tmp_path: Path) -> None:
    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--report-date",
            "2026-05-29",
            "--event-time-utc",
            "2026-05-29T21:30:00+00:00",
            "--output-dir",
            str(tmp_path),
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    assert "Paper observation asset timeline status: PASS" in result.stdout
    assert "Assets logged: 14" in result.stdout
    assert (tmp_path / "paper_observation_asset_timeline.json").exists()
    assert (tmp_path / "paper_observation_asset_timeline.md").exists()
