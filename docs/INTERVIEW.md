# Interview talking points : judge-field-guide

- **`python -m judgefieldguide.check_links`** : real HTTP check against every registry URL; exits 2 and names the dead ones instead of leaving stale links in a markdown table.
- **`pytest tests/test_check_links.py`** : pass/fail logic tested with a fake fetcher, so CI never depends on network flakiness for the blocking gate.
- **`pytest tests/test_registry.py`** : schema gate - required fields, valid A-D categories, no duplicate names/urls - catches copy-paste errors before they ship.
- **Weekly cron `link-check` job** : non-blocking on PRs, but gives a dated, verifiable "still alive" signal instead of a link list frozen the day it was written.
- **Composes with the face stack** : registry entries link back to `judge-reliability-kit`, `judge-drift-sentinel`, and `trace-gate` so the map doubles as a discovery path into the rest of the instruments.

## Three questions

1. **Why build this instead of just reading an existing awesome-list?**
   Awesome-lists have no license and no test - links rot silently and nobody notices until a reader hits a 404. This one fails CI when that happens.

2. **Why categories A-D instead of stars?**
   Stars measure popularity, not the job a tool does. The categories mirror the actual reasoning pattern (meta-eval, benchmark, gate, harness) so a reader picks by need, not by hype.

3. **What would you add next?**
   Auto-opening a GitHub issue when the weekly link-check job finds a dead link, so the registry self-reports rot instead of waiting for a human to notice.

## One limitation

16 entries is a slice, not a census; the categorization is a judgment call by one person, not a community vote.
