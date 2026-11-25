import json
import urllib.error
import urllib.request
from pathlib import Path

import pytest

from judgefieldguide.check_links import check_all, evaluate, fetch_status, format_report, main

ROOT = Path(__file__).resolve().parents[1]


def _raise(exc):
    def urlopen(*args, **kwargs):
        raise exc

    return urlopen


def test_redirect_loop_is_dead(monkeypatch):
    loop = urllib.error.HTTPError("https://x.example/", 302, "Found", {}, None)
    monkeypatch.setattr(urllib.request, "urlopen", _raise(loop))
    status = fetch_status("https://x.example/")
    [result] = check_all([{"name": "loop", "url": "https://x.example/"}], fetch=lambda u: status)
    assert result["ok"] is False


@pytest.mark.parametrize("status", [300, 301, 302, 304, 307, 399])
def test_unfollowed_3xx_status_is_dead(status):
    [result] = check_all([{"name": "n", "url": "https://x"}], fetch=lambda u: status)
    assert result["ok"] is False


def test_evaluate_with_no_results_is_not_a_pass():
    assert evaluate([]) != 0


def test_url_without_scheme_is_named_dead_not_a_crash():
    status = fetch_status("example.com")
    [result] = check_all([{"name": "n", "url": "example.com"}], fetch=lambda u: status)
    assert result["ok"] is False


def test_timeout_is_reported_as_timeout_after_one_retry(monkeypatch):
    calls = []

    def urlopen(*args, **kwargs):
        calls.append(1)
        raise urllib.error.URLError(TimeoutError("timed out"))

    monkeypatch.setattr(urllib.request, "urlopen", urlopen)
    assert fetch_status("https://slow.example/") == "timeout"
    assert len(calls) == 2


def test_unknown_host_is_reported_as_unreachable(monkeypatch):
    monkeypatch.setattr(
        urllib.request, "urlopen", _raise(urllib.error.URLError("Name or service not known"))
    )
    assert fetch_status("https://nohost.example/") == "unreachable"


def test_reason_text_is_dead_and_shown_in_report():
    results = check_all([{"name": "slow", "url": "u"}], fetch=lambda u: "timeout")
    assert results[0]["ok"] is False
    assert "slow | timeout | NO" in format_report(results)


def _write(tmp_path, name, data):
    path = tmp_path / name
    path.write_text(json.dumps(data), encoding="utf-8")
    return str(path)


def test_main_empty_registry_exits_1_with_one_line(tmp_path, capsys):
    reg = _write(tmp_path, "empty.json", [])
    stub = _write(tmp_path, "stub.json", {})
    assert main(["--registry", reg, "--stub-status", stub]) == 1
    err = capsys.readouterr().err.strip()
    assert len(err.splitlines()) == 1 and "no entries" in err


def test_main_non_object_entry_exits_1_with_one_line(tmp_path, capsys):
    reg = _write(tmp_path, "str.json", ["x"])
    stub = _write(tmp_path, "stub.json", {})
    assert main(["--registry", reg, "--stub-status", stub]) == 1
    err = capsys.readouterr().err.strip()
    assert len(err.splitlines()) == 1 and "must be a JSON object" in err


def test_main_stub_not_object_exits_1(tmp_path):
    stub = _write(tmp_path, "stub.json", [])
    reg = str(ROOT / "examples" / "dead_slice.json")
    assert main(["--registry", reg, "--stub-status", stub]) == 1


def test_main_writes_json_report(tmp_path):
    out = tmp_path / "report.json"
    code = main(
        [
            "--registry",
            str(ROOT / "examples" / "dead_slice.json"),
            "--stub-status",
            str(ROOT / "examples" / "stub_dead.json"),
            "--report-json",
            str(out),
        ]
    )
    assert code == 2
    report = json.loads(out.read_text(encoding="utf-8"))
    assert [r["ok"] for r in report] == [True, False, False]
