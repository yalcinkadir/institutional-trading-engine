import json
import os
import time
from pathlib import Path

import pytest

from src.data.polygon_cache import (
    PolygonCacheLockTimeout,
    polygon_cache_lock,
    polygon_cache_path,
    read_polygon_cache_json,
    write_polygon_cache_json,
    write_polygon_cache_text,
)


def test_write_polygon_cache_text_is_atomic_and_removes_lock(tmp_path: Path) -> None:
    target = tmp_path / ".cache" / "polygon" / "SPY.json"

    result = write_polygon_cache_text(target, '{"symbol":"SPY"}')

    assert target.read_text(encoding="utf-8") == '{"symbol":"SPY"}'
    assert result.path == target
    assert result.bytes_written == len('{"symbol":"SPY"}'.encode("utf-8"))
    assert result.atomic is True
    assert not target.with_suffix(".json.lock").exists()


def test_write_and_read_polygon_cache_json(tmp_path: Path) -> None:
    target = tmp_path / ".cache" / "polygon" / "QQQ.json"
    payload = {"symbol": "QQQ", "bars": [1, 2, 3]}

    write_polygon_cache_json(target, payload)

    assert read_polygon_cache_json(target) == payload


def test_polygon_cache_lock_times_out_when_existing_lock_is_fresh(tmp_path: Path) -> None:
    target = tmp_path / "IWM.json"
    lock = target.with_suffix(".json.lock")
    lock.write_text("locked", encoding="utf-8")

    with pytest.raises(PolygonCacheLockTimeout):
        with polygon_cache_lock(target, timeout_seconds=0.01, stale_after_seconds=300, poll_seconds=0.001):
            pass

    assert lock.exists()


def test_polygon_cache_lock_removes_stale_lock(tmp_path: Path) -> None:
    target = tmp_path / "DIA.json"
    lock = target.with_suffix(".json.lock")
    lock.write_text("stale", encoding="utf-8")
    stale_time = time.time() - 1000
    os.utime(lock, (stale_time, stale_time))

    with polygon_cache_lock(target, timeout_seconds=0.5, stale_after_seconds=1, poll_seconds=0.001) as info:
        assert info.acquired is True
        assert info.stale_lock_removed is True

    assert not lock.exists()


def test_polygon_cache_path_sanitizes_key(tmp_path: Path) -> None:
    path = polygon_cache_path("SPY/range?from=2024-01-01", cache_dir=tmp_path)

    assert path == tmp_path / "SPY_range_from_2024-01-01.json"


def test_polygon_cache_path_rejects_empty_key(tmp_path: Path) -> None:
    with pytest.raises(ValueError):
        polygon_cache_path("", cache_dir=tmp_path)


def test_cache_write_never_leaves_temp_file_after_success(tmp_path: Path) -> None:
    target = tmp_path / "bars.json"

    write_polygon_cache_json(target, {"ok": True})

    assert json.loads(target.read_text(encoding="utf-8")) == {"ok": True}
    assert list(tmp_path.glob("*.tmp.*")) == []
