from src.observability.healthcheck import build_healthcheck


def test_healthcheck_status():
    result = build_healthcheck()

    assert result["status"] == "healthy"
    assert "components" in result
