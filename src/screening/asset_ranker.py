from __future__ import annotations


def rank_assets(assets: list[dict]) -> list[dict]:
    return sorted(
        assets,
        key=lambda asset: asset.get("score", 0),
        reverse=True,
    )
