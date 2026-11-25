"""Check every registry URL and report which ones are dead.

Design: the network call is isolated behind ``fetch_status`` so tests can
monkeypatch it and exercise the pass/fail logic with zero network access.
"""

from __future__ import annotations

import argparse
import http.client
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

from .registry import RegistryError, load_registry

USER_AGENT = "judge-field-guide-linkcheck/0.1 (+https://github.com/homayoun-safarpour/judge-field-guide)"


def _fetch_once(url: str, timeout: float) -> int | str:
    try:
        req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status
    except urllib.error.HTTPError as exc:
        return exc.code
    except urllib.error.URLError as exc:
        return "timeout" if isinstance(exc.reason, TimeoutError) else "unreachable"
    except TimeoutError:
        return "timeout"
    except (OSError, ValueError, http.client.HTTPException):
        return "unreachable"


def fetch_status(url: str, timeout: float = 10.0) -> int | str:
    """Return the final HTTP status for ``url``, or ``"timeout"`` / ``"unreachable"``.

    A network failure is tried once more before it is reported.
    """
    status = _fetch_once(url, timeout)
    if isinstance(status, str):
        status = _fetch_once(url, timeout)
    return status


def check_all(
    entries: list[dict[str, Any]], fetch: Any = fetch_status
) -> list[dict[str, Any]]:
    """Return one result dict per entry: name, url, status, ok."""
    results = []
    for entry in entries:
        status = fetch(entry["url"])
        # urllib follows redirects, so a 3xx here was not followed (loop, 304): dead.
        ok = isinstance(status, int) and 200 <= status < 300
        results.append({"name": entry["name"], "url": entry["url"], "status": status, "ok": ok})
    return results


def evaluate(results: list[dict[str, Any]]) -> int:
    """Exit code contract: 0 all links alive, 2 at least one dead link, 1 nothing checked."""
    if not results:
        return 1
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


def stub_fetch(mapping: dict[str, Any]):
    """Return a fetch function that never touches the network."""

    def fetch(url: str, timeout: float = 10.0) -> int | str | None:
        if url not in mapping:
            return None
        status = mapping[url]
        return None if status is None else int(status)

    return fetch


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--registry", default=str(Path(__file__).parent.parent / "data" / "registry.json")
    )
    parser.add_argument(
        "--stub-status",
        default=None,
        help="JSON object mapping url to HTTP status (or null). Skips the network.",
    )
    parser.add_argument(
        "--report-json",
        default=None,
        help="Also write the results as a JSON list to this file (read by stamp_verified).",
    )
    args = parser.parse_args(argv)

    try:
        entries = load_registry(args.registry)
    except RegistryError as exc:
        print(f"registry error: {exc}", file=sys.stderr)
        return 1
    fetch = fetch_status
    if args.stub_status:
        try:
            raw = json.loads(Path(args.stub_status).read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            print(f"cannot read --stub-status: {exc}", file=sys.stderr)
            return 1
        if not isinstance(raw, dict):
            print("--stub-status must be a JSON object", file=sys.stderr)
            return 1
        fetch = stub_fetch(raw)
    results = check_all(entries, fetch=fetch)
    print(format_report(results))
    if args.report_json:
        Path(args.report_json).write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    return evaluate(results)


if __name__ == "__main__":
    sys.exit(main())
