from src.monitoring.anomaly_alerts import detect_operational_anomalies
from src.monitoring.telemetry import TelemetryTracker
from src.storage.sqlite_store import SQLiteStore


def test_sqlite_store(tmp_path):
    db_path = tmp_path / "test.db"
    store = SQLiteStore(db_path=db_path)

    store.insert_report(
        report_type="premarket",
        created_at="2026-05-18T10:00:00Z",
        path="reports/premarket/report.md",
        quality_score=88,
    )

    assert db_path.exists()


def test_telemetry_tracker(tmp_path):
    db_path = tmp_path / "telemetry.db"
    store = SQLiteStore(db_path=db_path)

    tracker = TelemetryTracker(store=store)
    tracker.track_metric(
        metric="report_generation_time_ms",
        value=1500,
    )

    assert db_path.exists()


def test_anomaly_alerts():
    result = detect_operational_anomalies(
        {
            "latency_ms": 6000,
            "failure_rate_percent": 15,
            "cache_hit_rate_percent": 20,
        }
    )

    assert result["severity"] == "CRITICAL"
    assert len(result["alerts"]) >= 3
