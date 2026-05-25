# Polygon Cache Locking

Polygon cache writes now use file locks and atomic replacement.

## Implementation

```text
src/data/polygon_cache.py
tests/test_polygon_cache.py
```

## Why this exists

Large Polygon data runs can overlap locally or in CI. If two processes write the same cache file at the same time, the result can be partially written or corrupted.

This module prevents that by combining:

1. exclusive lock-file creation
2. timeout handling
3. stale lock cleanup
4. temporary-file write
5. atomic `os.replace` into the target path

## Lock behavior

For a target file such as:

```text
.cache/polygon/SPY.json
```

The lock file is:

```text
.cache/polygon/SPY.json.lock
```

The lock is created with exclusive create semantics. If another process already holds it, the caller waits until timeout. Stale locks can be removed after the configured stale-lock threshold.

## Public API

```text
polygon_cache_lock
write_polygon_cache_text
write_polygon_cache_json
read_polygon_cache_json
polygon_cache_path
```

## Operational rule

Any new Polygon cache write should use `write_polygon_cache_text` or `write_polygon_cache_json`. Do not write directly with `Path.write_text`, `Path.write_bytes` or plain `open(..., "w")` for cache files.

## Failure mode

If a fresh lock cannot be acquired before timeout, the module raises:

```text
PolygonCacheLockTimeout
```

This is intentional. Cache corruption is worse than failing fast.
