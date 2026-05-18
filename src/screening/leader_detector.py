from __future__ import annotations


LEADER_THRESHOLD = 75


def detect_leaders(assets: list[dict]) -> list[dict]:
    return [
        asset
        for asset in assets
        if asset.get("score", 0) >= LEADER_THRESHOLD
    ]
