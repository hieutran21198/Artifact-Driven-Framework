"""Read the Artifact Driven configuration of the repository.

The repository root is the nearest directory, from the current directory up,
that holds artifact-driven.json. Without one, it is the parent of scripts/.
"""

from pathlib import Path
import json

NAME = "artifact-driven.json"
DEFAULTS = {
    "knowledge": "docs/software-knowledge",
    "skip": [".git", "node_modules", "build"],
    "clients": {},
    "routes": None,
    "site": {"title": "Software knowledge", "output": "build/site/index.html"},
}


def find_root():
    for folder in (Path.cwd(), *Path.cwd().parents):
        if (folder / NAME).is_file():
            return folder
    return Path(__file__).resolve().parent.parent


ROOT = find_root()
_file = ROOT / NAME
CONFIG = {**DEFAULTS, **(json.loads(_file.read_text(encoding="utf-8")) if _file.is_file() else {})}
CONFIG["site"] = {**DEFAULTS["site"], **(CONFIG.get("site") or {})}

KNOWLEDGE = ROOT / CONFIG["knowledge"]
SKIP = set(CONFIG["skip"])
CLIENTS = dict(CONFIG["clients"])
ROUTES = CONFIG["routes"]
SITE = CONFIG["site"]
