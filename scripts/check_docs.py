"""Check Markdown links, heading anchors and knowledge IDs in the repository."""

from pathlib import Path
import re
import sys

from project import ID, KNOWLEDGE, ROOT, SKIP

LINK = re.compile(r"\]\(([^)#\s]*)(?:#([^)\s]*))?\)")
HEADING = re.compile(r"^#+ (.*)$", re.MULTILINE)
ID_DEFINITION = re.compile(r"^\| (" + ID.pattern + r") \|", re.MULTILINE)
ID_ROW = re.compile(r"^\| (" + ID.pattern + r") \| *(Withdrawn\b)?")


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


def knowledge_ids():
    """The defined knowledge IDs, with the file of each, and the withdrawn ones."""
    defined, withdrawn = {}, set()
    for path in sorted(KNOWLEDGE.rglob("*")):
        if path.suffix in {".md", ".yaml"}:
            for line in path.read_text(encoding="utf-8").splitlines():
                row = ID_ROW.match(line)
                if row:
                    defined.setdefault(row.group(1), path.relative_to(ROOT))
                    if row.group(2):
                        withdrawn.add(row.group(1))
    return defined, withdrawn


def check_ids():
    defined, withdrawn, cited, problems = {}, set(), [], []
    for path in sorted(KNOWLEDGE.rglob("*")):
        if path.suffix not in {".md", ".yaml"}:
            continue
        where = path.relative_to(ROOT)
        for line in path.read_text(encoding="utf-8").splitlines():
            row = ID_ROW.match(line)
            if row:
                if row.group(1) in defined:
                    problems.append(f"{where}: {row.group(1)} is defined twice, also in {defined[row.group(1)]}")
                defined.setdefault(row.group(1), where)
                if row.group(2):
                    withdrawn.add(row.group(1))
                    continue
            own = row.group(1) if row else None
            cited.extend((found, where) for found in ID.findall(line) if found != own)
    for found, where in cited:
        if found not in defined:
            problems.append(f"{where}: {found} is cited but not defined")
        elif found in withdrawn:
            problems.append(f"{where}: {found} is withdrawn and still cited")
    return sorted(set(problems))


def triggers(text):
    """The names declared under the root key x-triggers of a contract."""
    block = re.search(r"^x-triggers:\n((?:[ \t]+.*\n?|\n)*)", text, re.MULTILINE)
    return set(re.findall(r"^  (\w+):", block.group(1), re.MULTILINE)) if block else set()


def check_scenarios():
    operations = set()
    for path in KNOWLEDGE.rglob("*.yaml"):
        text = path.read_text(encoding="utf-8")
        operations.update(re.findall(r"operationId: (\w+)", text))
        operations.update(triggers(text))
    problems, used = [], set()
    for path in sorted((KNOWLEDGE / "flows").glob("*.md")):
        for row in re.findall(r"^\| (F-[A-Z]+-\d+) \|(.*)$", path.read_text(encoding="utf-8"), re.MULTILINE):
            if row[1].lstrip().startswith("Withdrawn"):
                continue
            named = set(re.findall(r"`(\w+)`", row[1])) & operations
            used |= named
            if not named:
                problems.append(f"{path.relative_to(ROOT)}: {row[0]} names no operation")
    problems += [f"{name} is named by no scenario" for name in sorted(operations - used)]
    return problems


def check_direction():
    """A layer cites only the layers below it: a flow names no goal criterion,
    an artifact names no goal criterion or flow scenario."""
    upward = {"flows": re.compile(r"\bG-[A-Z]+-\d+\b"), "artifacts": re.compile(r"\b[GF]-[A-Z]+-\d+\b")}
    problems = []
    for folder, pattern in upward.items():
        for path in sorted((KNOWLEDGE / folder).rglob("*")):
            if path.suffix in (".md", ".yaml"):
                for name in sorted(set(pattern.findall(path.read_text(encoding="utf-8")))):
                    problems.append(f"{path.relative_to(ROOT)}: cites {name}, a layer above")
    return problems


def main():
    problems = check_links() + check_ids() + check_scenarios() + check_direction()
    for problem in problems:
        print(problem, file=sys.stderr)
    if problems:
        return 1
    print("Docs check passed: links, anchors, knowledge IDs, citation direction, and scenarios and the operations or triggers they name.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
