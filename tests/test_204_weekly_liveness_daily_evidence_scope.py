from __future__ import annotations

from pathlib import Path

from scripts.validate_scheduled_report_liveness import (
    REPORT_LIVENESS_BLOCKED,
    REPORT_LIVENESS_OK,
    STATUS_BLOCKED,
    STATUS_PASSED,
    build_scheduled_report_liveness_artifact,
)


def _write_market_family_outputs_without_daily_evidence(root: Path, day: str) -> None:
    files = {
        f"reports/signals/{day}-signals.json": "{}\n",
        f"reports/premarket/{day}-premarket.md": "# premarket\n",
        f"reports/intraday/{day}-intraday.md": "# intraday\n",
        f"reports/postmarket/{day}-postmarket.md": "# postmarket\n",
    }

    for relative_path, content in files.items():
        path = root / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")


def test_204_weekly_liveness_does_not_block_on_absent_daily_evidence(tmp_path: Path) -> None:
    """Weekly reports must not overwrite Paper Observation liveness as blocked.

    #204 was observed with report_type=weekly and daily_evidence_stale_or_missing:2.
    Weekly reports are scheduled-report evidence, but they are not the productive
    daily Paper Observation cycle. Missing reports/daily_evidence/*.json must
    remain visible in freshness evidence, but it must not block a weekly report
    liveness result.
    """

    _write_market_family_outputs_without_daily_evidence(tmp_path, "2026-06-12")

    report_file = tmp_path / "reports/weekly/2026-W24-weekly.md"
    latest_file = tmp_path / "reports/generated/weekly-report.md"

    report_file.parent.mkdir(parents=True, exist_ok=True)
    latest_file.parent.mkdir(parents=True, exist_ok=True)

    report_file.write_text("# weekly\n", encoding="utf-8")
    latest_file.write_text("# weekly\n", encoding="utf-8")

    result = build_scheduled_report_liveness_artifact(
        report_type="weekly",
        report_file=report_file,
        latest_file=latest_file,
        signals_file=None,
        paper_health_file=None,
        run_date="2026-06-13",
        report_root=tmp_path,
    )

    assert result.valid is True
    assert result.errors == ()
    assert result.artifact["scheduled_report_status"] == STATUS_PASSED
    assert result.artifact["report_liveness_status"] == REPORT_LIVENESS_OK
    assert result.artifact["productive_report_cycle"] is True

    assert result.artifact["freshness_by_family"]["daily_evidence"]["freshness_status"] == REPORT_LIVENESS_BLOCKED
    assert "daily_evidence" not in result.artifact["required_freshness_families"]


def test_204_market_liveness_still_blocks_on_absent_daily_evidence(tmp_path: Path) -> None:
    """Market report liveness still requires productive Daily Evidence."""

    _write_market_family_outputs_without_daily_evidence(tmp_path, "2026-06-12")

    report_file = tmp_path / "reports/postmarket/2026-06-13-postmarket.md"
    latest_file = tmp_path / "reports/generated/postmarket-report.md"
    signals_file = tmp_path / "reports/signals/latest-signals.json"
    paper_health_file = tmp_path / "reports/validation/latest-paper-observation-health.json"

    for path, content in (
        (report_file, "# postmarket\n"),
        (latest_file, "# postmarket\n"),
        (signals_file, "{}\n"),
        (paper_health_file, "{}\n"),
    ):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    result = build_scheduled_report_liveness_artifact(
        report_type="postmarket",
        report_file=report_file,
        latest_file=latest_file,
        signals_file=signals_file,
        paper_health_file=paper_health_file,
        run_date="2026-06-13",
        report_root=tmp_path,
    )

    assert result.valid is False
    assert result.artifact["scheduled_report_status"] == STATUS_BLOCKED
    assert "daily_evidence_stale_or_missing:2" in result.errors
    assert "daily_evidence" in result.artifact["required_freshness_families"]