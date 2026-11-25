"""Read .github/workflows/ci.yml as text and check the link-check job fails closed."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CI = (ROOT / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")


def _steps(text: str) -> list[str]:
    """Split the workflow into step blocks (each starts with '      - ')."""
    blocks: list[str] = []
    current: list[str] | None = None
    for line in text.splitlines():
        if re.match(r"^ {6}- ", line):
            if current is not None:
                blocks.append("\n".join(current))
            current = [line]
        elif current is not None:
            if line.strip() and not line.startswith("        "):
                blocks.append("\n".join(current))
                current = None
            else:
                current.append(line)
    if current is not None:
        blocks.append("\n".join(current))
    return blocks


def _link_check_step() -> str:
    steps = [s for s in _steps(CI) if "judgefieldguide.check_links" in s]
    assert len(steps) == 1, "expected exactly one step that runs the link check"
    return steps[0]


def test_link_check_pipe_has_pipefail():
    step = _link_check_step()
    piped = any(
        "judgefieldguide.check_links" in line and "|" in line for line in step.splitlines()
    )
    if piped:
        assert "set -o pipefail" in step, "link check is piped without pipefail"


def test_pipefail_check_catches_the_old_step():
    old = "      - name: Run link check\n        run: python -m judgefieldguide.check_links | tee r.txt\n"
    step = _steps(old)[0]
    assert "|" in step and "set -o pipefail" not in step


def test_stamp_runs_only_after_successful_scheduled_check():
    stamp = [s for s in _steps(CI) if "judgefieldguide.stamp_verified" in s]
    assert len(stamp) == 1
    assert "steps.linkcheck.outcome == 'success'" in stamp[0]
    assert "github.event_name == 'schedule'" in stamp[0]
    assert "--report" in stamp[0], "stamp must read the link report, not stamp blindly"


def test_dead_link_fails_the_link_check_job():
    fail = [s for s in _steps(CI) if "steps.linkcheck.outcome == 'failure'" in s and "exit 1" in s]
    assert fail, "a failed link check must end the job with a failure"


def test_scheduled_link_check_is_not_masked_by_continue_on_error():
    job = CI.split("  link-check:", 1)[1].split("    steps:", 1)[0]
    assert "continue-on-error: true" not in job
    assert "continue-on-error: ${{ github.event_name != 'schedule' }}" in job
