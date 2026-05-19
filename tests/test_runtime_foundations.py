from src.cache.redis_cache import RedisCache
from src.storage.postgres_store import PostgresStore


def test_redis_cache_set_and_get():
    cache = RedisCache()

    cache.set("spy", {"price": 500})

    result = cache.get("spy")

    assert result["price"] == 500


def test_postgres_connection_url():
    store = PostgresStore()

    url = store.connection_url()

    assert url.startswith("postgresql://")
