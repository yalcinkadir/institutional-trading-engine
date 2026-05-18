#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil
from datetime import UTC, datetime
from pathlib import Path

IMPORTANT_PATHS = [
    Path("data"),
    Path("reports"),
    Path(".cache/polygon"),
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create a daily backup archive for important runtime data.")
    parser.add_argument(
        "--output-dir",
        default="backups",
        help="Directory where the backup archive should be written.",
    )
    parser.add_argument(
        "--name-prefix",
        default="institutional-engine-backup",
        help="Backup archive filename prefix.",
    )
    return parser.parse_args()


def copy_if_exists(source: Path, destination_root: Path) -> None:
    if not source.exists():
        return

    destination = destination_root / source

    if source.is_dir():
        shutil.copytree(source, destination, dirs_exist_ok=True)
    else:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)


def create_backup(output_dir: Path, name_prefix: str) -> Path:
    timestamp = datetime.now(UTC).strftime("%Y-%m-%d_%H-%M-%S_UTC")
    staging_dir = output_dir / f"{name_prefix}-{timestamp}"
    staging_dir.mkdir(parents=True, exist_ok=True)

    manifest_lines = [
        f"backup_created_at={timestamp}",
        "included_paths=",
    ]

    for path in IMPORTANT_PATHS:
        if path.exists():
            copy_if_exists(path, staging_dir)
            manifest_lines.append(f"- {path}")
        else:
            manifest_lines.append(f"- {path} (missing)")

    (staging_dir / "BACKUP_MANIFEST.txt").write_text("\n".join(manifest_lines), encoding="utf-8")

    archive_base = output_dir / f"{name_prefix}-{timestamp}"
    archive_path = shutil.make_archive(str(archive_base), "zip", staging_dir)
    shutil.rmtree(staging_dir)

    return Path(archive_path)


def main() -> int:
    args = parse_args()
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    archive = create_backup(output_dir, args.name_prefix)
    print(f"Backup archive created: {archive}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
