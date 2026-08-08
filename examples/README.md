# Examples

Offline dogfood - no network required for these two.

```bash
pip install -e ".[dev]"
pytest -q
```

For a real (network) run against the live registry:

```bash
python -m judgefieldguide.check_links
```

Exit `0` means every URL in `data/registry.json` answered 200-3xx. Exit `2` prints which
entries are dead so you know what to fix or retire before trusting the map.

| Path | What it shows |
| --- | --- |
| [../data/registry.json](../data/registry.json) | The full curated, categorized registry |
| [../tests/test_check_links.py](../tests/test_check_links.py) | Pass/fail logic exercised with a fake fetcher (zero network) |
| [../tests/test_registry.py](../tests/test_registry.py) | Schema gate: required fields, valid categories, no duplicates |
