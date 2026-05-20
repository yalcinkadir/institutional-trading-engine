import json
from pathlib import Path

from src.scoring.adjustment_history import (
    append_scoring_adjustments,
    build_scoring_adjustment_records,
)


def _decision_report(score_delta=4.0, size_multiplier=1.05):
    return {
        "market_state": "low_vol_bull",
        "decisions": [
            {
                "symbol": "NVDA",
                "setup_type": "momentum_breakout",
                "decision": "approved",
                "risk_tier": "tier_1",
                "base_setup_score": 82,
                "setup_score": 86,
                "base_position_size_multiplier": 1.0,
                "position_size_multiplier": 1.05,
                "entry_type": "break_above",
                "expectancy": {
                    "profile_key": "regime_setup_entry::low_vol_bull::momentum_breakout::break_above",
                    "source": "regime_setup_entry",
                    "sample_size": 6,
                    "win_rate": 0.67,
                    "expectancy": 2.0,
                    "score_delta": score_delta,
                    "size_multiplier": size_multiplier,
                    "recommendation": "maintain_or_slightly_increase",
                    "reason": "positive_expectancy",
                    "entry_type_assumption": "break_above",
                },
            }
        ],
    }


def test_build_scoring_adjustment_records_extracts_auditable_fields():
    records = build_scoring_adjustment_records(
        decision_report=_decision_report(),
        report_type="postmarket",
        run_id="run-1",
        timestamp_utc="2026-05-20T21:00:00+00:00",
    )

    assert len(records) == 1
    record = records[0]
    assert record["symbol"] == "NVDA"
    assert record["profile_key"] == "regime_setup_entry::low_vol_bull::momentum_breakout::break_above"
    assert record["base_score"] == 82
    assert record["score_delta"] == 4.0
    assert record["final_score"] == 86
    assert record["base_size"] == 1.0
    assert record["size_multiplier"] == 1.05
    assert record["final_size"] == 1.05


def test_build_scoring_adjustment_records_skips_noop_adjustments():
    report = _decision_report(score_delta=0.0, size_multiplier=1.0)

    records = build_scoring_adjustment_records(
        decision_report=report,
        report_type="premarket",
        run_id="run-1",
    )

    assert records == []


def test_append_scoring_adjustments_writes_and_dedupes(tmp_path: Path):
    output = tmp_path / "scoring_adjustment_history.json"

    append_scoring_adjustments(
        decision_report=_decision_report(),
        report_type="postmarket",
        output_path=output,
        run_id="run-1",
        timestamp_utc="2026-05-20T21:00:00+00:00",
    )
    append_scoring_adjustments(
        decision_report=_decision_report(),
        report_type="postmarket",
        output_path=output,
        run_id="run-1",
        timestamp_utc="2026-05-20T21:00:00+00:00",
    )

    data = json.loads(output.read_text(encoding="utf-8"))
    assert len(data) == 1
    assert data[0]["run_id"] == "run-1"


def test_append_scoring_adjustments_keeps_max_records(tmp_path: Path):
    output = tmp_path / "scoring_adjustment_history.json"

    for i in range(5):
        append_scoring_adjustments(
            decision_report=_decision_report(score_delta=4.0 + i),
            report_type="postmarket",
            output_path=output,
            run_id=f"run-{i}",
            max_records=3,
        )

    data = json.loads(output.read_text(encoding="utf-8"))
    assert len(data) == 3
    assert [item["run_id"] for item in data] == ["run-2", "run-3", "run-4"]
