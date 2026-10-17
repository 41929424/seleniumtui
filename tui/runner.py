"""Keep pytest execution independent from the TUI process."""

import os
import subprocess
import sys


def run_pytest(target: str = "tests/ui") -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env.setdefault("HEADLESS", "1")
    return subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            target,
            "-v",
            "--color=no",
            "--junitxml=.qa-progress-results.xml",
        ],
        check=False,
        capture_output=True,
        text=True,
        env=env,
    )
