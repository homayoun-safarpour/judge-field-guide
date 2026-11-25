import re
from pathlib import Path

from judgefieldguide.registry import load_registry

ROOT = Path(__file__).resolve().parents[1]
COUNT = len(load_registry(ROOT / "data" / "registry.json"))


def test_docs_state_the_registry_entry_count():
    for name in ("README.md", "docs/RELIABILITY_CARD.md", "docs/INTERVIEW.md"):
        text = (ROOT / name).read_text(encoding="utf-8-sig")
        counts = {int(n) for n in re.findall(r"\b(\d+) (?:entries|open-source tools)\b", text)}
        assert counts == {COUNT}, f"{name} states {sorted(counts)} entries, registry has {COUNT}"
