import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT_DIR / "src"

for item in [ROOT_DIR, SRC_DIR]:
    value = str(item)
    if value not in sys.path:
        sys.path.insert(0, value)
