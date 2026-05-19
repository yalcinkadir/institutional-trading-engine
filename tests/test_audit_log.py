from pathlib import Path

from src.api.audit_log import AuditLogger


def test_audit_log_writes_file(tmp_path: Path):
    logger = AuditLogger()

    logger.log("test_event", "details")

    log_path = Path("logs/audit.log")

    assert log_path.exists()
