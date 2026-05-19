from src.api.health_api import health_response


def test_health_response():
    response = health_response()

    assert response["runtime"]["status"] == "ok"
    assert response["healthcheck"]["status"] == "healthy"
