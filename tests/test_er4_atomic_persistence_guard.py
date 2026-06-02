from __future__ import annotations

import json
from pathlib import Path

from src.persistence.atomic_write import write_json_atomic, write_text_atomic
from src.runtime.portfolio_state import PortfolioState, PortfolioStateStore


def test_er4_write_json_atomic_replaces_destination_without_leaving_temp_file(tmp_path: Path) -> None:
    destination = tmp_path / "state" / "evidence.json"

    saved_path = write_json_atomic(destination, {"z": 1, "a": 2}, fsync_file=False)

    assert saved_path == destination
    assert json.loads(destination.read_text(encoding="utf-8")) == {"a": 2, "z": 1}
    assert list(destination.parent.glob("*.tmp")) == []


def test_er4_write_text_atomic_preserves_existing_file_when_replace_fails(monkeypatch, tmp_path: Path) -> None:
    destination = tmp_path / "state.json"
    destination.write_text("original\n", encoding="utf-8")

    def fail_replace(src: Path, dst: Path) -> None:
        raise RuntimeError("simulated replace failure")

    monkeypatch.setattr("src.persistence.atomic_write.os.replace", fail_replace)

    try:
        write_text_atomic(destination, "new\n", fsync_file=False)
    except RuntimeError as exc:
        assert "simulated replace failure" in str(exc)
    else:
        raise AssertionError("expected simulated replace failure")

    assert destination.read_text(encoding="utf-8") == "original\n"
    assert list(tmp_path.glob("*.tmp")) == []


def test_er4_portfolio_state_store_uses_central_atomic_json_writer(monkeypatch, tmp_path: Path) -> None:
    destination = tmp_path / "portfolio_state.json"
    calls: list[tuple[Path, dict]] = []

    def fake_write_json_atomic(path: Path, payload: dict, **kwargs) -> Path:
        calls.append((Path(path), payload))
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        Path(path).write_text(json.dumps(payload), encoding="utf-8")
        return Path(path)

    monkeypatch.setattr("src.runtime.portfolio_state.write_json_atomic", fake_write_json_atomic)

    state = PortfolioState(
        equity_start=10000.0,
        equity_current=9800.0,
        drawdown_percent=-2.0,
        daily_loss_percent=-0.5,
        open_positions=[],
        updated_at="2026-06-02T10:00:00+00:00",
    )

    saved_path = PortfolioStateStore(destination).save(state)

    assert saved_path == destination
    assert calls == [(destination, state.to_dict())]
    assert json.loads(destination.read_text(encoding="utf-8"))["drawdown_percent"] == -2.0
