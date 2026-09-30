# judge-map

**Awesome-lists rot. Links die, and nobody notices until a reader hits a 404.**

[![CI](https://github.com/homayoun-safarpour/judge-field-guide/actions/workflows/ci.yml/badge.svg)](https://github.com/homayoun-safarpour/judge-field-guide/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue)
![License](https://img.shields.io/badge/license-MIT-green)

Curated, CI-tested map of the LLM-judge tool ecosystem - checked links, not a link-rot list.

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

That command exits 2. `--stub-status` skips the network. The live registry check has no stub and fails closed on any dead URL.

## Use this when

| Situation | Use this? |
| --- | --- |
| You want a curated entry point into the LLM-judge tool ecosystem | Yes |
| You want a registry with a real test, not a markdown table that goes stale | Yes |
| You want an exhaustive, community-voted index | No - it is a 16-entry curated slice, categorized by job |
| You want a judge implementation itself | No - see [judge-reliability-kit](https://github.com/homayoun-safarpour/judge-reliability-kit) or [judge-drift-sentinel](https://github.com/homayoun-safarpour/judge-drift-sentinel) |

## Quickstart

Interview pack: [docs/INTERVIEW.md](docs/INTERVIEW.md).

Claim boundaries: [docs/RELIABILITY_CARD.md](docs/RELIABILITY_CARD.md).

```bash
pip install -e ".[dev]"
pytest -q
python -m judgefieldguide.check_links
# exit 0 when every registry URL resolves; exit 2 names the dead ones
```

## Categories

| Code | Pattern | Meaning |
| --- | --- | --- |
| A | Meta-evaluate the judge | Kappa, bias correction, disagreement decomposition |
| B | Living/adversarial benchmarks | Judges tested against harder, evolving cases |
| C | Eval-driven systems and gates | Metrics that gate a deploy, not just report a score |
| D | Open harness norms | Shared libraries and curated maps of the ecosystem |

Full registry: [data/registry.json](data/registry.json).

## How the gate works

`judgefieldguide/check_links.py` isolates the network call behind `fetch_status` so the
pass/fail logic (`evaluate`) is tested offline with a fake fetcher
([tests/test_check_links.py](tests/test_check_links.py)). `--stub-status` is that same
isolation on the CLI. The real, network-backed check runs as a weekly `link-check` CI job
(non-blocking on PRs; the dated Action run is the blocking signal).
Schema is enforced separately: required fields, valid A-D categories, no duplicate names or
URLs ([tests/test_registry.py](tests/test_registry.py)).

## How this was built (provenance)

This is an independently curated, re-verified registry, not a fork. The idea started
from reading `haizelabs/Awesome-LLM-Judges` (entry D1 in the registry, credited there), which
has no license and is a plain link list. Rather than fork unlicensed content, every entry here
was re-selected, re-described in original language, and wired to a real test. MIT-licensed,
fork freely.

## Related instruments

- [judge-reliability-kit](https://github.com/homayoun-safarpour/judge-reliability-kit) - why a judge panel disagrees (kappa)
- [judge-drift-sentinel](https://github.com/homayoun-safarpour/judge-drift-sentinel) - judge vs system drift
- [trace-gate](https://github.com/homayoun-safarpour/trace-gate) - trajectory deploy gate

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## Author

Homayoun Safarpour. [LinkedIn](https://www.linkedin.com/in/homayoun-safarpour/)

## License

MIT
