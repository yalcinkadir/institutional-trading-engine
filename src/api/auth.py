from __future__ import annotations

import os

from fastapi import Header, HTTPException


API_KEY_ENV = "INSTITUTIONAL_API_KEY"


def validate_api_key(x_api_key: str | None = Header(default=None)) -> None:
    expected = os.getenv(API_KEY_ENV)

    if not expected:
        return

    if x_api_key != expected:
        raise HTTPException(status_code=401, detail="Invalid API key")
