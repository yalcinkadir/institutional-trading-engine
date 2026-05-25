from __future__ import annotations

import json
import os
import time
from contextlib import contextmanager
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterator

DEFAULT_POLYGON_CACHE_DIR = Path(".cache/polygon")
DEFAULT_LOCK_TIMEOUT_SECONDS = 30.0
DEFAULT_STALE_LOCK_SECONDS = 300.0


class PolygonCacheLockTimeout(TimeoutError):
    """Raised when a Polygon cache lock cannot be acquired in time."""


@dataclass(frozen=True)
class PolygonCacheLockInfo:
    lock_path: Path
    acquired: bool
    waited_seconds: float
    stale_lock_removed: bool = False

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["lock_path"] = str(self.lock_path)
        return payload


@dataclass(frozen=True)
class PolygonCacheWriteResult:
    path: Path
    bytes_written: int
    lock: PolygonCacheLockInfo
    atomic: bool = True

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["path"] = str(self.path)
        payload["lock"] = self.lock.to_dict()
        return payload


@contextmanager
def polygon_cache_lock(
    target_path: Path,
    *,
    timeout_seconds: float = DEFAULT_LOCK_TIMEOUT_SECONDS,
    stale_after_seconds: float = DEFAULT_STALE_LOCK_SECONDS,
    poll_seconds: float = 0.05,
) -> Iterator[PolygonCacheLockInfo]:
    """Acquire an exclusive file lock beside a Polygon cache target.

    The lock is created with `O_EXCL`, so two processes cannot acquire the same
    lock simultaneously. Stale lock files can be removed after the configured
    timeout to protect long-running data jobs from orphaned locks.
    """

    target_path = Path(target_path)
    lock_path = target_path.with_suffix(target_path.suffix + ".lock")
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    start = time.monotonic()
    stale_lock_removed = False

    while True:
        try:
            fd = os.open(str(lock_path), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                handle.write(
                    json.dumps(
                        {
                            "pid": os.getpid(),
                            "target_path": str(target_path),
                            "created_at": time.time(),
                        },
                        sort_keys=True,
                    )
                )
            waited = time.monotonic() - start
            info = PolygonCacheLockInfo(
                lock_path=lock_path,
                acquired=True,
                waited_seconds=round(waited, 6),
                stale_lock_removed=stale_lock_removed,
            )
            try:
                yield info
            finally:
                _remove_lock(lock_path)
            return
        except FileExistsError:
            if _is_stale_lock(lock_path, stale_after_seconds=stale_after_seconds):
                _remove_lock(lock_path)
                stale_lock_removed = True
                continue
            waited = time.monotonic() - start
            if waited >= timeout_seconds:
                raise PolygonCacheLockTimeout(
                    f"Timed out waiting for Polygon cache lock: {lock_path}"
                )
            time.sleep(max(0.001, poll_seconds))


def write_polygon_cache_text(
    path: Path,
    text: str,
    *,
    timeout_seconds: float = DEFAULT_LOCK_TIMEOUT_SECONDS,
    stale_after_seconds: float = DEFAULT_STALE_LOCK_SECONDS,
) -> PolygonCacheWriteResult:
    """Write cache text atomically under a lock."""

    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    encoded = text.encode("utf-8")
    with polygon_cache_lock(
        path,
        timeout_seconds=timeout_seconds,
        stale_after_seconds=stale_after_seconds,
    ) as lock_info:
        temp_path = path.with_suffix(path.suffix + f".tmp.{os.getpid()}")
        try:
            temp_path.write_bytes(encoded)
            os.replace(temp_path, path)
        finally:
            if temp_path.exists():
                temp_path.unlink()
    return PolygonCacheWriteResult(path=path, bytes_written=len(encoded), lock=lock_info)


def write_polygon_cache_json(
    path: Path,
    payload: Any,
    *,
    timeout_seconds: float = DEFAULT_LOCK_TIMEOUT_SECONDS,
    stale_after_seconds: float = DEFAULT_STALE_LOCK_SECONDS,
    indent: int = 2,
) -> PolygonCacheWriteResult:
    text = json.dumps(payload, indent=indent, sort_keys=True, default=str)
    return write_polygon_cache_text(
        path,
        text,
        timeout_seconds=timeout_seconds,
        stale_after_seconds=stale_after_seconds,
    )


def read_polygon_cache_json(path: Path) -> Any | None:
    path = Path(path)
    if not path.exists():
        return None
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def polygon_cache_path(key: str, *, cache_dir: Path = DEFAULT_POLYGON_CACHE_DIR, suffix: str = ".json") -> Path:
    safe_key = "".join(character if character.isalnum() or character in {"-", "_", "."} else "_" for character in key)
    if not safe_key:
        raise ValueError("cache key must not be empty")
    if not suffix.startswith("."):
        suffix = f".{suffix}"
    return Path(cache_dir) / f"{safe_key}{suffix}"


def _is_stale_lock(lock_path: Path, *, stale_after_seconds: float) -> bool:
    if stale_after_seconds <= 0:
        return False
    try:
        age = time.time() - lock_path.stat().st_mtime
    except FileNotFoundError:
        return False
    return age >= stale_after_seconds


def _remove_lock(lock_path: Path) -> None:
    try:
        lock_path.unlink()
    except FileNotFoundError:
        return
