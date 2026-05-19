from src.runtime.event_bus import EventBus
from src.storage.sqlite_runtime_store import SQLiteRuntimeStore


def test_event_bus_publishes_event():
    received = {"called": False}

    def handler(payload: dict):
        received["called"] = payload["value"] == 1

    bus = EventBus()

    bus.subscribe("test_event", handler)
    bus.publish("test_event", {"value": 1})

    assert received["called"] is True


def test_sqlite_runtime_store_inserts_event():
    store = SQLiteRuntimeStore()

    before = store.count_events()

    store.insert_event(
        event_type="runtime_test",
        payload="{}",
        created_at="2026-05-19T00:00:00Z",
    )

    after = store.count_events()

    assert after >= before + 1
