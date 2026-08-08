"""Check every registry URL and report which ones are dead.

Design: the network call is isolated behind ``fetch_status`` so tests can
monkeypatch it and exercise the pass/fail logic with zero network access.
"""

from __future__ import annotations

import argparse
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

from .registry import load_registry

USER_AGENT = "judge-field-guide-linkcheck/0.1 (+https://github.com/homayoun-safarpour/judge-field-guide)"


def fetch_status(url: str, timeout: float = 10.0) -> int | None:
    """Return the HTTP status code for ``url``, or ``None`` on network failure."""
    req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status
    except urllib.error.HTTPError as exc:
        return exc.code
    except (urllib.error.URLError, TimeoutError, OSError):
        return None


def check_all(
    entries: list[dict[str, Any]], fetch: Any = fetch_status
) -> list[dict[str, Any]]:
    """Return one result dict per entry: name, url, status, ok."""
    results = []
    for entry in entries:
        status = fetch(entry["url"])
        ok = status is not None and 200 <= status < 400
        results.append({"name": entry["name"], "url": entry["url"], "status": status, "ok": ok})
    return results


def evaluate(results: list[dict[str, Any]]) -> int:
    """Exit code contract: 0 all links alive, 2 at least one dead link."""
    return 0 if all(r["ok"] for r in results) else 2


def format_report(results: list[dict[str, Any]]) -> str:
    lines = ["name | status | ok", "--- | --- | ---"]
    for r in results:
        lines.append(f"{r['name']} | {r['status']} | {'yes' if r['ok'] else 'NO'}")
    dead = [r for r in results if not r["ok"]]
    lines.append("")
    lines.append(f"{len(results) - len(dead)}/{len(results)} links alive.")
    if dead:
        lines.append("Dead: " + ", ".join(r["name"] for r in dead))
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--registry", default=str(Path(__file__).parent.parent / "data" / "registry.json")
    )
    args = parser.parse_args(argv)

    entries = load_registry(args.registry)
    results = check_all(entries)
    print(format_report(results))
    return evaluate(results)


if __name__ == "__main__":
    sys.exit(main())
