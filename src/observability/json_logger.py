from __future__ import annotations

import json
import logging
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


LOG_PATH = Path("logs/runtime.jsonl")


class JsonLineFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, Any] = {
            "timestamp_utc": datetime.now(UTC).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        return json.dumps(payload)


def build_json_logger(name: str) -> logging.Logger:
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        handler = logging.FileHandler(LOG_PATH, encoding="utf-8")
        handler.setFormatter(JsonLineFormatter())
        logger.addHandler(handler)

    logger.propagate = False

    return logger
