from __future__ import annotations

import csv
from pathlib import Path

import pytest

from scripts.build_polygon_universe import iter_tickers, write_universe
from scripts.download_polygon_daily_bars import bar_to_row, load_symbols, write_bars, write_manifest


class FakeResponse:
    def __init__(self, payload: dict, status_code: int = 200) -> None:
        self._payload = payload
        self.status_code = status_code

    def raise_for_status(self) -> None:
        if self.status_code >= 400:
            raise RuntimeError(f"status {self.status_code}")

    def json(self) -> dict:
        return self._payload


class FakeSession:
    def __init__(self, payloads: list[dict]) -> None:
        self.payloads = payloads
        self.params = {}
        self.calls = 0

    def get(self, *args, **kwargs):
        payload = self.payloads[self.calls]
        self.calls += 1
        return FakeResponse(payload)


def test_iter_tickers_follows_next_url() -> None:
    session = FakeSession(
        [
            {
                "results": [{"ticker": "AAA", "name": "A", "type": "CS", "primary_exchange": "XNYS"}],
                "next_url": "https://example.test/next",
            },
            {"results": [{"ticker": "BBB", "name": "B", "type": "ETF", "primary_exchange": "ARCX"}]},
        ]
    )

    symbols = [item["symbol"] for item in iter_tickers(session, market="stocks", sleep_seconds=0.0)]

    assert symbols == ["AAA", "BBB"]
    assert session.calls == 2


def test_write_universe_creates_survivorship_schema(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("POLYGON_API_KEY", "test-token")
    output = tmp_path / "survivorship_universe.csv"

    class Args:
        active_from = "2026-05-24"
        market = "stocks"
        max_symbols = 1
        output = output
        sleep_seconds = 0.0

    payload = {"results": [{"ticker": "AAA", "name": "A Inc", "type": "CS", "primary_exchange": "XNYS"}]}

    from scripts import build_polygon_universe as module

    class SessionFactory:
        def __call__(self):
            session = FakeSession([payload])
            session.params = {}
            return session

    monkeypatch.setattr(module.requests, "Session", SessionFactory())
    count = write_universe(Args)

    assert count == 1
    with output.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    assert rows[0]["symbol"] == "AAA"
    assert rows[0]["active_from"] == "2026-05-24"
    assert "active_polygon_universe" in rows[0]["notes"]


def test_bar_to_row_converts_polygon_timestamp() -> None:
    row = bar_to_row({"t": 1704067200000, "o": 1, "h": 2, "l": 0.5, "c": 1.5, "v": 100})

    assert row == {"date": "2024-01-01", "open": 1, "high": 2, "low": 0.5, "close": 1.5, "volume": 100}


def test_write_bars_and_load_symbols(tmp_path: Path) -> None:
    universe = tmp_path / "universe.csv"
    universe.write_text("symbol,active_from\nAAA,2026-05-24\nBBB,2026-05-24\n", encoding="utf-8")

    assert load_symbols(universe) == ["AAA", "BBB"]

    count = write_bars("AAA", [{"t": 1704067200000, "o": 1, "h": 2, "l": 0.5, "c": 1.5, "v": 100}], tmp_path / "bars")

    assert count == 1
    assert (tmp_path / "bars" / "AAA.csv").exists()


def test_write_manifest_lists_failures(tmp_path: Path) -> None:
    manifest = tmp_path / "manifest.md"

    write_manifest(manifest, requested=2, downloaded=1, skipped=1, failed=0, bars_written=250, failures=["BBB: insufficient bars"])

    text = manifest.read_text(encoding="utf-8")
    assert "Requested symbols: **2**" in text
    assert "BBB: insufficient bars" in text
