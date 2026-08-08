# Contributing

Thanks for helping keep the judge-tool map honest.

## Ways to help

1. **Add one registry entry** (preferred) - see open good-first-issue for the checklist.
2. **Report a dead link** - open an issue with the entry `name` and the HTTP status you saw.
3. **Fix docs** - README / reliability card / interview pack only; keep senior-engineer register (no portfolio/demo filler).

## Rules

- Original `why` text only. Do not copy from unlicensed awesome-lists.
- Every entry needs: `name`, `url`, `category` (`A`|`B`|`C`|`D`), `why`, `last_verified` (`YYYY-MM-DD`).
- Before opening a PR:

```bash
pip install -e ".[dev]"
ruff check .
pytest -q
```

Optional (needs network): `python -m judgefieldguide.check_links` (exit `0` all alive, `2` names the dead).

## License

MIT. By contributing you agree your changes are MIT-licensed.
