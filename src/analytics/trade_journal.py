from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import UTC, datetime


@dataclass
class TradeJournalEntry:
    ticker: str
    entry_price: float
    exit_price: float
    shares: int
    pnl: float
    pnl_percent: float
    outcome: str
    closed_at: str = ""

    def to_dict(self) -> dict:
        data = asdict(self)
        if not data["closed_at"]:
            data["closed_at"] = datetime.now(UTC).isoformat()
        return data


def create_trade_journal_entry(
    ticker: str,
    entry_price: float,
    exit_price: float,
    shares: int,
) -> dict:
    pnl = round((exit_price - entry_price) * shares, 2)
    pnl_percent = round(((exit_price - entry_price) / entry_price) * 100, 2)

    outcome = "WIN"
    if pnl < 0:
        outcome = "LOSS"
    elif pnl == 0:
        outcome = "BREAKEVEN"

    return TradeJournalEntry(
        ticker=ticker,
        entry_price=entry_price,
        exit_price=exit_price,
        shares=shares,
        pnl=pnl,
        pnl_percent=pnl_percent,
        outcome=outcome,
    ).to_dict()
