"""Check that tests name only knowledge IDs that exist and are not withdrawn.

Usage:
    python3 scripts/check_tests.py [DIR]    # default: tests.folder in artifact-driven.json
"""

import sys

from check_docs import ID, ROOT, knowledge_ids
from impact import test_files
from project import TESTS


def prefix(found):
    return found.rsplit("-", 1)[0]


def main(argv):
    name = argv[0] if argv else TESTS["folder"]
    if not name:
        print("No tests folder: pass one, or set tests.folder in artifact-driven.json.", file=sys.stderr)
        return 2
    folder = ROOT / name
    if not folder.is_dir():
        print(f"Not a folder: {folder}", file=sys.stderr)
        return 1
    defined, withdrawn = knowledge_ids()
    prefixes = {prefix(i) for i in defined}
    problems = set()
    for path in test_files(folder):
        for found in ID.findall(path.read_text(encoding="utf-8", errors="ignore")):
            if prefix(found) not in prefixes:
                continue
            where = path.relative_to(ROOT) if path.is_relative_to(ROOT) else path
            if found not in defined:
                problems.add(f"{where}: {found} is not defined in the knowledge")
            elif found in withdrawn:
                problems.add(f"{where}: {found} is withdrawn")
    for problem in sorted(problems):
        print(problem, file=sys.stderr)
    if problems:
        return 1
    print("Test check passed: every knowledge ID named in a test exists.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
