from src.runtime.runtime_state import RuntimeState


def test_runtime_state_history_is_bounded() -> None:
    state = RuntimeState(history_maxlen=3)

    for index in range(5):
        state.update({"decision_id": index})

    assert state.cycle_count == 5
    assert len(state.history) == 3
    assert [item["cycle"] for item in state.history] == [3, 4, 5]
    assert state.snapshot()["history_size"] == 3
    assert state.snapshot()["history_maxlen"] == 3


def test_runtime_state_minimum_history_size_is_one() -> None:
    state = RuntimeState(history_maxlen=0)

    state.update({"decision_id": 1})
    state.update({"decision_id": 2})

    assert len(state.history) == 1
    assert list(state.history)[0]["cycle"] == 2
