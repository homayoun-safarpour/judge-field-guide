import json

import pytest

from judgefieldguide.stamp_verified import main


def _entry(name):
    return {
        "name": name,
        "url": f"https://x.example/{name}",
        "category": "A",
        "why": "x",
        "last_verified": "2026-01-01",
    }


def _files(tmp_path, report):
    reg = tmp_path / "registry.json"
    reg.write_text(json.dumps([_entry("a"), _entry("b")]), encoding="utf-8")
    rep = tmp_path / "report.json"
    rep.write_text(json.dumps(report), encoding="utf-8")
    return reg, rep


def _dates(reg):
    return [e["last_verified"] for e in json.loads(reg.read_text(encoding="utf-8"))]


def test_stamp_only_entries_whose_check_was_ok(tmp_path):
    reg, rep = _files(
        tmp_path,
        [
            {"name": "a", "url": "https://x.example/a", "status": 200, "ok": True},
            {"name": "b", "url": "https://x.example/b", "status": 404, "ok": False},
        ],
    )
    assert main(["--registry", str(reg), "--report", str(rep), "--date", "2026-11-25"]) == 0
    assert _dates(reg) == ["2026-11-25", "2026-01-01"]


@pytest.mark.parametrize("day", ["yesterday", "2026-13-01", "25-11-2026"])
def test_stamp_rejects_bad_date_and_leaves_registry_alone(tmp_path, day):
    reg, rep = _files(tmp_path, [{"name": "a", "url": "https://x.example/a", "ok": True}])
    assert main(["--registry", str(reg), "--report", str(rep), "--date", day]) == 1
    assert _dates(reg) == ["2026-01-01", "2026-01-01"]


def test_stamp_refuses_without_a_report(tmp_path):
    reg, _ = _files(tmp_path, [])
    with pytest.raises(SystemExit) as exc:
        main(["--registry", str(reg), "--date", "2026-11-25"])
    assert exc.value.code != 0
    assert _dates(reg) == ["2026-01-01", "2026-01-01"]


def test_stamp_refuses_malformed_report(tmp_path):
    reg, rep = _files(tmp_path, {"not": "a list"})
    assert main(["--registry", str(reg), "--report", str(rep), "--date", "2026-11-25"]) == 1
    assert _dates(reg) == ["2026-01-01", "2026-01-01"]
