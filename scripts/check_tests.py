"""Check that tests name only knowledge IDs that exist and are not withdrawn.

Usage:
    python3 scripts/check_tests.py [DIR]    # default: the tests of every service and client in artifact-driven.json
"""

import sys

from check_docs import ID, ROOT, knowledge_ids
from impact import test_files, test_folders
from project import TESTS


def prefix(found):
    return found.rsplit("-", 1)[0]


def main(argv):
    if argv and not (ROOT / argv[0]).is_dir():
        print(f"Not a folder: {ROOT / argv[0]}", file=sys.stderr)
        return 2
    folders = test_folders(argv[0] if argv else None)
    if not folders:
        if not TESTS:
            print("No tests to check: artifact-driven.json gives no part a tests setting.")
            return 0
        # Parts have tests, and none of their folders is here: a job that did
        # not clone them must not pass (TST-6).
        names = ", ".join(f"{name} ({tests['folder']})" for name, tests in TESTS)
        print(f"No tests folder of any part exists: {names}. Clone the parts, or pass a folder.", file=sys.stderr)
        return 2
    defined, withdrawn = knowledge_ids()
    prefixes = {prefix(i) for i in defined}
    problems = set()
    for path in test_files(folders):
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
