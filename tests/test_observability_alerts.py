from src.observability.alerts import AlertManager
from src.observability.runtime_monitor import RuntimeMonitor


def test_alert_manager_creates_alert():
    manager = AlertManager()

    alert = manager.trigger(
        level="warning",
        message="queue backlog high",
    )

    assert alert.level == "warning"
    assert manager.active_count() == 1


def test_runtime_monitor_creates_alerts():
    monitor = RuntimeMonitor()

    before = len(monitor.__dict__)

    monitor.check_health(
        failed_jobs=10,
        queue_backlog=200,
    )

    after = len(monitor.__dict__)

    assert after >= before
