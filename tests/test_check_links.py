from judgefieldguide.check_links import check_all, evaluate, format_report

ENTRIES = [
    {"name": "alive-one", "url": "https://example.com/a", "category": "A", "why": "x"},
    {"name": "dead-one", "url": "https://example.com/b", "category": "A", "why": "y"},
    {"name": "timeout-one", "url": "https://example.com/c", "category": "A", "why": "z"},
]


def fake_fetch(url: str, timeout: float = 10.0) -> int | None:
    return {"https://example.com/a": 200, "https://example.com/b": 404}.get(url)


def test_check_all_marks_ok_by_status_range():
    results = check_all(ENTRIES, fetch=fake_fetch)
    assert results[0]["ok"] is True
    assert results[1]["ok"] is False
    assert results[2]["ok"] is False  # None (network failure) => not ok


def test_evaluate_exit_code_zero_when_all_alive():
    all_alive = [{"name": "a", "url": "u", "status": 200, "ok": True}]
    assert evaluate(all_alive) == 0


def test_evaluate_exit_code_two_when_any_dead():
    mixed = [
        {"name": "a", "url": "u1", "status": 200, "ok": True},
        {"name": "b", "url": "u2", "status": 404, "ok": False},
    ]
    assert evaluate(mixed) == 2


def test_format_report_lists_dead_names():
    results = check_all(ENTRIES, fetch=fake_fetch)
    report = format_report(results)
    assert "dead-one" in report
    assert "timeout-one" in report
    assert "2/3 links alive" not in report  # only 1/3 alive here
    assert "1/3 links alive." in report
