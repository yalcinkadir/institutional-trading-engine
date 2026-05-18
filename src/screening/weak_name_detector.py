from __future__ import annotations


WEAK_THRESHOLD = 45


def detect_weak_names(assets: list[dict]) -> list[dict]:
    return [
        asset
        for asset in assets
        if asset.get("score", 100) <= WEAK_THRESHOLD
    ]
