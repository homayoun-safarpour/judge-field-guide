"""Stamp last_verified on the registry entries that a link-check report marks as alive.

The report is the JSON file written by ``check_links --report-json``. Entries that the
report does not mark ``ok`` keep their old date.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from pathlib import Path

from .registry import DATE_RE


def _valid_day(day: str) -> bool:
    if not DATE_RE.match(day):
        return False
    try:
        dt.date.fromisoformat(day)
    except ValueError:
        return False
    return True


def stamp(path: Path, report: Path, day: str | None = None) -> int:
    day = day or dt.datetime.now(dt.timezone.utc).date().isoformat()
    if not _valid_day(day):
        print(f"--date must be a real YYYY-MM-DD date, got {day!r}", file=sys.stderr)
        return 1
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        results = json.loads(report.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        print(f"cannot read registry or report: {exc}", file=sys.stderr)
        return 1
    if not isinstance(data, list):
        print("registry must be a JSON list", file=sys.stderr)
        return 1
    if not isinstance(results, list) or not all(
        isinstance(r, dict) and "url" in r and "ok" in r for r in results
    ):
        print("report must be a JSON list of results with url and ok", file=sys.stderr)
        return 1
    alive = {r["url"] for r in results if r["ok"] is True}
    stamped = 0
    for entry in data:
        if isinstance(entry, dict) and entry.get("url") in alive:
            entry["last_verified"] = day
            stamped += 1
    with path.open("w", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(data, indent=2) + "\n")
    print(f"stamped {stamped} of {len(data)} entries -> {day}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--registry",
        default=str(Path(__file__).parent.parent / "data" / "registry.json"),
    )
    parser.add_argument(
        "--report",
        required=True,
        help="JSON report written by check_links --report-json",
    )
    parser.add_argument("--date", default=None, help="YYYY-MM-DD (default: today)")
    args = parser.parse_args(argv)
    return stamp(Path(args.registry), Path(args.report), args.date)


if __name__ == "__main__":
    sys.exit(main())
