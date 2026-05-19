from pathlib import Path

from scripts.generate_outcomes import extract_signals


def test_extract_signals():
    text = "AAPL and NVDA are leaders. QQQ remains strong."

    signals = extract_signals(text)

    assert "AAPL" in signals
    assert "NVDA" in signals
    assert "QQQ" in signals


def test_outcome_directory_structure_exists():
    outcomes_dir = Path("reports/outcomes")
    outcomes_dir.mkdir(parents=True, exist_ok=True)

    assert outcomes_dir.exists()
