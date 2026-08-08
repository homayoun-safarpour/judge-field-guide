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
- [ ] W5 auto-open a GitHub issue when the weekly link-check job finds a dead entry
- [ ] W6 `last_verified` date field per entry, updated by a scheduled commit after a green link-check run
- [ ] W7 expand registry to ~24 entries once Sunday trend memo flags new field repos

## Provenance note

Started from reading `haizelabs/Awesome-LLM-Judges` (unlicensed link list, 202 stars). Not
forked — every entry independently re-selected and re-described; the license-clean path is
this repo's own MIT registry + real HTTP test, not a copy of their file.

## NEXT TICK (2026-08-08)

- Next: W5 (auto-issue on dead link) — smallest safe increment once the weekly cron has run once for real.
- Why: proves the registry self-reports rot instead of relying on a human noticing.
- Verify: trigger `workflow_dispatch` on `link-check`, confirm an issue opens only on a forced-dead fixture entry, then revert the fixture.
