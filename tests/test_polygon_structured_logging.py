import json
import logging

import pytest

from scripts import build_polygon_universe, download_polygon_daily_bars
from src.observability.structured_logging import StructuredLogEvent, emit_structured_log


class FakeResponse:
    def __init__(self, payload, status_code=200):
        self._payload = payload
        self.status_code = status_code

    def raise_for_status(self):
        if self.status_code >= 400:
            raise RuntimeError(f"status {self.status_code}")

    def json(self):
        return self._payload


class FakeSession:
    def __init__(self, response):
        self.response = response

    def get(self, *args, **kwargs):
        return self.response


def test_structured_log_event_serializes_required_fields() -> None:
    event = StructuredLogEvent(
        event="polygon_rate_limit",
        level="WARNING",
        component="polygon_daily_bars_downloader",
        message="Rate limit reached",
        fields={"symbol": "SPY", "status_code": 429},
    )

    payload = json.loads(event.to_json())

    assert payload["level"] == "WARNING"
    assert payload["component"] == "polygon_daily_bars_downloader"
    assert payload["event"] == "polygon_rate_limit"
    assert payload["symbol"] == "SPY"
    assert payload["status_code"] == 429
    assert "timestamp" in payload


def test_emit_structured_log_writes_json_message(caplog) -> None:
    logger = logging.getLogger("test.polygon.structured")

    with caplog.at_level(logging.INFO, logger="test.polygon.structured"):
        emit_structured_log(
            logger,
            event="polygon_bars_response",
            component="polygon_daily_bars_downloader",
            symbol="QQQ",
            bar_count=250,
        )

    assert len(caplog.records) == 1
    payload = json.loads(caplog.records[0].message)
    assert payload["event"] == "polygon_bars_response"
    assert payload["symbol"] == "QQQ"
    assert payload["bar_count"] == 250


def test_polygon_universe_rate_limit_emits_structured_log(caplog) -> None:
    session = FakeSession(FakeResponse({}, status_code=429))

    with caplog.at_level(logging.WARNING, logger="polygon.universe"):
        with pytest.raises(RuntimeError, match="rate limit reached"):
            build_polygon_universe._fetch_json(session, "https://example.test", {}, "token")

    payload = json.loads(caplog.records[0].message)
    assert payload["event"] == "polygon_rate_limit"
    assert payload["component"] == "polygon_universe_builder"
    assert payload["status_code"] == 429


def test_polygon_bars_response_emits_bar_count(caplog) -> None:
    session = FakeSession(FakeResponse({"results": [{"t": 1704067200000}]}))

    with caplog.at_level(logging.INFO, logger="polygon.daily_bars"):
        bars = download_polygon_daily_bars.fetch_bars(
            session,
            "SPY",
            from_date="2024-01-01",
            to_date="2024-01-02",
            token="token",
        )

    assert len(bars) == 1
    events = [json.loads(record.message)["event"] for record in caplog.records]
    assert "polygon_bars_request" in events
    assert "polygon_bars_response" in events
    response_payload = [json.loads(record.message) for record in caplog.records if "polygon_bars_response" in record.message][0]
    assert response_payload["symbol"] == "SPY"
    assert response_payload["bar_count"] == 1
