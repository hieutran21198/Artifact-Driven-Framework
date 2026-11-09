"""Check Markdown links, heading anchors and knowledge IDs in the repository."""

from pathlib import Path
import re
import sys

from project import ID, KNOWLEDGE, ROOT, SKIP
from flow_rules import read_flow_rules, table_cells

LINK = re.compile(r"\]\(([^)#\s]*)(?:#([^)\s]*))?\)")
HEADING = re.compile(r"^#+ (.*)$", re.MULTILINE)
ID_DEFINITION = re.compile(r"^\| (" + ID.pattern + r") \|", re.MULTILINE)
ID_ROW = re.compile(r"^\| (" + ID.pattern + r") \| *(Withdrawn\b)?")


def slug(heading):
    return re.sub(r"[^a-z0-9 -]", "", heading.lower()).replace(" ", "-")


def anchors(text):
    """The anchors of a page's headings. A repeated anchor takes -1, -2 and so
    on, as GitHub gives it (REPO-3)."""
    found, seen = set(), {}
    for heading in HEADING.findall(text):
        base = slug(heading)
        n = seen.get(base, 0)
        seen[base] = n + 1
        found.add(f"{base}-{n}" if n else base)
    return found


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
                headings = anchors(resolved.read_text(encoding="utf-8"))
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
    """The names declared under the root keys x-triggers and x-commands of a contract."""
    return {name for block in re.finditer(r"^x-(?:triggers|commands):\n((?:[ \t]+.*\n?|\n)*)", text, re.MULTILINE)
            for name in re.findall(r"^  (\w+):", block.group(1), re.MULTILINE)}


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


def check_flow_rules():
    """Validate explicit Flow definitions and their lower-layer citations."""
    rules, problems, scopes = {}, [], {}
    for path in sorted(KNOWLEDGE.rglob("*.md")):
        page = path.relative_to(KNOWLEDGE)
        found, errors = read_flow_rules(page, path.read_text(encoding="utf-8"))
        problems.extend(errors)
        for name, rule in found.items():
            scope, owner = rule["scope"], rule["owner"]
            if scope in scopes and scopes[scope] != owner:
                problems.append(f"{owner}: {name} scope {scope} is also defined in {scopes[scope]}")
            scopes.setdefault(scope, owner)
        rules.update(found)
    defined, _ = knowledge_ids()
    for name, rule in rules.items():
        if re.match(r"Withdrawn\b", rule["rule"]):
            continue
        for dependency in set(rule["dependencies"]) | set(ID.findall(rule["rule"])):
            if dependency not in defined:
                continue  # KN-4 reports undefined citations.
            home = defined[dependency].relative_to(KNOWLEDGE.relative_to(ROOT)).parts[0]
            allowed = (home == "artifacts" and not dependency.startswith(("F-", "G-", "SYS-")) or
                       home == "system" and dependency.startswith("SYS-"))
            if dependency in rules or not allowed:
                problems.append(f'{rule["owner"]}: {name} depends on {dependency}, not an artifact rule or system requirement')
    for path in sorted((KNOWLEDGE / "artifacts").rglob("*")):
        if path.suffix in {".md", ".yaml"}:
            for name in sorted(set(ID.findall(path.read_text(encoding="utf-8"))) & rules.keys()):
                problems.append(f"{path.relative_to(ROOT)}: cites {name}, a layer above")
    for path in sorted((KNOWLEDGE / "goals").rglob("*.md")):
        columns = []
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.startswith("|"):
                columns = []
                continue
            cells = table_cells(line)
            if cells[0] == "ID":
                columns = cells
            elif "Proven by" in columns:
                proof = dict(zip(columns, cells)).get("Proven by", "")
                for name in sorted(set(ID.findall(proof)) & rules.keys()):
                    problems.append(f"{path.relative_to(ROOT)}: {name} is a Flow rule, not scenario proof")
    return problems


def main():
    problems = check_links() + check_ids() + check_scenarios() + check_direction() + check_flow_rules()
    for problem in problems:
        print(problem, file=sys.stderr)
    if problems:
        return 1
    print("Docs check passed: links, anchors, knowledge IDs, citation direction, and scenarios and the operations, triggers or commands they name.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
