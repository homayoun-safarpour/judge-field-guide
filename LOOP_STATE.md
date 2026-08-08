# LOOP_STATE — judge-field-guide

## BENCHMARK GATE (Sat 2026-08-08)

Named suite: pytest (`tests/test_registry.py`, `tests/test_check_links.py`) + ruff.
Pinned: no external deps beyond stdlib for the checker; pytest/ruff pinned via `pyproject.toml` extras.
Runnable subset: `pytest -q` (offline, blocking). `python -m judgefieldguide.check_links` (network, weekly cron job, non-blocking on PRs — results are the dated artifact of truth).

## Backlog

- [x] W1 registry schema + loader with validation (`judgefieldguide/registry.py`) — 2026-08-08
- [x] W2 link checker with fetch isolated for offline testing (`judgefieldguide/check_links.py`) — 2026-08-08
- [x] W3 CI: 3.10/3.11/3.12 test matrix + weekly non-blocking link-check job — 2026-08-08
- [x] W4 README (problem-first, categories, provenance/attribution) + reliability card + interview pack — 2026-08-08
- [x] W5 auto-open a GitHub issue when the weekly link-check job finds a dead entry — 2026-08-08
- [x] W6 `last_verified` date field per entry, updated by a scheduled commit after a green link-check run — 2026-08-08
- [x] W7 expand registry (+4 field entries -> 20 total) — 2026-08-08

## Provenance note

Started from reading `haizelabs/Awesome-LLM-Judges` (unlicensed link list, 202 stars). Not
forked — every entry independently re-selected and re-described; the license-clean path is
this repo's own MIT registry + real HTTP test, not a copy of their file.

## NEXT TICK (2026-08-08, W7 done)

- Next: keep registry fresh via weekly link-check; add entries only when Sunday trend memo names a new hire-signal tool.
- Why: avoid untested mega-list growth.
- Verify: pytest green; scheduled link-check stays green.