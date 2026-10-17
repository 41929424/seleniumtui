"""Persist the most recent passing verification state for each test case."""

import json
import xml.etree.ElementTree as ET
from pathlib import Path

PROGRESS_FILE = Path(".qa-progress.json")
RESULTS_FILE = Path(".qa-progress-results.xml")
MODULE_CASES = {
    "test_login.py": {f"test_auth_{i:02d}" for i in range(1, 6)},
    "test_inventory.py": {f"test_cat_{i:02d}" for i in range(1, 6)},
    "test_cart.py": {f"test_cart_{i:02d}" for i in range(1, 6)},
    "test_checkout.py": {f"test_chk_{i:02d}" for i in range(1, 6)},
}


def read_progress() -> set[str]:
    if not PROGRESS_FILE.exists():
        return set()
    try:
        return set(json.loads(PROGRESS_FILE.read_text(encoding="utf-8")).get("verified", []))
    except (OSError, json.JSONDecodeError):
        return set()


def record_run(target: str) -> int:
    """Update only scenarios included in the just-completed pytest run."""
    cases = set().union(
        *(ids for filename, ids in MODULE_CASES.items() if filename in target or target.endswith("tests/ui"))
    )
    if not cases or not RESULTS_FILE.exists():
        return len(read_progress())

    verified = read_progress() - cases
    root = ET.parse(RESULTS_FILE).getroot()
    for testcase in root.iter("testcase"):
        function_name = testcase.attrib.get("name", "")
        case = next((prefix for prefix in cases if function_name.startswith(prefix)), None)
        failed = any(testcase.find(tag) is not None for tag in ("failure", "error", "skipped"))
        if case and not failed:
            verified.add(case)

    PROGRESS_FILE.write_text(
        json.dumps({"verified": sorted(verified)}, indent=2) + "\n", encoding="utf-8"
    )
    return len(verified)
