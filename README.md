# judge-map

**Curated tool lists go stale: links die, and nobody notices until a reader hits a 404.**

[![CI](https://github.com/homayoun-safarpour/judge-field-guide/actions/workflows/ci.yml/badge.svg)](https://github.com/homayoun-safarpour/judge-field-guide/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue)
![License](https://img.shields.io/badge/license-MIT-green)

Link-checked map of tools for language-model judges, with a checker that names dead links (exit 0 or 2).

judge-field-guide is a map of 20 open-source tools for language-model judges, kept as one JSON file with a tested link checker. We built it because the links in a curated list stop working over time, and a reader usually finds a dead link before the maintainer does. Given a registry file, the checker sends a HEAD request to each URL and counts a status from 200 to 399 as alive, while an error status or no answer counts as dead. It prints each entry with its HTTP status and returns exit 0 when every link is alive or 2 when any is dead, so that CI names the dead entries.

```bash
git clone https://github.com/homayoun-safarpour/judge-field-guide
cd judge-field-guide && pip install -e .
python -m judgefieldguide.check_links --registry examples/dead_slice.json --stub-status examples/stub_dead.json
```

```text
name | status | ok
--- | --- | ---
alive-one | 200 | yes
dead-one | 404 | NO
timeout-one | None | NO

1/3 links alive.
Dead: dead-one, timeout-one
```

That command exits 2. `--stub-status` replaces the network with a fixed map of URL to status, and a URL missing from the map counts as no answer.

## What each result means

| Exit | Meaning |
|---|---|
| 0 | Every URL in the registry answered with a status from 200 to 399. |
| 2 | At least one URL answered with another status or did not answer. The report lists those entries after `Dead:`. |
| 1 | The `--stub-status` file is not a JSON object, or the registry failed its schema check and the checker stopped with a `RegistryError`. |

An exit 0 shows that each URL answered on the day of the run. It does not show that the tool behind the link works, is maintained or is any good. Exits 0 and 2 have named tests (`test_evaluate_exit_code_zero_when_all_alive`, `test_evaluate_exit_code_two_when_any_dead`, `test_readme_stranger_stub_exits_2`); exit 1 has none. The limits of each claim are in [docs/RELIABILITY_CARD.md](docs/RELIABILITY_CARD.md).

## Use this when

| Situation | Use judge-field-guide? |
| --- | --- |
| You want a short list of tools for language-model judges, grouped by the job each tool does | Yes |
| You keep links in this registry format and want a check that names the dead ones with exit 0 or 2 | Yes |
| You want every judge tool there is, ranked by votes | No. Use a broader list such as [CSHaitao/Awesome-LLMs-as-Judges](https://github.com/CSHaitao/Awesome-LLMs-as-Judges), which is one of the entries |
| You want a judge or a judge metric itself | No. Use [judge-reliability-kit](https://github.com/homayoun-safarpour/judge-reliability-kit) or [judge-drift-sentinel](https://github.com/homayoun-safarpour/judge-drift-sentinel) |
| You need to know whether a linked tool works | No. The checker only tests that the URL answers |

Interview pack: [docs/INTERVIEW.md](docs/INTERVIEW.md).

## The problem

A list of links in a markdown file has no test, so it is correct only on the day it was written. When a repository is renamed or deleted, the list keeps pointing at it, and the first person to find out is a reader who clicks the link. Here every entry lives in a JSON registry with a schema, and a link check runs in CI, so a dead entry shows up as a failed check with its name.

## The map

The registry is [data/registry.json](data/registry.json). Each entry has a `name`, a `url`, a `category`, a `why` written for this registry, and a `last_verified` date.

| Code | Group | What the tools do | Entries |
| --- | --- | --- | --- |
| A | Meta-evaluate the judge | Kappa, bias correction, disagreement decomposition | 9 |
| B | Living and adversarial benchmarks | Test judges against harder, changing cases | 2 |
| C | Eval-driven systems and gates | Metrics that gate a deploy instead of only reporting a score | 5 |
| D | Open harness norms | Shared libraries and curated maps of judge tools | 4 |

## How it works

1. `judgefieldguide.registry` loads the registry and rejects a missing field, a category outside A to D, a `last_verified` date not in `YYYY-MM-DD` form, and a repeated URL ([tests/test_registry.py](tests/test_registry.py)).
2. `judgefieldguide.check_links` keeps the network call inside `fetch_status`, so the pass and fail logic is tested offline with a fake fetcher ([tests/test_check_links.py](tests/test_check_links.py)). `--stub-status` does the same from the command line.
3. CI runs `ruff` and the tests on Python 3.10, 3.11 and 3.12. A separate `link-check` job runs the live check on every push and pull request and every Monday at 06:00 UTC. On the Monday run, a green check stamps today's date into `last_verified` and commits it, and a dead link opens an issue labelled `link-rot` unless one is already open.

```bash
pip install -e ".[dev]"
python -m pytest -q
python -m judgefieldguide.check_links
```

On 20 Nov 2026 the tests printed `15 passed in 0.16s`. The live check, which needs network access, printed one row per entry, ended with `20/20 links alive.` and exited 0.

| Module | What it does |
|---|---|
| `judgefieldguide.registry` | Loads `data/registry.json` and checks its schema |
| `judgefieldguide.check_links` | Checks every URL, prints the report and returns exit 0 or 2 |
| `judgefieldguide.stamp_verified` | Writes one `last_verified` date into every entry after a green scheduled check |

## Limits

- It is not a complete index. It holds 20 entries chosen by one person, and the A to D groups are a judgement call.
- The check sends HEAD requests only. A server that refuses HEAD (for example with 405) counts as dead, even if the page opens in a browser.
- The `link-check` job is set to `continue-on-error`, so a dead link does not block a pull request.
- `last_verified` is written to all entries at once after a green scheduled run. It is not a separate date per entry.
- Exit 1 comes from an input error, not from a designed check, and has no test.
- The checker uses the Python standard library only and needs Python 3.10 or later.

## Related tools

- [judge-reliability-kit](https://github.com/homayoun-safarpour/judge-reliability-kit): why a judge panel disagrees (kappa).
- [judge-drift-sentinel](https://github.com/homayoun-safarpour/judge-drift-sentinel): tells judge drift from system drift.
- [trace-gate](https://github.com/homayoun-safarpour/trace-gate): a deploy gate on agent runs.

## Credit

This is an independently curated, re-verified registry, not a fork. The idea started
from reading `haizelabs/Awesome-LLM-Judges` (entry D1 in the registry, credited there), which
has no license and is a plain link list. Rather than fork unlicensed content, every entry here
was re-selected, re-described in original language, and wired to a real test. MIT-licensed,
fork freely.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## Author

Homayoun Safarpour. [LinkedIn](https://www.linkedin.com/in/homayoun-safarpour/)

## License

MIT. See [`LICENSE`](LICENSE).
