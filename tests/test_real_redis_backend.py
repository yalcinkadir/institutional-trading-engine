from src.cache.redis_cache import RedisCache


def test_cache_backend_is_available():
    cache = RedisCache()

    assert cache.backend in ["memory", "redis"]


def test_cache_set_and_get():
    cache = RedisCache()

    cache.set("spy", {"price": 500})

    result = cache.get("spy")

    assert result["price"] == 500
