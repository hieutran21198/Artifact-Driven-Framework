"""Read the Artifact Driven configuration of the repository.

The repository root is the nearest directory, from the current directory up,
that holds artifact-driven.json. Without one, it is the parent of scripts/.
"""

from pathlib import Path
import json
import re

NAME = "artifact-driven.json"
DEFAULTS = {
    "knowledge": "docs/software-knowledges",
    "skip": [".git", "node_modules", "build"],
    "clients": {},
    "services": {},
    "e2e": None,
    "site": {"title": "Software Knowledge", "output": "build/site/index.html"},
}
TEST_GLOB = "**/*_test.*"
# A knowledge ID, such as SYS-4, G-SELL-2 or INV-3. Names of standards that
# look like one, such as UTF-8 or RFC-3339, are not IDs.
ID = re.compile(r"\b(?!(?:UTF|ISO|RFC|SHA|TLS|HTTP|IEEE)-)[A-Z]{1,6}(?:-[A-Z]{1,8})?-\d+\b")


def find_root():
    for folder in (Path.cwd(), *Path.cwd().parents):
        if (folder / NAME).is_file():
            return folder
    return Path(__file__).resolve().parent.parent


def tests_of(part):
    """The tests setting of a service or a client, with the default glob."""
    tests = part.get("tests") if isinstance(part, dict) else None
    return {"glob": TEST_GLOB, **tests} if tests and tests.get("folder") else None


ROOT = find_root()
_file = ROOT / NAME
CONFIG = {**DEFAULTS, **(json.loads(_file.read_text(encoding="utf-8")) if _file.is_file() else {})}
CONFIG["site"] = {**DEFAULTS["site"], **(CONFIG.get("site") or {})}

KNOWLEDGE = ROOT / CONFIG["knowledge"]
SKIP = set(CONFIG["skip"])
# A client is a display name, or an object with a name and its tests.
CLIENTS = {name: (c if isinstance(c, str) else c.get("name", name)) for name, c in CONFIG["clients"].items()}
SERVICES = {name: {"routes": s.get("routes"), "tests": tests_of(s)} for name, s in CONFIG["services"].items()}
SITE = CONFIG["site"]
# Every part with tests, end-to-end tests included: (part name, tests setting).
TESTS = [(name, tests_of(s)) for name, s in CONFIG["services"].items() if tests_of(s)] + \
        [(name, tests_of(c)) for name, c in CONFIG["clients"].items() if tests_of(c)] + \
        ([("e2e", tests_of({"tests": CONFIG["e2e"]}))] if tests_of({"tests": CONFIG["e2e"]}) else [])
