from fastapi import HTTPException

from src.api.rate_limit import SimpleRateLimiter


def test_rate_limit_blocks_after_threshold():
    limiter = SimpleRateLimiter(limit=2, window_seconds=60)

    limiter.check("client")
    limiter.check("client")

    blocked = False

    try:
        limiter.check("client")
    except HTTPException as exc:
        blocked = exc.status_code == 429

    assert blocked is True
