from src.storage.postgres_store import PostgresStore


def test_postgres_backend_detection():
    store = PostgresStore()

    assert store.backend in ["postgres", "fallback"]


def test_postgres_connection_url():
    store = PostgresStore()

    url = store.connection_url()

    assert url.startswith("postgresql://")
