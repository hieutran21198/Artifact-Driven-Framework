"""Check Markdown links, heading anchors and knowledge IDs in the repository."""

from pathlib import Path
import re
import sys

from project import KNOWLEDGE, ROOT, SKIP

LINK = re.compile(r"\]\(([^)#\s]*)(?:#([^)\s]*))?\)")
HEADING = re.compile(r"^#+ (.*)$", re.MULTILINE)
ID = re.compile(r"\b[A-Z]{1,6}(?:-[A-Z]{1,8})?-\d+\b")
ID_DEFINITION = re.compile(r"^\| (" + ID.pattern + r") \|", re.MULTILINE)


def slug(heading):
    return re.sub(r"[^a-z0-9 -]", "", heading.lower()).replace(" ", "-")


def markdown_files():
    for path in ROOT.rglob("*.md"):
        if not SKIP.intersection(path.relative_to(ROOT).parts):
            yield path


def check_links():
    problems = []
    for path in markdown_files():
        for target, anchor in LINK.findall(path.read_text(encoding="utf-8")):
            if target.startswith(("http://", "https://", "mailto:")):
                continue
            resolved = (path.parent / target) if target else path
            where = path.relative_to(ROOT)
            if not resolved.exists():
                problems.append(f"{where}: missing {target}")
            elif anchor and resolved.suffix == ".md":
                headings = {slug(h) for h in HEADING.findall(resolved.read_text(encoding="utf-8"))}
                if anchor not in headings:
                    problems.append(f"{where}: missing anchor {target}#{anchor}")
    return problems


def check_ids():
    defined, cited = set(), {}
    for path in KNOWLEDGE.rglob("*"):
        if path.suffix not in {".md", ".yaml"}:
            continue
        text = path.read_text(encoding="utf-8")
        defined.update(ID_DEFINITION.findall(text))
        for found in ID.findall(text):
            cited.setdefault(found, path.relative_to(ROOT))
    return [f"{where}: {found} is cited but not defined" for found, where in sorted(cited.items()) if found not in defined]


def check_scenarios():
    operations = set()
    for path in KNOWLEDGE.rglob("*.yaml"):
        operations.update(re.findall(r"operationId: (\w+)", path.read_text(encoding="utf-8")))
    problems = []
    for path in (KNOWLEDGE / "flows").glob("*.md"):
        for row in re.findall(r"^\| (F-[A-Z]+-\d+) \|(.*)$", path.read_text(encoding="utf-8"), re.MULTILINE):
            named = set(re.findall(r"`(\w+)`", row[1])) & operations
            if not named and "worker" not in row[1].lower():
                problems.append(f"{path.relative_to(ROOT)}: {row[0]} names no operation")
    return problems


def main():
    problems = check_links() + check_ids() + check_scenarios()
    for problem in problems:
        print(problem, file=sys.stderr)
    if problems:
        return 1
    print("Docs check passed: links, anchors, knowledge IDs and scenario operations.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
