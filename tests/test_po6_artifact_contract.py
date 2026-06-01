from __future__ import annotations

from src.operations.daily_observation_record_artifact_contract import build_daily_observation_record_path


def test_po6_builds_expected_record_file_name() -> None:
    assert str(build_daily_observation_record_path("2026-06-01")) == "reports/daily_observation_records/2026-06-01.json"
