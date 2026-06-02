"""Atomic file persistence helpers for governance and evidence artifacts."""

from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from typing import Any


def write_text_atomic(
    path: str | Path,
    content: str,
    *,
    encoding: str = "utf-8",
    fsync_file: bool = True,
) -> Path:
    """Write text via a temporary sibling file and atomic replacement."""

    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)

    tmp_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            "w",
            encoding=encoding,
            dir=destination.parent,
            prefix=f".{destination.name}.",
            suffix=".tmp",
            delete=False,
        ) as handle:
            tmp_path = Path(handle.name)
            handle.write(content)
            handle.flush()
            if fsync_file:
                os.fsync(handle.fileno())

        os.replace(tmp_path, destination)
        return destination
    except Exception:
        if tmp_path is not None:
            tmp_path.unlink(missing_ok=True)
        raise


def write_json_atomic(
    path: str | Path,
    payload: Any,
    *,
    indent: int = 2,
    sort_keys: bool = True,
    fsync_file: bool = True,
) -> Path:
    """Serialize JSON and persist it with atomic replacement."""

    content = json.dumps(payload, indent=indent, sort_keys=sort_keys) + "\n"
    return write_text_atomic(path, content, fsync_file=fsync_file)
