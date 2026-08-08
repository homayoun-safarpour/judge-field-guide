"""Load and validate the judge-tool registry."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

VALID_CATEGORIES = {"A", "B", "C", "D"}
REQUIRED_FIELDS = {"name", "url", "category", "why"}


class RegistryError(ValueError):
    """Raised when the registry file fails schema validation."""


def load_registry(path: str | Path) -> list[dict[str, Any]]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise RegistryError("registry must be a JSON list")
    seen_urls: set[str] = set()
    seen_names: set[str] = set()
    for i, entry in enumerate(data):
        missing = REQUIRED_FIELDS - entry.keys()
        if missing:
            raise RegistryError(f"entry {i} missing fields: {sorted(missing)}")
        if entry["category"] not in VALID_CATEGORIES:
            raise RegistryError(
                f"entry {i} ({entry['name']}) has invalid category {entry['category']!r}"
            )
        if entry["url"] in seen_urls:
            raise RegistryError(f"duplicate url: {entry['url']}")
        if entry["name"] in seen_names:
            raise RegistryError(f"duplicate name: {entry['name']}")
        seen_urls.add(entry["url"])
        seen_names.add(entry["name"])
    return data
