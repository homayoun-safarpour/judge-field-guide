from pathlib import Path

import pytest

from judgefieldguide.registry import RegistryError, load_registry

DATA = Path(__file__).parent.parent / "data" / "registry.json"


def test_registry_loads_and_has_entries():
    entries = load_registry(DATA)
    assert len(entries) >= 10


def test_all_categories_valid():
    for entry in load_registry(DATA):
        assert entry["category"] in {"A", "B", "C", "D"}


def test_no_duplicate_urls(tmp_path):
    bad = tmp_path / "dup.json"
    bad.write_text(
        '[{"name": "a", "url": "https://x", "category": "A", "why": "x", "last_verified": "2026-08-08"},'
        ' {"name": "b", "url": "https://x", "category": "A", "why": "y", "last_verified": "2026-08-08"}]'
    )
    with pytest.raises(RegistryError, match="duplicate url"):
        load_registry(bad)


def test_missing_field_rejected(tmp_path):
    bad = tmp_path / "bad.json"
    bad.write_text('[{"name": "a", "url": "https://x", "category": "A"}]')
    with pytest.raises(RegistryError, match="missing fields"):
        load_registry(bad)


def test_bad_last_verified_rejected(tmp_path):
    bad = tmp_path / "bad_date.json"
    bad.write_text(
        '[{"name": "a", "url": "https://x", "category": "A", "why": "x", '
        '"last_verified": "08-08-2026"}]'
    )
    with pytest.raises(RegistryError, match="last_verified"):
        load_registry(bad)


def test_all_entries_have_last_verified():
    for entry in load_registry(DATA):
        assert "last_verified" in entry
        assert len(entry["last_verified"]) == 10


def test_invalid_category_rejected(tmp_path):
    bad = tmp_path / "bad_cat.json"
    bad.write_text(
        '[{"name": "a", "url": "https://x", "category": "Z", "why": "x", '
        '"last_verified": "2026-08-08"}]'
    )
    with pytest.raises(RegistryError, match="invalid category"):
        load_registry(bad)


def test_not_a_list_rejected(tmp_path):
    bad = tmp_path / "not_list.json"
    bad.write_text('{"name": "a"}')
    with pytest.raises(RegistryError, match="must be a JSON list"):
        load_registry(bad)
