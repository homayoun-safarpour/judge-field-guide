"""Load and validate the judge-tool registry."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit

VALID_CATEGORIES = {"A", "B", "C", "D"}
REQUIRED_FIELDS = {"name", "url", "category", "why", "last_verified"}
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
URL_RE = re.compile(r"^https?://[^/\s]+", re.IGNORECASE)


class RegistryError(ValueError):
    """Raised when the registry file fails schema validation."""


def url_key(url: str) -> str:
    """Key used to spot the same URL written twice (case of scheme/host, trailing slash)."""
    parts = urlsplit(url.strip())
    path = parts.path.rstrip("/")
    return f"{parts.scheme.lower()}://{parts.netloc.lower()}{path}?{parts.query}"


def load_registry(path: str | Path) -> list[dict[str, Any]]:
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise RegistryError(f"cannot read registry {path}: {exc}") from exc
    if not isinstance(data, list):
        raise RegistryError("registry must be a JSON list")
    if not data:
        raise RegistryError("registry has no entries")
    seen_urls: set[str] = set()
    seen_names: set[str] = set()
    for i, entry in enumerate(data):
        if not isinstance(entry, dict):
            raise RegistryError(f"entry {i} must be a JSON object")
        missing = REQUIRED_FIELDS - entry.keys()
        if missing:
            raise RegistryError(f"entry {i} missing fields: {sorted(missing)}")
        if entry["category"] not in VALID_CATEGORIES:
            raise RegistryError(
                f"entry {i} ({entry['name']}) has invalid category {entry['category']!r}"
            )
        if not DATE_RE.match(str(entry["last_verified"])):
            raise RegistryError(
                f"entry {i} ({entry['name']}) last_verified must be YYYY-MM-DD"
            )
        url = entry["url"]
        if not isinstance(url, str) or not URL_RE.match(url):
            raise RegistryError(
                f"entry {i} ({entry['name']}) url must start with http:// or https://"
            )
        key = url_key(url)
        if key in seen_urls:
            raise RegistryError(f"duplicate url: {url}")
        name_key = str(entry["name"]).casefold()
        if name_key in seen_names:
            raise RegistryError(f"duplicate name: {entry['name']}")
        seen_urls.add(key)
        seen_names.add(name_key)
    return data
