from src.runtime.in_memory_state_cache import InMemoryStateCache


def test_in_memory_state_cache():
    cache = InMemoryStateCache()

    cache.set("latest_regime", "risk_on")

    assert cache.get("latest_regime") == "risk_on"

    snapshot = cache.snapshot()

    assert snapshot["latest_regime"] == "risk_on"
