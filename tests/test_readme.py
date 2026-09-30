from pathlib import Path

from judgefieldguide.check_links import main

ROOT = Path(__file__).resolve().parents[1]
README = (ROOT / "README.md").read_text(encoding="utf-8-sig")
DEAD = ROOT / "examples" / "dead_slice.json"
STUB = ROOT / "examples" / "stub_dead.json"


def test_readme_spoken_h1_is_judge_map():
    assert README.lstrip().startswith("# judge-map\n")
    assert "judge-field-guide" in README


def test_readme_first_screen_matches_top100_craft():
    pip_at = README.find("pip install")
    interview_at = README.find("Interview pack")
    assert 0 <= pip_at < interview_at
    head = "\n".join(README.splitlines()[:28])
    assert "# judge-map" in head
    assert "git clone https://github.com/homayoun-safarpour/judge-field-guide" in head
    assert "pip install -e" in head
    assert "examples/dead_slice.json" in head
    assert "Dead: dead-one, timeout-one" in head
    assert "Interview pack" not in head
    assert "\u2014" not in head


def test_readme_stranger_stub_exits_2():
    code = main(
        [
            "--registry",
            str(DEAD),
            "--stub-status",
            str(STUB),
        ]
    )
    assert code == 2
