"""Read the Artifact Driven configuration of the repository.

The repository root is the nearest directory, from the current directory up,
that holds artifact-driven.json. Without one, it is the parent of scripts/.
"""

from pathlib import Path
import json
import re
import sys

NAME = "artifact-driven.json"
DEFAULTS = {
    "knowledge": "docs/software-knowledges",
    "skip": [".git", "node_modules", "build"],
    "clients": {},
    "services": {},
    "e2e": None,
    "standards": [],
    "site": {"title": "Software Knowledge", "output": "build/site/index.html"},
}
TEST_GLOB = "**/*_test.*"
# Prefixes of names of standards that look like a knowledge ID, such as UTF-8
# or RFC-3339 (KN-1). A workspace adds its own under "standards" (CFG-9).
STANDARDS = ["UTF", "ISO", "RFC", "SHA", "TLS", "HTTP", "IEEE"]


def find_root():
    for folder in (Path.cwd(), *Path.cwd().parents):
        if (folder / NAME).is_file():
            return folder
    return Path(__file__).resolve().parent.parent


def tests_of(part):
    """The tests setting of a service or a client, with the default glob."""
    tests = part.get("tests") if isinstance(part, dict) else None
    return {"glob": TEST_GLOB, **tests} if tests and tests.get("folder") else None


def read_config(file):
    """The settings in the configuration file, or a problem line and status 2
    when it is not a JSON object (CFG-7)."""
    if not file.is_file():
        return {}
    try:
        settings = json.loads(file.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        stop(f"{file}:{e.lineno}:{e.colno}: not valid JSON: {e.msg}")
    if not isinstance(settings, dict):
        stop(f"{file}:1:1: not a JSON object")
    return settings


def stop(problem):
    """Report that a script cannot run, and exit with status 2 (SYS-3)."""
    print(problem, file=sys.stderr)
    sys.exit(2)


ROOT = find_root()
CONFIG = {**DEFAULTS, **read_config(ROOT / NAME)}
CONFIG["site"] = {**DEFAULTS["site"], **(CONFIG.get("site") or {})}

# A knowledge ID, such as SYS-4, G-SELL-2 or INV-3, and not the name of a standard.
_standards = CONFIG.get("standards") or []
if not isinstance(_standards, list) or not all(isinstance(s, str) for s in _standards):
    stop(f"{ROOT / NAME}:1:1: standards must be a list of prefixes, such as [\"PCI\"]")
ID = re.compile(r"\b(?!(?:" + "|".join(map(re.escape, STANDARDS + _standards)) + r")-)[A-Z]{1,6}(?:-[A-Z]{1,8})?-\d+\b")

KNOWLEDGE = ROOT / CONFIG["knowledge"]
SKIP = set(CONFIG["skip"])
SERVICES = {name: {"routes": s.get("routes"), "tests": tests_of(s)} for name, s in CONFIG["services"].items()}
SITE = CONFIG["site"]
# Every part with tests, end-to-end tests included: (part name, tests setting).
TESTS = [(name, tests_of(s)) for name, s in CONFIG["services"].items() if tests_of(s)] + \
        [(name, tests_of(c)) for name, c in CONFIG["clients"].items() if tests_of(c)] + \
        ([("e2e", tests_of({"tests": CONFIG["e2e"]}))] if tests_of({"tests": CONFIG["e2e"]}) else [])
