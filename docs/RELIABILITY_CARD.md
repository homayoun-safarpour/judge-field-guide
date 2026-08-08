# Reliability card

| Field | Value |
| --- | --- |
| **Job** | Keep a map of the LLM-judge tool ecosystem from rotting |
| **Primary signal** | `judge-field-guide` / `python -m judgefieldguide.check_links` exit 0/2 against `data/registry.json` |
| **Claim** | Every URL in the registry answered HTTP 200-3xx on the date of the last green `link-check` CI run |
| **Not claimed** | Quality, stars, or maintenance status of the linked tools - only that the link resolves |
| **Not claimed** | Completeness - this is a curated slice (16 entries at v0.1), not an exhaustive index |

## Categories (from field-pattern synthesis)

- **A** - Meta-evaluate the judge (kappa, bias correction, disagreement decomposition)
- **B** - Living/adversarial benchmarks for judges
- **C** - Eval-driven systems and deploy gates
- **D** - Open harness/library norms

## Field alignment

Same production habit as the rest of the stack: a claim is only as good as its named,
runnable test - here that test is a real HTTP check, not a manually-updated markdown table.

## Provenance

Independently curated and re-verified; not a fork. `haizelabs/Awesome-LLM-Judges` is listed
as entry D1 and credited as the broadest prior-art map that inspired starting this registry.
