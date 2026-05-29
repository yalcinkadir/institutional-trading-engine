import asyncio

import pytest

from src.runtime.runtime_loop import RuntimeLoop, RuntimeLoopError
from src.runtime.runtime_state import RuntimeState


def test_runtime_loop_continues_after_transient_provider_error(monkeypatch) -> None:
    loop = RuntimeLoop()
    state = RuntimeState()
    calls = {"count": 0}

    async def provider() -> dict:
        calls["count"] += 1
        if calls["count"] == 1:
            raise RuntimeError("temporary provider failure")
        return {"decision_id": calls["count"]}

    monkeypatch.setattr("src.runtime.runtime_loop.runtime_state", state)

    asyncio.run(
        loop.start(
            provider,
            cycle_interval_seconds=0,
            max_cycles=1,
            max_consecutive_errors=3,
        )
    )

    assert calls["count"] == 2
    assert state.cycle_count == 1
    assert state.latest_decision == {"decision_id": 2}


def test_runtime_loop_stops_after_max_consecutive_errors(monkeypatch) -> None:
    loop = RuntimeLoop()
    state = RuntimeState()

    async def provider() -> dict:
        raise RuntimeError("persistent provider failure")

    monkeypatch.setattr("src.runtime.runtime_loop.runtime_state", state)

    with pytest.raises(RuntimeLoopError, match="2 consecutive"):
        asyncio.run(
            loop.start(
                provider,
                cycle_interval_seconds=0,
                max_cycles=1,
                max_consecutive_errors=2,
            )
        )

    assert state.cycle_count == 0
