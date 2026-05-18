from datetime import UTC, datetime, timedelta
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.outcome_pipeline import build_expectancy_summary, record_decisions_from_report_payload, update_outcomes  # noqa: E402
from src.outcome_tracking import read_decision_records  # noqa: E402

DAY_MS = 86400000


def _bars(start=100.0, drift=1.0, count=30):
    bars = []
    close = start
    start_dt = datetime.now(UTC).replace(hour=0, minute=0, second=0, microsecond=0)
    start_ms = int(start_dt.timestamp() * 1000)

    for index in range(count):
        close += drift
        bars.append({"t": start_ms + (index * DAY_MS), "c": round(close, 2), "h": round(close + 2, 2), "l": round(close - 2, 2)})

    return bars


def _payload():
    return {
        "decision_report": {
            "market_state": "low_vol_bull",
            "decisions": [
                {
                    "symbol": "NVDA",
                    "decision": "approved",
                    "risk_tier": "tier_1",
                    "setup_type": "momentum_breakout",
                    "position_size_multiplier": 1.0,
                    "setup_score": 88,
                    "regime_alignment": 0.9,
                    "asymmetry_score": 0.7,
                    "data_confidence": 0.95,
                    "blocked_reasons": [],
                    "notes": ["strong_trend"],
                }
            ],
        }
    }


def test_record_decisions_from_payload(tmp_path):
    path = tmp_path / "decisions.csv"
    record_decisions_from_report_payload(_payload(), path=path, price_lookup={"NVDA": 120.0})
    rows = read_decision_records(path)
    assert len(rows) == 1
    assert rows[0]["symbol"] == "NVDA"


def test_update_outcomes_adds_returns_and_mfe_mae(tmp_path):
    path = tmp_path / "decisions.csv"
    record_decisions_from_report_payload(_payload(), path=path, price_lookup={"NVDA": 100.0})
    update_outcomes(path=path, bars_by_symbol={"NVDA": _bars()})
    rows = read_decision_records(path)
    assert rows[0]["result_5d"] not in {None, "", "None"}
    assert rows[0]["mfe"] not in {None, "", "None"}
    assert rows[0]["mae"] not in {None, "", "None"}


def test_expectancy_summary_builds_profiles(tmp_path):
    path = tmp_path / "decisions.csv"
    for _ in range(6):
        record_decisions_from_report_payload(_payload(), path=path, price_lookup={"NVDA": 100.0})
    update_outcomes(path=path, bars_by_symbol={"NVDA": _bars()})
    summary = build_expectancy_summary(path)
    assert len(summary["setup_profiles"]) >= 1
