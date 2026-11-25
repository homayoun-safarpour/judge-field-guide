import json

import pytest

from judgefieldguide.registry import RegistryError, load_registry


def _entry(name="a", url="https://x.example/a"):
    return {"name": name, "url": url, "category": "A", "why": "x", "last_verified": "2026-08-08"}


def _reg(tmp_path, data):
    path = tmp_path / "reg.json"
    path.write_text(json.dumps(data), encoding="utf-8")
    return path


def test_empty_registry_rejected(tmp_path):
    with pytest.raises(RegistryError, match="no entries"):
        load_registry(_reg(tmp_path, []))


def test_non_object_entry_rejected(tmp_path):
    with pytest.raises(RegistryError, match="must be a JSON object"):
        load_registry(_reg(tmp_path, ["x"]))


@pytest.mark.parametrize("url", ["example.com", "ftp://example.com/x", "", 42])
def test_url_without_http_scheme_rejected(tmp_path, url):
    with pytest.raises(RegistryError, match="http"):
        load_registry(_reg(tmp_path, [_entry(url=url)]))


def test_duplicate_name_differing_in_case_rejected(tmp_path):
    data = [_entry("Foo", "https://a.example/x"), _entry("foo", "https://a.example/y")]
    with pytest.raises(RegistryError, match="duplicate name"):
        load_registry(_reg(tmp_path, data))


@pytest.mark.parametrize(
    "second", ["https://a.example/x/", "https://A.EXAMPLE/x", "HTTPS://a.example/x"]
)
def test_duplicate_url_differing_in_slash_or_host_case_rejected(tmp_path, second):
    data = [_entry("one", "https://a.example/x"), _entry("two", second)]
    with pytest.raises(RegistryError, match="duplicate url"):
        load_registry(_reg(tmp_path, data))


def test_distinct_paths_are_not_duplicates(tmp_path):
    data = [_entry("one", "https://a.example/x"), _entry("two", "https://a.example/X")]
    assert len(load_registry(_reg(tmp_path, data))) == 2
