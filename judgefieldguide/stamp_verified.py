"""Stamp last_verified=today on every registry entry (run after a green link-check)."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from pathlib import Path


def stamp(path: Path, day: str | None = None) -> int:
    day = day or dt.datetime.now(dt.timezone.utc).date().isoformat()
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise SystemExit("registry must be a JSON list")
    for entry in data:
        entry["last_verified"] = day
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print(f"stamped {len(data)} entries -> {day}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--registry",
        default=str(Path(__file__).parent.parent / "data" / "registry.json"),
    )
    parser.add_argument("--date", default=None, help="YYYY-MM-DD (default: today)")
    args = parser.parse_args(argv)
    return stamp(Path(args.registry), args.date)


if __name__ == "__main__":
    sys.exit(main())
